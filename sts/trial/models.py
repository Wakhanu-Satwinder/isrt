from django.db import models

# Create your models here.
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.conf import settings
# Create your models here.


class CustomUser(AbstractBaseUser,PermissionsMixin):
    username=None
    full_name=models.CharField(max_length=150,unique=True,)
    email=models.EmailField(unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    date_joined=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['full_name']

    objects=CustomUserManager()

    groups=models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        related_query_name='customuser',
        blank=True,
        help_text='the groups user belongs to',
        verbose_name='groups', )
    

    user_permissions=models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        related_query_name='customuser',
        blank=True,
        help_text='specific permissions for this user',
        verbose_name='user permissions',
    )
 

    def __str__(self):
        return self.full_name
    
    
class Request(models.Model): 
    PENDING='pending'
    RESOLVED='resolved'
    STATUS_CHOICES=[
        ( PENDING,'pending'),
        (RESOLVED,'resolved')
    ]

    request_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    department=models.CharField(max_length=20)
    issue_category=models.CharField(max_length=12)
    description=models.CharField(max_length=255)
    created_on=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10,default='pending')

