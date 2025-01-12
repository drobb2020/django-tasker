from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("task_create/", views.task_create, name="task-create"),
    path("task_detail/<int:pk>/", views.task_detail, name="task-detail"),
    path("task_update/<int:pk>/", views.task_update, name="task-update"),
    path("task_delete/<int:pk>/", views.task_delete, name="task-delete"),
    path("register/", views.register, name="register"),
    path("my_login/", views.my_login, name="my-login"),
    path("my_logout/", views.my_logout, name="my-logout"),
    path("profile/", views.profile, name="profile"),
    path("profile_update/", views.profile_update, name="profile-update"),
    path("profile_delete/", views.profile_delete, name="profile-delete"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
