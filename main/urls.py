from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('planner/', views.planner, name='planner'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle-task/<int:task_id>/', views.toggle_complete, name='toggle_task'),
    path('habits/', views.habits, name='habits'),
    path('delete-habit/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('dashboard/spending/', views.spending_dashboard, name='spending_dashboard'),
    path('smart-suggestions/', views.smart_suggestions, name='smart_suggestions'),
    path('add-to-planner/<int:product_id>/', views.add_to_planner, name='add_to_planner'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),


]
