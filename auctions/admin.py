from django.contrib import admin
from .models import Category, Comment, User, Picture, Listing, Bid
# Register your models here.


class CommentInline(admin.TabularInline):
    model = Comment


class ListingAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Picture)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
