from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
	return JsonResponse({
		'bot_name':"人机一号",
		'bot_rating':1500
		})