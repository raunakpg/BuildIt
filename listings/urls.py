from django.urls import path

from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("index", views.index, name="index"),
    path("sellerIndex", views.sellerIndex, name="sellerIndex"),
    path("login", views.login_view, name="login"),
    path("loginSeller", views.loginSeller, name="loginSeller"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("registerSeller", views.registerSeller, name="registerSeller"),
    path('about/', views.about, name="about"),
    path('inactive/', views.inactive, name="inactive"),
    path('all/', views.all, name="all"),
    path('sellerAll/', views.sellerAll, name="sellerAll"),
    path('close/<int:item_id>', views.close, name="close"),
    path('checkcurr/<int:item_id>', views.checkcurr, name="checkcurr"),
    path('new/', views.new, name="new"),
    path('item/<int:item_id>', views.item, name="item"),
    path('sellerItem/<int:item_id>', views.sellerItem, name="sellerItem"),
    path('placebid/<int:item_id>', views.bid, name="bid"),
    path('comment/<int:item_id>', views.comment, name="comment"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('categories/', views.categories, name="categories"),
    path('categories/<str:category>', views.category, name="category"),
    path('my_listings/', views.my_listings, name="my_listings"),
    path('wins/', views.wins, name="wins")
]
