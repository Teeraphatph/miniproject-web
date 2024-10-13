from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login,update_session_auth_hash  
from django.contrib.auth.models import User, auth
from .forms import RegisterForm ,ProductForm,LoginForm,ProductImageForm,RegisterForm,UserUpdateForm
from .models import Product,ProductImage,OrderItem,Order,Customer,CartItem,Order,Address
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import ValidationError
from collections import defaultdict
from django.http import JsonResponse
import json
from django.dispatch import receiver
from django.db.models.signals import post_save
from .forms import CustomUserCreationForm,PaymentForm,CheckoutForm
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm  
from django.db.models import Q,Sum  
from .utility import calculate_total
from django.http import HttpResponse
from django.utils import timezone


def index(request):
    products = Product.objects.all()  
    return render(request, 'index.html', {'products': products})

def product(request):
    products = Product.objects.all() 
    return render(request, 'product.html', {'products': products})

def product_admin(request):
    products = Product.objects.all()  
    return render(request, 'product_admin.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('product_admin')  
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # เพิ่ม request.FILES
        if form.is_valid():
            form.save()
            return redirect('product_admin')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_admin') 
    return render(request, 'confirm_delete.html', {'product': product})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def food3(request):
    return render(request, 'food3.html')

def profile(request):
    return render(request, 'profile.html')

@user_passes_test(lambda u: u.is_superuser)
def list_user(request):
    users = User.objects.prefetch_related('customer')  
    return render(request, 'list_user.html', {'users': users})


def backend_view(request):
    products = Product.objects.all()
    sold_data = {}
    total_revenue = 0  # สร้างตัวแปรเพื่อเก็บยอดรายได้รวม

    for product in products:
        sold_quantity = OrderItem.objects.filter(product=product).aggregate(total_sold=Sum('quantity'))['total_sold'] or 0
        sold_data[product.name] = int(sold_quantity)
        
        # คำนวณรายได้รวมจากการขาย
        total_revenue += sold_quantity * product.price  # เพิ่มรายได้ของสินค้านั้นเข้ายอดรวม

    context = {
        'products': products,
        'sold_data': sold_data,
        'total_revenue': total_revenue,  # ส่งข้อมูลรายได้รวมไปยังเทมเพลต
    }
    return render(request, 'backend.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'ไม่มีผู้ใช้นี้ในระบบ')
            else:
                
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    
                    if user.is_superuser:
                        return redirect('backend') 
                    else:
                        return redirect('index') 
                else:
                    messages.error(request, 'รหัสผ่านไม่ถูกต้อง')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            
            if not hasattr(user, 'customer'):
                Customer.objects.create(
                    user=user, 
                    name=f"{user.first_name} {user.last_name}",  # ใช้ชื่อและนามสกุล
                    email=user.email  
                )
                
            messages.success(request, 'สมัครสมาชิกเรียบร้อยแล้ว!')
            return redirect('login')
        else:
            
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})



def upload_product_image(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            product_image = form.save(commit=False)
            product_image.product = product
            product_image.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductImageForm()

    return render(request, 'upload_product_image.html', {'form': form, 'product': product})

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    if request.user.is_authenticated:
        customer = request.user.customer
        
        product = Product.objects.get(id=productId)

        order_queryset = Order.objects.filter(customer=customer, complete=False)

        if order_queryset.exists():
            order = order_queryset.latest('order_date')
        else:
            order = Order.objects.create(customer=customer, complete=False)

        cart_item, created = CartItem.objects.get_or_create(order=order, product=product)

        if created:
            cart_item.price = product.price 
        if action == 'add':
            cart_item.quantity += 1
        elif action == 'remove':
            cart_item.quantity -= 1

        cart_item.price = product.price 
        cart_item.save()

        if cart_item.quantity <= 0:
            cart_item.delete()

        if cart_item.order.cart_items.count() == 0:
            cart_item.order.delete()

        return JsonResponse('Item was added', safe=False)

    return JsonResponse('User not logged in', safe=False)

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'customer'):
        Customer.objects.create(
            user=instance,
            name=f"{instance.first_name} {instance.last_name}",
            email=instance.email
        )

@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()

