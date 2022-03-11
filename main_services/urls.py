"""main_services URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from service.views import display_service_page
import service.views as service_views
from django.contrib.auth import views as auth_views
import complaint_management.views as complaint_management_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', display_service_page, name='home_page'),
    path('about/', service_views.display_about_page, name='about_page'),
    path('services/', service_views.display_services_page, name='service_page'),
    path('team/', service_views.display_team_page, name='team_page'),
    path('success/', service_views.save_customer_details, name='success_page'),
    path('complaint_info_login/', auth_views.LoginView.as_view(template_name = 'complaint_management/login.html', redirect_authenticated_user=True), name='complaint_info_login_page'),
    path('account_logout/', complaint_management_views.logout, name='account_logout'),
    path('complaint_detail_view/', complaint_management_views.view_complaints, name='view_complaints_page'),
    path('complaint_info_login_admin/', complaint_management_views.login_request_admin, name='complaint_info_login_admin_page'),
    path('complaint_detail_view_admin/', complaint_management_views.view_complaints_admin, name='view_complaints_admin_page'),
    path('account_admin_logout/', complaint_management_views.admin_logout, name='account_admin_logout_page'),
    path('update_complaints/<str:pk>/', complaint_management_views.update_complaint_details, name='update_complaints_page'),
    path('download_csv', complaint_management_views.export_csv, name='download_csv_page')
]
