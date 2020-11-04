from django.contrib.auth.base_user import BaseUserManager


class LabPersonManager(BaseUserManager):
   
    def create_user(self, name, lab_email, password, **extra_fields):
        
        user = self.model(
            name=name,
            lab_email=lab_email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, lab_email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(name, lab_email, password, **extra_fields)
