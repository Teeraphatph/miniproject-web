from django.contrib.auth.models import User 
# as AuthUser
from django.db import models
#Customer
# class User(models.Model):
#     user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, null=True, blank=True)  # ทำให้ nullable
#     firstname = models.CharField(max_length=100)
#     lastname = models.CharField(max_length=100)
#     user_address = models.TextField()


    # def __str__(self):
    #     return self.user.username 

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # เชื่อมโยงกับ User
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, null=True, blank=True)  
    
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    default_address = models.OneToOneField(Address, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)



class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100)
    complete = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # ดึง default_address จาก Customer แทน User
        if not hasattr(self.customer, 'default_address'):
            raise ValueError("Customer does not have a default address.")
        
        self.address = self.customer.default_address
        super(Order, self).save(*args, **kwargs)

class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    quantity = models.PositiveIntegerField(default=0) 
    price = models.DecimalField(max_digits=10, decimal_places=2 )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notification = models.TextField(blank=True, null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        # ตรวจสอบราคาและตั้งค่าราคาเริ่มต้น
        if self.price is None:  # หรือ self.price < 0
            self.price = 0.00  # ตั้งราคาเริ่มต้น
        self.total_price = self.price * self.quantity  # คำนวณ total_price
        super().save(*args, **kwargs)
  # รูปภาพหลัก

# class Color(models.Model):
#     name = models.CharField(max_length=50)

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='products/')
#     color = models.ForeignKey(Color, on_delete=models.CASCADE, default=1)

class Color(models.Model):
    name = models.CharField(max_length=50)  # ชื่อของสี
    hex_value = models.CharField(max_length=7, default='#FFFFFF')  # ค่าสีแบบ Hex เช่น #FFFFFF

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)  # ฟิลด์สี

    def __str__(self):
        return f"{self.product.name} - {self.color.name if self.color else 'No Color'}"

# class CartItem(models.Model):
#     # Replace '1' with an actual Order ID that exists
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, default=1, related_name='cart_items') 
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
    

#     @property
#     def total_price(self):
#         return self.quantity * self.product.price

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"

# class CartItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='cart_items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
#     notification = models.TextField(blank=True, null=True)

#     @property
#     def total_price(self):
#         # คำนวณราคาทั้งหมดตามปริมาณ
#         return self.quantity * self.product.price

#     def save(self, *args, **kwargs):
#         # อัปเดตราคาก่อนที่จะบันทึก
#         self.price = self.product.price
#         self.total_price = self.total_price  # หรือคำนวณจาก quantity * price
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, editable=False)

    notification = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.quantity > 0 and self.price > 0:
            self.total_price = self.quantity * self.price
        else:
            self.total_price = 0.0
        super().save(*args, **kwargs)  # วิธีนี้ใช้ได้ใน Python 3.x

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)