from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.

class Book_Author(models.Model):
    author_name = models.CharField(max_length=30)

    def __str__(self):
        return self.author_name

class Book_Publisher(models.Model):
    publisher_name = models.CharField(max_length=60)
    publisher_number = models.IntegerField(
        null=True,
        validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(6000000000)
        ]
    )
    pubilsher_address = models.CharField(max_length=150, default='Unknown')

    def __str__(self):
        return self.publisher_name

class Library_Branch(models.Model):
    branch_name = models.CharField(max_length=60)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.branch_name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Book_Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Book_Publisher, on_delete=models.CASCADE)
    branch = models.ForeignKey(Library_Branch, on_delete=models.CASCADE)
    published_year = models.PositiveIntegerField(
        default=timezone.now().year,
        validators=[
            MaxValueValidator(2024),
            MinValueValidator(1950)
        ]
    )
    num_copies = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title

class Borrower(models.Model):
    borrower_name = models.CharField(max_length=30)
    borrower_number = models.IntegerField(
        null=True,
        validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(6000000000)
        ]
    )
    loan_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    branch = models.ForeignKey(Library_Branch, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.borrower_name} borrowed {self.book} from {self.branch} on {self.loan_date}"
