from django.contrib import admin
from django.utils.text import slugify
from .models import Activity, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Activity)
class ActivityAdmin(SummernoteModelAdmin):

    list_display = ('name', 'status')
    search_fields = ['name']
    list_filter = ('status',)
    summernote_fields = ('description',)

    def save_model(self, request, obj, form, change):
        """
        Prepopulate the slug based on the name field.
        """
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)

    prepopulated_fields = {'slug': ('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'created_on', 'user', 'activity', 'approved')
    list_filter = ('created_on', 'approved')

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = 'Approve selected comments'

    actions = [approve_comments]