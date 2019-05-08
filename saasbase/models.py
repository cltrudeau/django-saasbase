from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from awl.absmodels import TimeTrackModel

from .contacts import PersonalInfo, PhoneInfo, AddressInfo, BirthDayInfo

# ============================================================================
# Login -- custom user definition for logging in with e-mail address

class LoginManager(BaseUserManager):
    def _user_factory(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('email address is required')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        return user

    def create_user(self, email, password=None, **kwargs):
        """Creates a user using Hexa's custom user agent.  

        :param email: required, this is the unique key for users in Hexa
        :param password: [optional] the password for the user (no password
            will cause the account to be disabled
        :param **kwargs: A CoreUser is also a people.models.Person, any valid
            field in Person can also be passed in 

        :returns: the created user object
        """

        user = self._user_factory(email, password, **kwargs)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        """Creates an admin account using Hexa's custom user agent.

        :param email: required, this is the unique key for users in Hexa
        :param password: required for super users
        :param **kwargs: A CoreUser is also a people.models.Person, any valid
            field in Person can also be passed in 

        :returns: the created super user object
        """
        if not password:
            raise ValueError('password is required')

        user = self._user_factory(email, password, **kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Login(AbstractBaseUser, TimeTrackModel, PersonalInfo, PhoneInfo, 
        BirthDayInfo):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = LoginManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        name = ''

        if self.first_name:
            name = self.first_name + ' '

        if self.last_name:
            name = name + self.last_name + ' '

        if self.first_name or self.last_name:
            return name + '<' + self.email + '>'

        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

# ----------------------------------------------------------------------------
# Account Info

class Account(TimeTrackModel):
    name = models.CharField(max_length=60)
    logins = models.ManyToManyField(Login)

    def __str__(self):
        return '%s (id=%s)' % (self.name, self.id)


class AccountAddress(TimeTrackModel, AddressInfo):
    name = models.CharField(max_length=30, help_text=('Name or type of the ',
        'address.  Examples: "Primary" or "Sales office".'))
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Account addresses'

    def __str__(self):
        return '%s:%s (id=%s)' % (self.name, self.address1, self.id)
