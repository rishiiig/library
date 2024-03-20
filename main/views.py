from django.shortcuts import render, redirect
from .models import Book_Author, Book_Publisher, Library_Branch, Book, Borrower

# Create your views here.

def default(request):
    return render(request, 'index.html')

def add_data(request):
    if request.method == 'POST':
        # Retrieve form data
        author_id = request.POST.get('author')
        new_author_name = request.POST.get('new_author')
        publisher_id = request.POST.get('publisher')
        new_publisher_name = request.POST.get('new_publisher')
        book_title = request.POST.get('book_title')
        branch_id = request.POST.get('branch')
        new_location = request.POST.get('new_location')
        new_branch_name = request.POST.get('new_branch')
        borrower_name = request.POST.get('borrower_name')
        contact_info = request.POST.get('contact_info')
        loan_date = request.POST.get('loan_date')
        return_date = request.POST.get('return_date')
        
        # Add new author if provided, otherwise use selected author
        if new_author_name:
            author = Book_Author.objects.create(author_name=new_author_name)
        elif author_id:
            author = Book_Author.objects.get(pk=author_id)
        else:
            author = None
        
        # Add new publisher if provided, otherwise use selected publisher
        if new_publisher_name:
            publisher = Book_Publisher.objects.create(publisher_name=new_publisher_name)
        elif publisher_id:
            publisher = Book_Publisher.objects.get(pk=publisher_id)
        else:
            publisher = None
        
        # Add new branch if provided, otherwise use selected branch
        if new_branch_name:
            branch = Library_Branch.objects.create(branch_name=new_branch_name, location=new_location)
        elif branch_id:
            branch = Library_Branch.objects.get(pk=branch_id)
        else:
            branch = None
        
        # Create book
        book = Book.objects.create(title=book_title, author=author, publisher=publisher, branch=branch)
        
        # Create borrower and loan record
        borrower = Borrower.objects.create(borrower_name=borrower_name, contact_info=contact_info, loan_date=loan_date, return_date=return_date, book=book)
        
        # Redirect to a success page or the same page (for another entry)
        # return redirect('success_page')  # Redirect to a success page
        return redirect('add_data')  # Redirect to the same page for another entry

    else:
        # Fetch existing data for dropdowns
        authors = Book_Author.objects.all()
        publishers = Book_Publisher.objects.all()
        branches = Library_Branch.objects.all()

        context = {
            'authors': authors,
            'publishers': publishers,
            'branches': branches,
        }
        return render(request, 'add_data.html', context)
