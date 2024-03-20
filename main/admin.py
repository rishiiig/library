from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Book_Author)
admin.site.register(Book_Publisher)
admin.site.register(Library_Branch)
admin.site.register(Book)
admin.site.register(Borrower)