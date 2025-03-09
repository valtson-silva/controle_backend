from django.contrib import admin
from django.urls import path, include
from user.views import UserLoginView, UserLogoutView, UserRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("modelo_de_carro/", include("exhausts.car_model_urls")),
    path("escapamento/", include("exhausts.exhaust_urls")),
    path("escapamento/modelo/", include("exhausts.exhausts_car_models_urls")),
    path("produtos/", include("miscellaneous_products.urls")),
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
