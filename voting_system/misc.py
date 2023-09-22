from .models import *
import random
from datetime import datetime, timedelta

from django.core.mail import send_mail


def generate_OTP():
    otp = 0
    while True:
        otp = random.randint(100000,999999)
        if len(Confirmation.objects.filter(otp=otp, isActive=True)) == 0:
            break
    return otp

def send_Email(otp, receipient):
    receiving_list = [receipient]
    message = "This is your OTP: {}".format(otp)
    send_mail(subject="This is your OTP", message=message, from_email="voting@voting.com", recipient_list=receiving_list,fail_silently=False)
    return True

def is_first_time_voter(poll:Poll, voter:Voter):
    voting_list = poll.voter_set.filter(email=voter.email)
    return len(voting_list) == 0

def is_OTP_expired(confirmation: Confirmation):
    now = datetime.now()
    date_created = confirmation.created_at
    return now - date_created < timedelta(minutes=10)
