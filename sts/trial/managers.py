from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,email,full_name,password=None):

        if not full_name:
            raise ValueError('users must have a Name')
        if not email:
            raise ValueError('users must have an email address')
        

        user=self.model( full_name=full_name,
            email=self.normalize_email(email))
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,full_name,email,password=None):
        user=self.create_user(full_name=full_name,email=email,password=password)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
