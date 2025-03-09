from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
