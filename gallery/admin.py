from django.contrib import admin

from gallery.models import Photo


# Register your models here.
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
