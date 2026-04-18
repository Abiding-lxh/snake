from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from game.models.player import Player
from django.core.paginator import Paginator
from django.utils import timezone

class rankListView(APIView):
	permission_classes=([IsAuthenticated])

	def get(self,request):
		data=request.GET
		page_num=data.get("page",1)

		# records=Record.objects.all().order_by("-createTime")
		# 一行代码：查记录 + 关联玩家 + 排序 + 分页
		lists = Player.objects.order_by('-score')
		paginator=Paginator(lists,8)

		page_lists=paginator.get_page(page_num)
		data=[]
		for player in page_lists:
			
			data.append({
				"photo":player.photo,
				"username":player.user.username,
				"score":player.score
			})

		return Response({
			'result':"success",
			'data':data,
			'total_page':paginator.num_pages,
			'total_count':paginator.count
			})



