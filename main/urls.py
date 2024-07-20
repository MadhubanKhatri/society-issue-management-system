from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('member/', views.member_loggedin, name='member_loggedin'),
    path('logout/<str:flag>/', views.logout, name='logout'),
    path('create_issue/', views.create_issue, name='create_issue'),
    path('admin_panel_login/', views.admin_panel_login, name='admin_panel_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_issue/<int:issue_id>/', views.edit_issue, name='edit_issue'),
]