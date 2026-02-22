"""
URL configuration for study project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.dashbord_open, name="dashbord"),
    path("order_input/",views.Order_input.as_view(), name="order_input"),
    path("item_register", views.Item_register.as_view(), name="item_register"),
    path("shipping_list/",views.Shipping_list.as_view(), name="shipping_list"),
    path("process_list/",views.Process_list.as_view(),name="process_list"),
    path("progress_input/",views.progress_input.as_view(),name="progress_input"),
]
