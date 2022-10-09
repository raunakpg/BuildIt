from django.contrib import admin
from .models import *

class ListItemAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "category", "reserve_price", "current_price", "creator", "date")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("item", "which_user", "comment")

class BidAdmin(admin.ModelAdmin):
    list_display = ("bidder", "item", "bid")

# Register your models here.
admin.site.register(User)
admin.site.register(ListItem, ListItemAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)