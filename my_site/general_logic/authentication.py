"""
бэкэнда аутентификации.
"""
from typing import Optional

from django.contrib.auth.models import User, AbstractUser


class EmailAuthBackend(object):
    """ Выполняет аутентификацию пользователя по e-mail. """

    def authenticate(self, request, user: Optional[str] = None, password: Optional[str] = None) -> Optional[User]:
        """Возвращает пользователя, соответствующего указанным электронной почте и паролю

        :param request:
        :param email:
        :param password:
        :return:
            user/none
        """
        try:
            user = User.objects.get(email=user)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None