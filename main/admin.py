from django.contrib import admin
from .models import Habit, PlannerTask
from .models import Product

admin.site.register(Habit)
admin.site.register(PlannerTask)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'category')