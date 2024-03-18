from django.contrib import admin
from .models import Activity
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Activity)
class ActivityAdmin(SummernoteModelAdmin):

    list_display = ('name', 'status')
    search_fields = ['name']
    list_filter = ('status',)
    summernote_fields = ('description',)