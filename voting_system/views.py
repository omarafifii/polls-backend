import json
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PollSerializer, ChoiceSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .misc import *
from .models import *

# Create your views here.

@api_view(['GET'])
def getPolls(request):
	polls = Poll.objects.all()
	serial_polls = PollSerializer(polls, many=True)
	if(request.body):
		json_data = json.loads(request.body)
		items_per_page = json_data['items_per_page']
		current_page = json_data['current_page']
		p = Paginator(polls, items_per_page)
		number_of_pages = p.num_pages
		return Response({
			"number_of_pages": "{}".format(number_of_pages),
			"data": PollSerializer((p.page(current_page).object_list), many=True).data
			})
	return Response(serial_polls.data)

@api_view(['GET'])
def getPollChoices(request,pk):
	try:
		poll = Poll.objects.get(pk=pk)
	except:
		return Response({"error": "Id is incorrect"}, status=400)
	choices = poll.choice_set.all()
	serial_choices = ChoiceSerializer(choices, many=True)
	return Response(serial_choices.data)

@api_view(['GET'])
# def search(request,key):
def search(request,key):
	polls = Poll.objects.filter(Q(title__icontains=key) | Q(description__icontains=key) | Q(choice__text__icontains=key)).distinct()
	serial_polls = PollSerializer(polls, many=True)
	if(request.body):
		json_data = json.loads(request.body)
		items_per_page = json_data['items_per_page']
		current_page = json_data['current_page']
		p = Paginator(polls, items_per_page)
		number_of_pages = p.num_pages
		return Response({
			"number_of_pages": "{}".format(number_of_pages),
			"data": PollSerializer((p.page(current_page).object_list), many=True).data
			})
	return Response(serial_polls.data)

@api_view(['POST'])
def vote(request):
	try:
		json_data = json.loads(request.body)
		email = json_data['email']
		choice_id = json_data['choice_id']
	except:
		return Response({"error": "Missing data"}, status=400)
	voter = get_Voter(email)
	try:
		choice = Choice.objects.get(pk=choice_id)
	except:
		return Response({"error": "Wrong data"}, status=400)

	poll = choice.poll

	if not is_first_time_voter(poll,voter):
		return Response({"error": "Already voted!"}, status=400)

	if is_Poll_expired(poll):
		return Response({"error": "Poll expired!"}, status=400)
		
	otp = generate_OTP()
	deactivate_old_otp(voter)

	confirmation = Confirmation(otp=otp,voter=voter)
	confirmation.save()

	send_Email(otp=otp, receipient=voter.email)

	return Response("Email sent, enter OTP to proceed")

@api_view(['POST'])
def confirm(request):
	try:
		json_data = json.loads(request.body)
		email = json_data['email']
		choice_id = json_data['choice_id']
		otp = json_data['otp']
	except:
		return Response({"error": "Missing data"}, status=400)
	voter = get_Voter(email)
	try:
		choice = Choice.objects.get(pk=choice_id)
	except:
		return Response({"error": "Wrong data"}, status=400)
	
	try:
		confirmation = Confirmation.objects.get(otp=otp)
	except:
		return Response({"error": "Wrong otp"}, status=400)

	poll = choice.poll

	if is_Poll_expired(poll):
		return Response({"error": "Poll expired!"}, status=400)

	if not check_email_otp(confirmation,voter):
		return Response({"error": "Wrong otp"}, status=400)

	if is_OTP_expired(confirmation) or not is_OTP_active(confirmation):
		return Response({"error": "OTP expired"}, status=400)

	increment_vote(choice)
	deactivate_old_otp(voter)
	
	return Response("Voted Successfully")