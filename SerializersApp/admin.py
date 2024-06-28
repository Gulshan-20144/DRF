from django.contrib import admin
from SerializersApp.models import BookStore, Books
# Register your models here.
@admin.register(BookStore)
class BookStoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'books', 'Qty')
    list_filter = ('user', 'books')
    search_fields = ('name', 'user__username', 'books__name')
    ordering = ('id',)
    # other configurations

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)
   