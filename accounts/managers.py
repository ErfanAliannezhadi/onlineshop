from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,email,phone_number,password,name):
        if not email:
            raise ValueError('user must have Email')
        if not phone_number:
            raise ValueError('user must have Phone Number')
        if not name:
            raise ValueError('user must have Name')
        user = self.model(email=self.normalize_email(email),phone_number=phone_number,name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,phone_number,password,name):
        user = self.create_user(email,phone_number,password,name)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
