from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from game.models.bot import Bot

class BotUpdateView(APIView):
	permission_classes=([IsAuthenticated])
	def post(self,request):
		data=request.POST
		user=request.user
		bot_id=int(data.get("bot_id","").strip())
		title=data.get("title","").strip()
		description=data.get("description","").strip()
		content=data.get("content","").strip()
		if not title:
			return Response({
				'result':"标题不能为空"
				})
		if len(title)>100:
			return Response({
				'result':"标题长度不能大于100"
				})
		if not description:
			description="这个用户很懒，什么也没留下"
		if len(description)>300:
			return Response({
				'result':"描述长度不能大于300"
				})
		if not content:
			return Response({
				'result':"代码不能为空"
				})
		try:
			bot=Bot.objects.get(id=bot_id)
			if bot.user_id!=user.id:
				return Response({
					'result':"没有权限修改该Bot"
					})
			bot.title=title
			bot.description=description
			bot.content=content
			bot.save()
			return Response({
				'result':"success"
				})
		except Exception as e:
			return Response({
				'result':"修改失败"
				})