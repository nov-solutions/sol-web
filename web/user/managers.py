from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_superuser(self, email, password):
        user = self.model(email=email, is_staff=True, is_superuser=True)
        user.set_password(password)
        user.save(using=self._db)
        return user
