from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PollSerializer, ChoiceSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Poll, Choice

# Create your views here.

@api_view(['GET'])
def getPolls(request):
	polls = Poll.objects.all()
	serial_polls = PollSerializer(polls, many=True)
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
def search(request,key):
	polls = Poll.objects.filter(Q(title__icontains=key) | Q(description__icontains=key) | Q(choice__text__icontains=key)).distinct()
	serial_polls = PollSerializer(polls, many=True)
	return Response(serial_polls.data)

@api_view(['GET'])
def sendEmail(request):
	print("sent")
	return Response()