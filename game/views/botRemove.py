from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from game.models.bot import Bot

class BotRemoveView(APIView):
	permission_classes=([IsAuthenticated])

	def post(self,request):
		data=request.POST
		user=request.user
		bot_id=int(data.get("bot_id","").strip())
		try:
			bot=Bot.objects.get(id=bot_id)
			if bot.user_id!=user.id:
				return Response({
					'result':"没有权限删除该bot"
					})
			bot.delete()
			return Response({
				'result':"success"
				})
		except Exception as e:
			return Response({
				'result':"删除失败"
				})