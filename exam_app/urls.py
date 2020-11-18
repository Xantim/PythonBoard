from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('quotes', views.quotes),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('add_quote', views.add_quote),
    path('quotes/<int:quote_id>/delete', views.delete_quote),
    path('user/<int:username_id>', views.user),
    path('user/<int:quote_posted_by_id', views.showuser),
    path('account/<int:username_id>', views.account),
    path('account/<int:username_id>/edit', views.account_edit),

]