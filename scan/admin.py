from django.contrib import admin

from scan.models import Uploads

# Register your models here.


class UploadsAdmin(admin.ModelAdmin):
    date_hierarchy = 'uploaded_at'
    list_display = ['id', 'image', 'user', 'uploaded_at']


admin.site.register(Uploads, UploadsAdmin)
