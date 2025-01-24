from django.contrib import admin
from .models import Posts
from .models import ContactMessage
# Register your models here.

admin.site.register(Posts)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')

