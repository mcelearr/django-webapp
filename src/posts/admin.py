from django.contrib import admin

# Register your models here.
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "updated", "timestamp"]
    list_display_links = ["__unicode__"]
    list_filter = ["updated", "timestamp"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
