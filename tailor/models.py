from django.db import models

class Customer(models.Model):
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50, blank=True)  
    username = models.CharField(max_length=128, unique=True)
    PhoneNumber = models.CharField(max_length=10)
    CustomerEmail = models.EmailField()
    CustomerPassword = models.CharField(max_length=50)
    ConfirmPassword = models.CharField(max_length=50)
    def __str__(self):
        return self.username

class Products(models.Model):
    category = models.CharField(max_length=50, choices=(
        ('Blouse', 'Blouse'),
        ('Dress', 'Dress'),
        ('Jacket','Jacket'),
        ('Jumpsuit','Jumpsuit'),
        ('Kurta-Kurti','Kurta-Kurti'),
        ('Lehenga','Lehenga'),
        ('Salwar-Suit','Salwar-Suit'),
        ('Ready-To-wear-Saree','Ready-To-wear-Saree'),
        ('Shirt','Shirt'),
        ('Skirt','Skirt'),
        ('Top','Top'),
        ('Trouser','Trouser'),
    ))
    ProductName = models.CharField(max_length=100)
    ProductDetails = models.TextField()    
    img1 = models.FileField(upload_to='products/')

    def __str__(self):
        return f"{self.ProductName} - {self.category}"


class Sizechart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)    
    fabric = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    neck = models.CharField(max_length=50,null=True,blank=True)
    overbust = models.CharField(max_length=50,null=True,blank=True)
    bust = models.CharField(max_length=50,null=True,blank=True)
    waist = models.CharField(max_length=50,null=True,blank=True)
    hips = models.CharField(max_length=50,null=True,blank=True)    
    neckToAboveKnee = models.CharField(max_length=50,null=True,blank=True)
    neckToHeel = models.CharField(max_length=50,null=True,blank=True)
    armLength = models.CharField(max_length=50,null=True,blank=True)
    aboveKneeToAnkle = models.CharField(max_length=50,null=True,blank=True)
    shoulderSeam = models.CharField(max_length=50,null=True,blank=True)
    armHole = models.CharField(max_length=50,null=True,blank=True)
    bicep = models.CharField(max_length=50,null=True,blank=True)
    foreArm = models.CharField(max_length=50,null=True,blank=True)
    wrist = models.CharField(max_length=50,null=True,blank=True)
    vNeckCut = models.CharField(max_length=50,null=True,blank=True)
    shoulderToWaist = models.CharField(max_length=50,null=True,blank=True)
    waistToAboveKnee = models.CharField(max_length=50,null=True,blank=True)
    productdescription = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.customer.username

class Cart(models.Model):
    Product=models.ForeignKey(Products, on_delete=models.CASCADE)    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    size=models.ForeignKey(Sizechart,on_delete=models.CASCADE,null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True,default='Pending')
    

    def __str__(self):  
        return f"{self.Product.ProductName} - {self.customer.username}"     
