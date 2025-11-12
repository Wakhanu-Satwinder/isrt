from django.shortcuts import render
from .serializers import RequestSerializer,UserSerializer,CustomRegisterSerializer,LoginUser
from .models import Request,CustomUser
from rest_framework import viewsets

from django.views.decorators.csrf import ensure_csrf_cookie


from .permissions import IsAdminOrReadOnly,IsOwner

from urllib import request
from reflex import serializer
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model,logout
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import mixins
from rest_framework.mixins import RetrieveModelMixin,ListModelMixin,CreateModelMixin
from rest_framework.generics import GenericAPIView

from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken,BlacklistedToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.authentication import SessionAuthentication,BasicAuthentication

from knox.models import AuthToken
from knox.auth import TokenAuthentication
from knox.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.http import HttpResponse,JsonResponse
from django.core.mail import send_mail,EmailMessage,get_connection
from rest_framework import status
from django.conf import settings
import mailtrap as mt
from mailtrap import MailtrapClient
from mailtrap import Mail
from django.http import JsonResponse
import smtplib
from email.message import EmailMessage
from rest_framework.decorators import api_view
# Create your views here.


class LoginView(APIView):

    def post(self,request):
        serializer=LoginUser(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Requeest(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,pk):
        serializer=RequestSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            #self.perform_create(serializer)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self,request,pk):
        try:
            request_obj=Request.objects.get(pk=pk)
            if request_obj.user==request.user:
                serializer=RequestSerializer(request_obj,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response({'error':'you are not the author of this request'},status=status.HTTP_403_FORBIDDEN)
        except Request.DoesNotExist:
            return Response({'error':'request not found'},status=status.HTTP_404_NOT_FOUND)
                


    '''class ResolveRequestView(APIView):
     permission_classes=[IsAuthenticated]'''       
    '''request_obj.status=Request.RESOLVED
            request_obj.save()
            return Response({'status':'Request Marked as resolved'})
        except Request.DoesNotExist:
            return Response({'error':'Request Not Found'},status=status.HTTP_404_NOT_FOUND)'''




class GenericUserAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class=UserSerializer
    queryset=CustomUser.objects.all()
    lookup_field='id'

    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.List(request)
    def post(self,request):
        return self.create(request)
    def put(self,request,id=None):
        return self.update(request,id)
    def delete(self,request,id):
        return self.destroy(request,id)

class UserList(generics.ListAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]

class UserDetail(generics.RetrieveAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]




class RegisterView(generics.CreateAPIView):
      queryset=CustomUser.objects.all()
      serializer_class=CustomRegisterSerializer
      
      def create(self,request,*args,**kwargs):
          serializer=self.get_serializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          user=serializer.save(request=request)
          refresh=RefreshToken.for_user(user)
          return Response({
              "user":{"email":user.email},
              "refresh":str(refresh),
              "access":str(refresh.access_token),
          },status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    #authentication_classes=[TokenAuthentication]
    #permission_classes=[IsAuthenticated]
    def post(self,request):
        logout(request)
        return Response({"message":"successfully logged out"},status=status.HTTP_200_OK)
        
    
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    


class CustomAuthToken(ObtainAuthToken):
    serializer_class=UserSerializer

    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'email':user.email,
        })


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token=super().get_token(user)
        return token 
    
    def validate(self,attrs):
        data=super().validate(attrs)
        data['email']=self.user.email
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer


class CustomTokenBlacklistHandler:
    def blacklist_token(self,token):
        try:
            outstanding_token=OutstandingToken.objects.get(token=token)
            BlacklistedToken.objects.create(token=outstanding_token)
        except OutstandingToken.DoesNotExist:
            pass
        except Exception as e:
            print(f"Error blacklisting token:{e}")
            
    

    
    


'''def send_email(request):
   subject='enter subject of email'
   message=f'write your text here'
   email_from='settings.EMAIL_HOST_USER'
   recipient=['satwinder.wakhanu@gmail.com']
   res=send_mail(subject,message,email_from ,recipient)

   return HttpResponse('%s'%res)'''


class send_email(APIView):
  def post(self,request):
      subject=request.data['subject']
      message=request.data['message']
      from_email=request.data['from_email']
      to_email=request.data['to_email']

      try:
          send_mail(
              subject,
              message,
              from_email,
              [to_email],
              fail_silently=False
          )
          return Response({'message':'Email sent successfully'})
      except Exception as e:
          return Response({'error':str(e)},status=500)
