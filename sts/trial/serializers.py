from .models import Request,CustomUser
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import CurrentUserDefault

from django.conf import settings
from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from django.contrib.auth import authenticate,get_user_model


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class CustomRegisterSerializer(RegisterSerializer):
    username=None
    full_name=serializers.CharField(max_length=15)

    class Meta:
        model=CustomUser
        fields=['email','full_name','password1','password2']
        
    def get_cleaned_data(self):
        return{
            'email':self.validated_data.get('email',''),
            'full_name':self.validated_data.get('full_name',''),
            'password1':self.validated_data.get('password1',''),
            'password2':self.validated_data.get('password2',''),
            
        }
 
    #@transaction.atomic
    def save(self,request):
        adapter=get_adapter()
        user=adapter.new_user(request)
        self.cleaned_data=self.get_cleaned_data()
        user.full_name=self.cleaned_data.get('full_name')
        user.email=self.cleaned_data.get('email') 
        user.save()
        adapter.save_user(request,user,self)
        return user
    




class UserSerializer(ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','email','full_name','password']
        extra_kwargs={'password':{'write_only':True}}
        

        def create(self,validated_data):
            user=CustomUser.object.create_user(**validated_data)
            return user
        
        def update(self,instance,validated_data):
            password=validated_data.pop('password',None)
            if password:
                instance.set.password(password)
            return super().update(instance,validated_data)


class RequestSerializer(ModelSerializer):
   user=serializers.HiddenField(default=serializers.CurrentUserDefault())
   class Meta:
      model=Request
      fields=['name','department','issue_category','description','user','status'] 
     
   def create(self,validated_data):
      validated_data['user']=self.context['request'].user
      return Request.objects.create(**validated_data)  
   

   def update(self,instance,validated_data):
       if 'status' in validated_data and validated_data['status']:
           validated_data['status']=Request.RESOLVED
       return super().update(instance,validated_data) 


class LoginUser(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()

    '''ADDITIONAL FOR JWT'''
    def validate(self, data):
        email=data.get('email')
        password=data.get('password')

        if email and password:
            user=CustomUser.objects.filter(email=email).first()
            if user and user.check_password(password):
                refresh=RefreshToken.for_user(user)
                data['refresh']=str(refresh)
                data['access']=str(refresh.access_token)
                return data
            else:
                raise serializers.ValidationError('invalid email or password')
        else:
            raise serializers.ValidationError('Email and password are required')


