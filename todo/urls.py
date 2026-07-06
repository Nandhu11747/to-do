from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("add/", views.add_task, name="add_task"),

    path("edit/<int:task_id>/", views.edit_task, name="edit_task"),

    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
    
    path("complete/<int:task_id>/", views.complete_task, name="complete_task"),

    #Authentication URLs

    path("signup/", views.signup, name="signup"),

    path("login/", views.login_view, name="login"),
    
    path("logout/", views.logout_view, name="logout"),


    path("create-admin/", views.create_admin, name="create_admin"),
]   
