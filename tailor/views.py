from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
import re

def home(request):
    return render(request, 'home.html')

def About_Us(request):
    return render(request, 'AboutUs.html')

def register(request):
    if request.method == "POST":
        CustomerPassword = request.POST.get("CustomerPassword")
        ConfirmPassword = request.POST.get("ConfirmPassword")
        if CustomerPassword == ConfirmPassword:
            FirstName = request.POST.get('FirstName')
            LastName = request.POST.get("LastName")
            username = request.POST.get("username")
            PhoneNumber = request.POST.get("PhoneNumber")
            CustomerEmail = request.POST.get("CustomerEmail")   
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_pattern.match(CustomerEmail):
                messages.error(request, "Please enter a valid email address")
                return render(request, 'register.html')
            phone_pattern = re.compile(r'^\d{10}$')  
            if not phone_pattern.match(PhoneNumber):
                messages.error(request, "Please enter a valid phone number")
                return render(request, 'register.html')

            customer = Customer.objects.create(FirstName=FirstName, LastName=LastName, username=username, PhoneNumber=PhoneNumber, CustomerEmail=CustomerEmail, CustomerPassword=CustomerPassword, ConfirmPassword=ConfirmPassword)
            messages.success(request, "User profile has been registered successfully! Please login to continue")
            return redirect('user_login')
        else:
            messages.error(request, "Passwords do not match! Please try again")
    
    return render(request, 'register.html')


def user_login(request):
    if request.session.has_key('username'):
        return redirect('body')
    else:
        if request.method=='POST':
            Username=request.POST.get("username_or_email")
            Email = request.POST.get("username_or_email")
            Password=request.POST.get("CustomerPassword")
            session = Customer.objects.filter((Q(username=Username)|Q(CustomerEmail=Email)),CustomerPassword=Password)
            if session.exists():  
                user = session.first()  
                request.session['username'] = user.username 
                request.session['user_id'] = user.id 
                return redirect('home') 
            else:
                messages.warning(request,'Invalid Username or Password! Please Try Again')

    return render(request, 'login.html')

def user_logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('user_login')

def edit_users(request, id):
    useredit = Customer.objects.get(id=id)
    password = useredit.ConfirmPassword

    if request.method == 'POST':
        OldPassword = request.POST.get("OldPassword")
        
        if OldPassword != password:
            messages.error(request, 'Invalid old Password! Please Try Again')
        else:
            FirstName = request.POST.get("FirstName")
            LastName = request.POST.get("LastName")
            username = request.POST.get("username")
            PhoneNumber = request.POST.get("PhoneNumber")
            CustomerEmail = request.POST.get("CustomerEmail")
            CustomerPassword = request.POST.get("CustomerPassword")
            ConfirmPassword = request.POST.get("ConfirmPassword")
            
            if CustomerPassword == ConfirmPassword:
                # Update user fields and save
                useredit.FirstName = FirstName
                useredit.LastName = LastName
                useredit.username = username
                useredit.PhoneNumber = PhoneNumber
                useredit.CustomerEmail = CustomerEmail
                useredit.CustomerPassword = CustomerPassword
                useredit.ConfirmPassword = ConfirmPassword
                useredit.save()
                
                messages.success(request, "User profile has been updated successfully! Please to continue shopping")
                return redirect('home')
            else:
                messages.error(request, "The password and confirmation do not match")

    return render(request, 'profile.html', {'useredit': useredit})

def product(request):
    data = Products.objects.all()
    context = {
        'data':data
    }
    return render(request, 'product.html',context)

def products_by_category(request, category):
    products = Products.objects.filter(category=category)
    # Enumerate the products to get both index and product object
    products_with_index = [(index, product) for index, product in enumerate(products)]
    context = {
        'products_with_index': products_with_index,
        'category': category
    }
    return render(request, 'filterproduct.html', context)

def cart(request):
    if request.session.has_key('username'):
        ID = request.session['user_id']         
        cart_items = Cart.objects.filter(customer=int(ID))
        context={
            'cart_items':cart_items       
                }
        return render(request, 'cart.html',context)
    
    else:
        return redirect('user_login')
    
    

def add_to_cart(request, product_id):
    if request.session.has_key('username'):
        user_id=request.session['user_id']
        customer = Customer.objects.get(id=int(user_id))    
        filtered_products = Products.objects.filter(id=product_id).get(id=product_id)    
        if filtered_products:
            cart_item, created = Cart.objects.get_or_create(Product=filtered_products,customer=customer)
            cart_item.save()
            return redirect('cart')
    else:
        return redirect('user_login')

def remove_from_cart(request, item_id):
    if request.session.has_key('username'):
        cart_item = Cart.objects.get(id=item_id)
        cart_item.delete()
        return redirect('cart')

def size_chart_form(request):
    if request.method == "POST":
        fabric = request.POST.get("fabric")
        colour = request.POST.get("colour")
        neck = request.POST.get("neck")
        overbust = request.POST.get("overbust")
        bust = request.POST.get("bust")        
        waist = request.POST.get("waist") 
        hips =  request.POST.get("hips")
        neckToAboveKnee = request.POST.get("neckToAboveKnee")
        neckToHeel =  request.POST.get("neckToHeel")
        armLength =  request.POST.get("armLength")
        aboveKneeToAnkle =  request.POST.get("aboveKneeToAnkle")
        shoulderSeam =  request.POST.get("shoulderSeam")
        armHole =  request.POST.get("armHole")
        bicep = request.POST.get("bicep")
        foreArm =  request.POST.get("foreArm")
        wrist =  request.POST.get("wrist")
        vNeckCut =  request.POST.get("vNeckCut")
        shoulderToWaist =  request.POST.get("shoulderToWaist")
        waistToAboveKnee =  request.POST.get("waistToAboveKnee")
        productdescription =  request.POST.get("productdescription")
        user_id=request.session['user_id'] 
        userId = Customer.objects.get(id=int(user_id))
        sizechart = Sizechart.objects.create(customer=userId,
                    fabric=fabric,colour=colour,neck=neck,overbust=overbust,
                    bust=bust,waist=waist,hips=hips,neckToAboveKnee=neckToAboveKnee,
                    neckToHeel=neckToHeel,armLength=armLength,aboveKneeToAnkle=aboveKneeToAnkle,
                    shoulderSeam=shoulderSeam,armHole=armHole,bicep=bicep,foreArm=foreArm,wrist=wrist,
                    vNeckCut=vNeckCut,shoulderToWaist=shoulderToWaist,waistToAboveKnee=waistToAboveKnee,
                    productdescription=productdescription)
        if sizechart:
            messages.success(request,"Your descriptions are saved Successfully! now your order will be verified and confirm later. Please continue to shopping")
            return redirect('product')
        else:
            messages.warning(request,"Something went wrong please try again later!!!")
    

    return render(request, 'sizechartform.html')




