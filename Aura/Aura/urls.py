"""Aura URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path , include
from dataLoggingApi import views
from DocManager import views as DocViews

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('dem/' , include('dataLoggingApi.urls')) ,
    path('datalog/', views.DemDailyData),
    path('edit/<int:id>', views.edit_records, name="formdata"),  # edit dem data
    path('', views.Login),  # login page
    path('Logout/', views.Logout),  # logout
    path('Jarvis/', views.Jarvis_Headsup),  # Jarvis DashBoard
    path('Dem/Main/', views.DemMainPage, name="main"),  # landing page
    path('transactionAnalysis/', views.DemMainPage),
    path('docmanager/', DocViews.save_doc_data),
    path('customtransaction/', views.MonthTable),  # all records table

]
