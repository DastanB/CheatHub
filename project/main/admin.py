from django.contrib import admin
from main import models


@admin.register(models.Order)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'executor', 'description', 'pictures', 'created_at', 'due_to', 'price', 'payment_type', 'order_type')
    