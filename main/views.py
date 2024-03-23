from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def default(request):
    return render(request, 'index.html')

def borrow(request):
    return render(request, 'borrow.html')

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
        return redirect('add_data')

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

def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author_id = request.POST.get('author', None)
        new_author_name = request.POST.get('new_author', None)
        publisher_id = request.POST.get('publisher_name', None)
        new_publisher_name = request.POST.get('new_publisher_name', None)
        new_publisher_number = request.POST.get('new_publisher_number', None)
        new_publisher_address = request.POST.get('new_publisher_address', None)
        branch_id = request.POST.get('branch', None)
        new_branch_name = request.POST.get('new_branch', None)
        new_location = request.POST.get('new_location', None)
        published_year = request.POST['published_year']
        num_copies = request.POST['num_copies']

        # Handling Author
        if author_id:
            author = Book_Author.objects.get(id=author_id)
        elif new_author_name:
            author = Book_Author.objects.create(author_name=new_author_name)
        else:
            return redirect('add_book')

        # Handling Publisher
        if publisher_id:
            publisher = Book_Publisher.objects.get(id=publisher_id)
        elif new_publisher_name:
            publisher = Book_Publisher.objects.create(publisher_name=new_publisher_name, 
                                                       publisher_number=new_publisher_number, 
                                                       pubilsher_address=new_publisher_address)
        else:
            return redirect('add_book')

        # Handling Branch
        if branch_id:
            branch = Library_Branch.objects.get(id=branch_id)
        elif new_branch_name and new_location:
            branch = Library_Branch.objects.create(branch_name=new_branch_name, location=new_location)
        else:
            return redirect('add_book')

        # Saving Book
        book = Book.objects.create(title=title, author=author, publisher=publisher, branch=branch, 
                                   published_year=published_year, num_copies=num_copies)

        return redirect('add_book')

    # Fetching data to populate dropdowns
    authors = Book_Author.objects.all()
    publishers = Book_Publisher.objects.all()
    branches = Library_Branch.objects.all()

    return render(request, 'add_book.html', {'authors': authors, 'publishers': publishers, 'branches': branches})

def borrow(request):
    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        book_id = request.POST.get('book')
        borrower_name = request.POST.get('borrower_name')
        borrower_number = request.POST.get('borrower_number')
        loan_date = request.POST.get('loan_date')
        return_date = request.POST.get('return_date')

        # book = Book.objects.get(pk=book_id)
        book = Book.objects.filter(id=book_id, branch_id=branch_id).first()

        if book and book.num_copies > 0:
            branch = Library_Branch.objects.get(pk=branch_id)
            borrower = Borrower.objects.create(
                borrower_name=borrower_name,
                borrower_number=borrower_number,
                loan_date=loan_date,
                return_date=return_date,
                book=book,
                branch=branch
            )
            borrower.save()

            # Update the number of copies
            book.num_copies -= 1
            book.save()

            return redirect('borrow')
        else:
            messages.error(request, 'No copies of this book are available at the selected branch')
            return redirect('borrow')

    else:
        branches = Library_Branch.objects.all()
        return render(request, 'borrow.html', {'branches': branches})

def get_books(request):
    branch_id = request.GET.get('branch_id')
    books = Book.objects.filter(branch_id=branch_id).values('id', 'title')
    return JsonResponse(list(books), safe=False)

def view(request):
    authors = Book_Author.objects.all()
    publishers = Book_Publisher.objects.all()
    branches = Library_Branch.objects.all()
    books = Book.objects.all()
    borrowers = Borrower.objects.all()

    return render(request, 'view.html', {
        'authors': authors,
        'publishers': publishers,
        'branches': branches,
        'books': books,
        'borrowers': borrowers }
        )

def view_borrowers(request):
    borrowers = Borrower.objects.all()
    current_date = timezone.now().date()  # Get current date in server's timezone

    return render(request, 'view_borrowers.html', {
        'borrowers': borrowers,
        'current_date': current_date,  # Pass current date to the template
    })

def receive_book(request, borrower_id):
    if request.method == 'POST':
        try:
            borrower = Borrower.objects.get(pk=borrower_id)
            book = borrower.book

            # Deleting the borrower record
            borrower.delete()

            # Increasing the book count for the branch
            book.num_copies += 1
            book.save()

            return redirect('view_borrowers')

        except Borrower.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Borrower not found'})

    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
