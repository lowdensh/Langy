"""
Create a csv of transformed learning traces to use as input to a model.
Foreign words are transformed into embed features.
Outliers are removed and data is standardised.
"""

from django.core.management.base import BaseCommand, CommandError
from tracking.management.commands._slutil import tprint
from tracking.management.commands._vocabulary import get_word_to_ix
import numpy as np
import pandas as pd
import torch
import torch.nn as nn


csv_directory = 'model_data/'

EMBEDDING_DIM = 5     # 5 dimensional word embeddings
torch.manual_seed(1)  # reproducible results


# Returns a Tensor
#   for a foreign word embedding.
#   e.g. 'lernen' : tensor([[ 0.5695, -0.0698, -0.8072,  0.7015, -0.1184]])
#   An embedding is a numerical encoding of a string.
#   Each Tensor has EMBEDDING_DIM dimensions, where each item is a float.
def get_embed(word, word_to_ix, embeddings):
    try:
        ix = word_to_ix[word]
    except KeyError:
        # tprint(f'No index for word \'{word}\'')
        return torch.zeros(1, EMBEDDING_DIM, dtype=torch.long)

    lookup_tensor = torch.tensor([word_to_ix[word]], dtype=torch.long)
    return embeddings(lookup_tensor)


# Normalise a pandas series based on its mean and standard deviation.
# A mean and std can be optionally provided for reproducible results.
def standardise(series, verbose=False, series_mean=None, series_std=None):
    if verbose: tprint(f'Standardising series: {series.name}')

    if series_mean == None:
        series_mean = series.mean()
    if series_std == None:
        series_std = series.std()

    if verbose:
        tprint(f'   mean: {series_mean}')
        tprint(f'   std: {series_std}')

    series_standardised = (series - series_mean) / series_std
    return series_standardised


# Get ith item from Tensor in embed column
def get_embed_item(row, i):
    return row['embed'][0][i].item()


# Transform foreign words into embed features
def words_to_embeds(df, word_to_ix, embeddings, verbose=False):
    # Get embeds for all foreign words
    if verbose: tprint('getting embeds for foreign words')
    df['embed'] = df['frn'].apply(
        get_embed,
        word_to_ix=word_to_ix,
        embeddings=embeddings)

    # Create new feature per embed dimension
    if verbose: tprint('creating features for word embeds')
    for i in range(EMBEDDING_DIM):
        if verbose: tprint(f'embed feature {i+1}/{EMBEDDING_DIM}')
        df[f'frn_{i}'] = df.apply(get_embed_item, i=i, axis=1)
    
    # Drop columns now that foreign words are represented numerically
    if verbose: tprint('dropping columns')
    df.drop(['frn', 'embed'], axis=1, inplace=True)

    return df


class Command(BaseCommand):
    help = ('Create a csv of transformed learning traces to use as input to a model. '
            'Foreign words are transformed into embed features.'
            'Outliers are removed and data is standardised.')


    def handle(self, *args, **kwargs):
        input_csv = f'{csv_directory}learning_traces_duolingo_subset.csv'
        output_csv = f'{csv_directory}model_input_duolingo_subset.csv'

        # Read csv and create dataframe
        tprint(f'reading {input_csv} and creating dataframe')
        df = None
        try:
            df = pd.read_csv(input_csv)
        except:
            raise CommandError(f'could not read {input_csv}')

        # Display data
        tprint(f'{df.shape[0]} datapoints:')
        print(df.head())


        ###################
        # Word Embeddings #
        ###################

        # Dictionary mapping unique foreign words to indices
        word_to_ix = get_word_to_ix()

        # Stores embeddings for all words
        # Indices from word_to_ix are used to find the embedding for a particular word
        embeddings = nn.Embedding(len(word_to_ix), EMBEDDING_DIM)
        
        # Replace foreign words with embeddings
        df = words_to_embeds(df, word_to_ix, embeddings, verbose=True)

        # Display data
        tprint(f'{df.shape[0]} datapoints:')
        print(df.head())


        ##################
        # Pre-Processing #
        ##################

        # Interquartile range
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1

        # Remove outliers / extreme values
        df = df[
        ~(
            (df < (Q1 - 1.5 * IQR))
            | (df > (Q3 + 1.5 * IQR))
        ).any(axis=1)]

        # Standardisation for delta and interaction statistics only
        # Not performed on word embeddings
        df['delta'] = standardise(df['delta'], verbose=True)
        df['seen'] = standardise(df['seen'], verbose=True)
        df['interacted'] = standardise(df['interacted'], verbose=True)
        df['tested'] = standardise(df['tested'], verbose=True)
        df['correct'] = standardise(df['correct'], verbose=True)

        # Display data
        tprint(f'{df.shape[0]} datapoints:')
        print(df.head())


        #######
        # CSV #
        #######

        # Create csv
        tprint(f'creating {output_csv}')
        try:
            df.to_csv(output_csv, index=False)
        except:
            raise CommandError(f'could not create {output_csv}')

        tprint('done.')
