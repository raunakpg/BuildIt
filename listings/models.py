from django.contrib.auth.models import AbstractUser
from django.db import models

class ListItem(models.Model):
    CATEGORIES = [
        ('House', 'House'),
        ('Building', 'Building'),
        ('NONE', 'NONE')
    ]
    active = models.BooleanField()
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    reserve_price = models.PositiveIntegerField() 
    current_price = models.PositiveIntegerField()
    contact=models.CharField(max_length=15, default='000000')
    image = models.ImageField(blank=True, null=True, upload_to = '%Y/%m/%d/')
    category = models.CharField(max_length=50, choices=CATEGORIES, default='NONE')
    creator = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)  
    
    

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)  # Call the "real" delete() method.
    
    def __str__(self):
        return f"{self.title}: {self.category}, reserve price Rs.{self.reserve_price}"

class User(AbstractUser):
    user_watchlist = models.ManyToManyField(ListItem, blank=True, related_name="watchlist")
    prediction=models.CharField(max_length=15, default='genuine')
    GST=models.CharField(max_length=15, default='000000000000000')

class Comment(models.Model): 
    item = models.ForeignKey(ListItem, on_delete=models.CASCADE, related_name="listing")           #one-to-many relationship
    which_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")       #one-to-many relationship
    date = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=500)


    def __str__(self):
        return f"{self.which_user} commented on {self.item}"
        
class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person")              #one-to-many relationship
    item = models.ForeignKey(ListItem, on_delete=models.CASCADE, related_name="item")              #one-to-many relationship
    bid = models.PositiveIntegerField() 

    def __str__(self):
        return f"{self.bidder} bid Rs.{self.bid} on {self.item}"


#payment

class Order(models.Model):
    email = models.EmailField(max_length=254)
    paid = models.BooleanField(default="False")
    amount = models.IntegerField(default=0)
    description = models.CharField(default=None,max_length=800)
    def __str__(self):
        return self.email


