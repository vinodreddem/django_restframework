from django.db import models 
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
    """Manager for User Profile """
    def create_user(self,email,name, password=None):
        """Create New User Profile """
        if not email:
            raise ValueError('User Must have an Email')
        email = self.normalize_email(email)
        user = self.model(email = email, name = name)
        
        user.set_password(password)
        user.save(using = self._db)
        
        return user
        
        """ 
        Django default managers use using parameter to define which database underlying the manager should use for operation.
        This will optionally use. This is used in case you have multiple databases by which you define which database
        you need to use for operation.

        An example user.save(using=self._db) usually defined as "default" from your database configuration in settings.py.
        

        Behind the scene self._db set as None. If user.save(using=None), then it will use default database.

        For example, your database configuration is like

        DATABASES = {
            'default': {
                'NAME': 'app_data',
                'ENGINE': 'django.db.backends.postgresql',
                'USER': 'postgres_user',
                'PASSWORD': '****'
            },
            'new_users': {
                'NAME': 'user_data',
                'ENGINE': 'django.db.backends.mysql',
                'USER': 'mysql_user',
                'PASSWORD': '****'
            }
        }
        Then if you want to use default database then use user.save(using=self._db) If you want to use new_users database then use user.save(using="new_users")
        
        """ 
    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        self.is_superuser = True #PermissionsMixin in this class we have defined this variable
        self.is_staff = True
        
        user.save(using=self._db)
        
        return user
        
        
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for User in System"""
    email = models.EmailField(max_length =255, unique = True)
    name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    
    objects = UserProfileManager()
    
    # USERNAME_FIELD: A string describing the name of the field on the user model that is used as the unique identifier. 
    # This will usually be a username of some kind, but it can also be an email address,
    # or any other unique identifier. The field must be unique (i.e., have unique=True set in its definition), 
    # unless you use a custom authentication backend that can support non-unique usernames.
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ Retrieve Full Name User Name """
        return self.name
    
    def get_short_name(Self):
        """ Retrieve the Short Name"""
        return self.name
    
    def __str__(self):
        return self.email