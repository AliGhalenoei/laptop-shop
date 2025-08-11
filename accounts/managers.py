from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self , phone , email , username , password):

        if not phone:
            raise ValueError("Errore Phone")
        if not email:
            raise ValueError("Errore email")
        if not username:
            raise ValueError("Errore username")
        
        user = self.model(
            phone = phone,
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)

        user.save(using = self._db)
        return user
    
    def create_superuser(self , phone , email , username , password):
        user = self.create_user(phone , email , username , password)
        user.is_admin = True
        user.is_superuser = True

        user.save(using = self._db)
        return user
        
