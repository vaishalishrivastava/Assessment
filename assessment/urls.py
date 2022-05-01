"""assessment URL Configuration

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
from home_price import views as HV
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("import_csv_data/", HV.import_csv_data, name="import_csv_data"),
    path("register_user/", HV.register_user, name="register_user"),
    path("budget_homes/", HV.budget_homes, name="budget_homes"),
    path("sqft_homes/", HV.sqft_homes, name="sqft_homes"),
    path("age_homes/", HV.age_homes, name="age_homes"),
    path("predict_std_prices/", HV.predict_std_prices, name="predict_std_prices")
]
