from django.contrib import admin
from .models import Request,CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

#from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    '''CreationForm=CustomUserCreationForm
    ChangeForm= CustomUserChangeForm''' 

    model=CustomUser
    list_display=('email','full_name','is_staff','is_active','date_joined')
    list_filter=('is_staff','is_active',)
    fieldsets=(
        (None,{'fields':('email','full_name','password','date_joined')}),
        ('Permissions',{'fields':('is_staff','is_active')}),
    )
    add_fieldsets=(
        (None,{'classes':('wide,'),'fields':('email','full_name','password1','password2')}),
    )
    search_fields=('email','full_name')
    ordering=('email',)


User = get_user_model()
'''class ContactAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'subject', 'review','created_on')
    list_filter = ['created_on']
    search_fields = ['username']'''

class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'issue_category', 'description','created_on')
    list_filter = ['issue_category']
    search_fields = ['name', 'department', 'issue_category', 'description','created_on']
   
#admin.site.register(User)
#admin.site.register(Contact,ContactAdmin)
admin.site.register(Request,RequestAdmin)

admin.site.register(CustomUser,CustomUserAdmin)
# Register your models here.

