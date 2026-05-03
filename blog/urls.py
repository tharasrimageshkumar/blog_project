from django.urls import path
from .views import home, create_post, edit_post, delete_post, user_login, user_logout, signup

urlpatterns = [
    path('', home),
    path('create/', create_post),
    path('edit/<int:id>/', edit_post),
    path('delete/<int:id>/', delete_post),
    path('login/', user_login),
    path('logout/', user_logout),
    path('signup/', signup),
]