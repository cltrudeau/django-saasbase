# contains abstract contact storage info
import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from awl.models import Choices

# ============================================================================

from localflavor.ca.ca_provinces import PROVINCE_CHOICES
from localflavor.us.us_states import US_STATES

PROVINCE_STATES_CHOICES = PROVINCE_CHOICES + tuple(US_STATES)
PROVINCE_STATES_LOOKUP = dict(PROVINCE_STATES_CHOICES)
COUNTRY_CHOICES = (('CA', 'Canada'), ('US', 'United States of America'))
COUNTRY_LOOKUP = dict(COUNTRY_CHOICES)

class PhoneChoices(Choices):
    MOBILE = 'm'
    HOME = 'h'
    WORK = 'w'
    FAX = 'f'

month_choices = [(i, datetime.date(2008, i, 1).strftime('%B')) \
    for i in range(1, 13)]

day_choices = [(i, i) for i in range(1, 32)]
YEAR_MIN = 1900
YEAR_MAX = datetime.date.today().year + 1
year_choices = [(i, i) for i in range(YEAR_MIN, YEAR_MAX)]

# ============================================================================

class PersonalInfo(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    email = models.EmailField(blank=True)

    class Meta:
        abstract = True


class PhoneInfo(models.Model):
    phone_best = models.CharField(max_length=1, choices=PhoneChoices,
        blank=True)
    phone_home = models.CharField(max_length=32, verbose_name='Home Phone #',
        blank=True)
    phone_mobile = models.CharField(max_length=32, blank=True,
        verbose_name='Mobile Phone #')
    phone_work = models.CharField(max_length=32, verbose_name='Work Phone #',
        blank=True)
    phone_fax = models.CharField(max_length=32, verbose_name='Fax #',
        blank=True)

    class Meta:
        abstract = True


class AddressInfo(models.Model):
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    address3 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    province = models.CharField(max_length=2, blank=True,
        choices=PROVINCE_STATES_CHOICES)
    country = models.CharField(max_length=2, blank=True,
        choices=COUNTRY_CHOICES)

    class Meta:
        abstract = True


class BirthDayInfo(models.Model):
    birth_day = models.PositiveSmallIntegerField(null=True, blank=True,
        choices=day_choices,
        validators=[MinValueValidator(1), MaxValueValidator(31)])
    birth_month = models.PositiveSmallIntegerField(null=True, blank=True,
        choices=month_choices,
        validators=[MinValueValidator(1), MaxValueValidator(12)])
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True,
        choices=year_choices,
        validators=[MinValueValidator(YEAR_MIN), MaxValueValidator(YEAR_MAX)])

    class Meta:
        abstract = True
