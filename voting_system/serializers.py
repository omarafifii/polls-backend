from rest_framework import serializers
from .models import Poll, Choice, Voter, Confirmation

class PollSerializer(serializers.ModelSerializer):
	class Meta:
		model = Poll
		fields ='__all__'

class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Choice
		fields ='__all__'

class VoterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Voter
		fields ='__all__'

class ConfirmationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Confirmation
		fields ='__all__'