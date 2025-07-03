from django.contrib import admin
from .models import JournalEntry, Note

# Register your models here.
admin.site.register(JournalEntry)
admin.site.register(Note)
