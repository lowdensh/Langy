from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
import nltk


class Author(models.Model):
    forename = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    middle_names = models.CharField(max_length=100, blank=True)

    # Adds a period after single character names
    def format(self, name):
        if len(name) == 1:
            return f'{name}.'
        return name

    @property
    def full_name(self):
        # Forename first
        return f'{self.format(self.forename)} {self.format(self.middle_names)} {self.format(self.surname)}'

    def __str__(self):
        # Surname first, with comma
        return f'{self.format(self.surname)}, {self.format(self.forename)} {self.format(self.middle_names)}'

    class Meta:
        ordering = ['surname', 'forename', 'middle_names',]


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(to=Author, on_delete=models.SET_DEFAULT, default=1)
    source_url = models.URLField('Source URL')
    summary = models.TextField(max_length=1000, blank=True)
    cover = models.ImageField(upload_to='book_covers', default='book_covers/default.jpg')
    pdf = models.FileField(
        'PDF',
        help_text='A PDF file representing the book. This can be blank. Used to generate Pages.',
        upload_to='book_pdfs',
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    @property
    def page_count(self):
        return self.pages.count()

    @property
    def has_pages(self):
        if self.page_count > 0:
            return True
        return False

    @property
    def summary_text(self):
        if self.summary:
            return self.summary
        return f'{self.title}, written by {self.author.full_name}.'

    @property
    def has_cover(self):
        if self.cover.name == 'book_covers/default.jpg':
            return False
        return True

    @property
    def has_pdf(self):
        if self.pdf:
            return True
        return False

    @property
    def translatable_word_count(self):
        return self.translatable_words.count()

    @property
    def has_translatable_words(self):
        if self.translatable_word_count == 0:
            return False
        return True
    
    # Returns a list of Translations
    #   for the TranslatableWords used by this Book for a given ForeignLanguage.
    def available_translations(self, foreign_language):
        return [
            tw.translation(foreign_language)
            for tw in self.translatable_words.all()
            if tw.translation(foreign_language) is not None
        ]

    # Returns an int
    #   for the amount of words that can be learnt from this Book for a given ForeignLanguage.
    def words_to_learn(self, foreign_language):
        return len(self.available_translations(foreign_language))

    # Returns a string
    #   representing how "difficult" the book is, with respect to the amount of foreign words
    def difficulty(self, foreign_language):
        if self.words_to_learn(foreign_language) <= 11:
            return 'Easy'
        elif self.words_to_learn(foreign_language) <= 15:
            return 'Medium'
        else:
            return 'Hard'
    
    # Returns an int
    #   for the number of non-unique English words in the Book's Pages
    @property
    def english_word_count(self):
        counts = [page.english_word_count for page in self.pages.all()]
        return sum(counts)
    
    # Returns a string
    #   representing how "long" the book is, with respect to the amount of English words in total
    @property
    def length(self):
        if self.english_word_count <= 700:
            return 'Short'
        elif self.english_word_count <= 1000:
            return 'Medium'
        else:
            return 'Long'
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'author',]


class Page(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name='pages')
    number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    text = models.TextField()
    image = models.ImageField(upload_to='book_page_images', blank=True, null=True)

    # Returns a string
    #   which is a short snippet of the text at the beginning of this page.
    @property
    def text_snippet(self):
        max_length = 50
        if len(self.text) <= max_length:
            return f'{self.text}'
        else:
            return f'{self.text[0:max_length]}...'
    
    # Returns an int
    #   for the number of non-unique English words in the Page text
    @property
    def english_word_count(self):
        words = nltk.tokenize.word_tokenize(self.text)
        words = [w for w in words if w.isalnum()]
        return len(words)
    
    def __str__(self):
        return f'{self.book}, pg. {self.number} ({self.text_snippet})'

    class Meta:
        ordering = ['book', 'number',]
