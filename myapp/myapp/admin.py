from django.contrib import admin
from .models import User, Address, Admin, Order, OrderItem, Product,Customer

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total_price')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # ร่วมข้อมูลผู้ใช้กับ Order
        return queryset.select_related('order__customer')

    def order(self, obj):
        return obj.order.customer.user.username if obj.order.customer else "Unknown User"

admin.site.register(Address)
admin.site.register(Admin)
admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Product)
admin.site.register(Customer)