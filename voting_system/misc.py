from .models import *
import random
from datetime import datetime, timedelta, timezone

from django.core.mail import send_mail


# OTP confirmation
def send_Email(otp, receipient):
    receiving_list = [receipient]
    message = "This is your OTP: {}".format(otp)
    send_mail(subject="This is your OTP", message=message, from_email="voting@omarafifi.com", recipient_list=receiving_list,fail_silently=False)
    return True

def generate_OTP():
    otp = 0
    while True:
        otp = random.randint(100000,999999)
        if len(Confirmation.objects.filter(otp=otp, isActive=True)) == 0:
            break
    return otp

def is_OTP_expired(confirmation: Confirmation):
    now = datetime.now(timezone.utc)
    date_created = confirmation.created_at
    return now - date_created > timedelta(minutes=10)

def deactivate_OTP(confirmation: Confirmation):
    confirmation.isActive = False
    confirmation.save()
    return True

def deactivate_old_otp(voter: Voter):
    otp_list = Confirmation.objects.filter(voter=voter)
    if len(otp_list) > 0:
        for otp in otp_list:
            otp.isActive = False
            otp.save()
    return True

def is_OTP_active(confirmation: Confirmation):
    return confirmation.isActive

def check_email_otp(confirmation: Confirmation, voter:Voter):
    return confirmation.voter.email == voter.email


# Polls
def is_Poll_expired(poll: Poll):
    now = datetime.now(timezone.utc)
    expiry_date = poll.exp_date
    return now > expiry_date

def get_Poll_from_Choice(c: Choice):
    return c.poll

# Voters
def get_Voter(email):
    v_list = Voter.objects.filter(email=email)
    if len(v_list) == 0:
        v = Voter(email=email)
        v.save()
        return v
    return v_list[0]

def is_first_time_voter(poll:Poll, voter:Voter):
    voting_list = poll.voter_set.filter(email=voter.email)
    return len(voting_list) == 0

# Choice
def increment_vote(choice:Choice):
    votes = choice.votes
    votes += 1
    choice.votes = votes
    choice.save()
    return True