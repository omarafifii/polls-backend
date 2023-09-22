from django.contrib import admin

from .models import *

admin.site.register([Poll, Choice, Voter, Confirmation])

# Register your models here.