def some_view(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer  

        except Customer.DoesNotExist:

            customer = Customer.objects.create(user=request.user)

def create_customer_for_existing_users():
    users_without_customers = User.objects.filter(customer__isnull=True)
    for user in users_without_customers:
        Customer.objects.create(user=user)

create_customer_for_existing_users()


def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(order__customer=request.user.customer)
        total_amount = sum(item.total_price for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_amount': total_amount,
        }
    else:
        cart_items = []
        total_amount = 0

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

@user_passes_test(lambda u: u.is_superuser)
def admin_order(request):
    order_items_by_user = {}

    order_items = OrderItem.objects.select_related('order__customer__user', 'order__address')

    for item in order_items:
        item.notification = f"ผู้ใช้เพิ่ม: {item.product.name}"

        user = item.order.customer.user 
        username = f"{user.first_name} {user.last_name}"
        order_number = item.order.id
        
        if item.order.address:
            address = (
                f"{item.order.address.address_line1}, "
                f"{item.order.address.city}, "
                f"{item.order.address.state}, "
                f"{item.order.address.postal_code}"

            )
            phone_number = item.order.address.phone_number
        else:
            address = "ไม่มีที่อยู่ที่ระบุ"
            phone_number = "ไม่มีหมายเลขโทรศัพท์ที่ระบุ"

        order_date = timezone.localtime(item.order.order_date)

        if username not in order_items_by_user:
            order_items_by_user[username] = {}

        if order_number not in order_items_by_user[username]:
            order_items_by_user[username][order_number] = {
                'items': [],
                'total': 0,
                'address': address,
                'phone_number': phone_number,
                'order_number': order_number,
                'order_date': order_date,
                

            }

        order_items_by_user[username][order_number]['items'].append(item)
        order_items_by_user[username][order_number]['total'] += item.total_price

    print(order_items_by_user)

    return render(request, 'admin_order.html', {'order_items_by_user': order_items_by_user})


def search_product(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'search_results.html', {'products': products, 'query': query})

# @login_required
# def checkout(request):
#     if request.method == 'POST':
#         address_line1 = request.POST.get('address_line1')
#         address_line2 = request.POST.get('address_line2', '')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         postal_code = request.POST.get('postal_code')
#         phone_number = request.POST.get('phone_number')

        
#         customer, created = Customer.objects.get_or_create(user=request.user)

        
#         address = Address.objects.create(
#             user=request.user,
#             address_line1=address_line1,
#             address_line2=address_line2,
#             city=city,
#             state=state,
#             postal_code=postal_code,
#             phone_number=phone_number
#         )

        
#         customer.default_address = address 
#         customer.save() 

#         order = Order.objects.create(customer=customer, address=address)

#         cart_items = CartItem.objects.filter(order__customer=request.user.customer)

#         for cart_item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=cart_item.product,
#                 quantity=cart_item.quantity,
#                 price=cart_item.product.price
#             )

#         cart_items.delete()

#         return redirect('process_payment')

#     return render(request, 'checkout.html')

from django.shortcuts import render, redirect
from .models import Address

@login_required
def checkout(request):
    # ดึงที่อยู่ทั้งหมดของผู้ใช้
    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        if address_id:  # หากมีการเลือกที่อยู่ที่มีอยู่
            address = Address.objects.get(id=address_id)
        else:  # หากไม่ได้เลือกที่อยู่ที่มีอยู่ ให้สร้างที่อยู่ใหม่
            address_line1 = request.POST.get('address_line1')
            address_line2 = request.POST.get('address_line2', '')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postal_code = request.POST.get('postal_code')
            phone_number = request.POST.get('phone_number')

            address = Address.objects.create(
                user=request.user,
                address_line1=address_line1,
                address_line2=address_line2,
                city=city,
                state=state,
                postal_code=postal_code,
                phone_number=phone_number
            )

        customer, created = Customer.objects.get_or_create(user=request.user)
        customer.default_address = address 
        customer.save() 

        order = Order.objects.create(customer=customer, address=address)

        cart_items = CartItem.objects.filter(order__customer=request.user.customer)

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        cart_items.delete()

        return redirect('process_payment')

    return render(request, 'checkout.html', {'addresses': addresses})  # ส่งข้อมูลที่อยู่ไปยัง template





def calculate_total(cart_items):
    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity
    return total

def payment_success(request):
    return render(request, 'payment_success.html') 

@login_required
def process_payment(request):
    if request.method == 'POST':
        customer = request.user.customer

        if not customer.default_address:
            return redirect('checkout') 

        order_items = OrderItem.objects.filter(order__customer=customer)

        for item in order_items:
            product = item.product
            if product.stock_quantity >= item.quantity:
                product.stock_quantity -= item.quantity
                product.save()
            else:
                # จัดการกรณีที่ stock ไม่พอ
                pass


        order = order_items.first().order  
        order.complete = True
        order.save()

        return redirect('payment_success')

    return render(request, 'process_payment.html')


@login_required
def cart_view(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer, complete=False)

    if orders.exists():
        order = orders.first() 
    else:
        order = None 

    return render(request, 'cart.html', {'order': order})

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)  # เพิ่มบรรทัดนี้

        if user_form.is_valid():
            new_username = user_form.cleaned_data['username']
            new_email = user_form.cleaned_data['email']

            if User.objects.exclude(pk=request.user.pk).filter(username=new_username).exists():
                user_form.add_error('username', 'ชื่อผู้ใช้นี้ถูกใช้แล้ว')

            if User.objects.exclude(pk=request.user.pk).filter(email=new_email).exists():
                user_form.add_error('email', 'อีเมลนี้ถูกใช้แล้ว')

            if not user_form.errors:
                user_form.save()
                messages.success(request, 'บันทึกข้อมูลสำเร็จ')

        if password_form.is_valid():  # เช็คความถูกต้องของฟอร์มเปลี่ยนรหัสผ่าน
            user = password_form.save()
            update_session_auth_hash(request, user)  # อัปเดต session ของผู้ใช้เพื่อไม่ให้ต้องล็อกเอาท์
            messages.success(request, 'เปลี่ยนรหัสผ่านสำเร็จ')  # แสดงข้อความสำเร็จ

    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)  # แสดงฟอร์มเปลี่ยนรหัสผ่าน

    context = {
        'user_form': user_form,
        'password_form': password_form,  # เพิ่มฟอร์มเปลี่ยนรหัสผ่านใน context
    }
    return render(request, 'update_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # อัปเดตรหัสผ่านใน session
            messages.success(request, 'รหัสผ่านของคุณถูกเปลี่ยนสำเร็จ!')
            return redirect('change_password')  # เปลี่ยนเป็น URL ที่คุณต้องการ
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'change_password.html', context)
