qfrom django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('signout/', views.signout, name='signout'),
    path('create_post/', views.create_post, name='create_post'),  # Create post URL
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),  # Edit post URL
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),  # Delete post URL
    path('contact-us/', views.contact_us, name='contact_us'),
]
