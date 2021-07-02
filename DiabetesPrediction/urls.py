from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = (
    path('admin/', admin.site.urls),
    path("", views.home, name="Home"),
    path("register", views.register,name="register"),
    path("login", views.login, name="login"),
    path("home", views.home,name="Home"),
    path("register", views.register, name="register"),
    path("contact", views.contactView, name="contact"),
    path('success', views.successView, name='success'),
    path('checkdisease', views.checkdisease, name="checkdisease"),
  #  path("predict/",views.predict),
   # path("predict/result",views.result),
   # path('heart', views.heart, name='heart'),
    path("logout", views.logout, name="logout"),


)
