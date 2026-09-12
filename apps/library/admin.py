from django.contrib import admin
from .models import BookCategory, Book, BookIssue


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'total_copies', 'available_copies', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'author', 'isbn')


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower_type', 'student', 'staff', 'issue_date', 'due_date', 'return_date', 'status', 'fine_amount')
    list_filter = ('status', 'borrower_type')
    search_fields = ('book__title', 'student__full_name', 'staff__full_name')