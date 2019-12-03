from django.contrib import admin
from main.models import Order, OrderPicture, CommentOrder, Review, CommentReview 


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'executor', 'description', 'pictures', 'created_at', 'due_to', 'price', 'payment_type', 'order_type')

@admin.register(OrderPicture)
class OrderPictureAdmin(admin.ModelAdmin):
    list_display = '__all__' 

@admin.register(CommentOrder)
class CommentOrderAdmin(admin.ModelAdmin):
    list_display = '__all__' 

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = '__all__' 

@admin.register(CommentReview)
class CommentReviewAdmin(admin.ModelAdmin):
    list_display = '__all__' 