from django.contrib import admin

# Register your models here.


from .models import *
admin.register(demDatatable)(admin.ModelAdmin)
admin.register(demDailyData)(admin.ModelAdmin)