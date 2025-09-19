from django.contrib import admin

from perfume_app.models import Perfumes

# Register your models here.
@admin.register(Perfumes)
class PerfumesAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name')