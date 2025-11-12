from django import views
from django.urls import path,include,URLPattern
from rest_framework import routers
from .views import LogoutView,MyTokenObtainPairView,LoginView,Requeest,send_email
from . import views
from dj_rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView

#router=routers.DefaultRouter()
#router.register('request',views.Requeest)

urlpatterns=[
    #path('',include(router.urls)),
    path('token/',views.TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
     path('register/',views.RegisterView.as_view(),name='register'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),
    path('logout/',LogoutView.as_view(),name='custom_logout'),
    
    path('login/',views.LoginView.as_view(),name='login'),
    path('request/',views.Requeest.as_view(),name='request'),
    path('request/<int:pk>/',views.Requeest.as_view(),name='resolve_request'),

    path('send-email/',views.send_email.as_view(), name='send_email'),
]
    


#url_patterns+=router.urls