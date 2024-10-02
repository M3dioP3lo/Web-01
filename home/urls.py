from django.urls import path
from . import views
from .views import UpdatePostView
from .views import login_view
from django.contrib.auth import views as auth_views

urlpatterns = [
#blogs
    path("", views.blogs, name="blog"),
    path("blog/<str:slug>/", views.blogs_comments, name="blogs_comments"),
    path("add_blogs/", views.add_blogs, name="add_blogs"),
    path("edit_blog_post/<str:slug>/", UpdatePostView.as_view(), name="edit_blog_post"),
    path("delete_blog_post/<str:slug>/", views.delete_blog_post, name="delete_blog_post"),
    path("search/", views.search, name="search"),

    
#Perfil
    path("profile/", views.profile_view, name="profile"),#Antes ----> path("profile/", views.Profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("user_profile/<int:myid>/", views.user_profile, name="user_profile"),
    
#Autenticación de usuario
    path("register/", views.register, name="register"),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Ruta para el cierre de sesión
    path('logout_redirect/', views.logout_and_redirect, name='logout_redirect'), #Antes --->path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]