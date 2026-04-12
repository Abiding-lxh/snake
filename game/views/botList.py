from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from game.models.bot import Bot

class BotListView(APIView):
	permission_classes=([IsAuthenticated])
	def get(self,request):
		user=request.user
		bots=Bot.objects.filter(user_id=user.id)
		bot_list = []
		for bot in bots:
			bot_list.append({
				"id": bot.id,
				"title": bot.title,
				"description": bot.description,
				"content": bot.content,
				"rating": bot.rating,
			})

		return Response({
			'result':"success",
			'Bots':bot_list
			})