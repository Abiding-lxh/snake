from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from game.models.record import Record
from django.core.paginator import Paginator
from django.utils import timezone

class getRecordView(APIView):
	permission_classes=([IsAuthenticated])

	def get(self,request):
		data=request.GET
		page_num=data.get("page",1)

		# records=Record.objects.all().order_by("-createTime")
		# 一行代码：查记录 + 关联玩家 + 排序 + 分页
		records = Record.objects.select_related('a_id', 'b_id').order_by('-createTime')
		paginator=Paginator(records,8)

		page_record=paginator.get_page(page_num)

		data = []

		for record in page_record:
			print(record.a_id)
			gameresult="平局"
			if record.loser=="A":
				gameresult="B胜"
			elif record.loser=="B":
				gameresult="A胜"
			data.append({
				"id":record.id,
				"a_id":record.a_id.id,
				"a_username":record.a_id.username,
				"a_photo":record.a_id.player.photo,
				"a_sx":record.a_sx,
				"a_sy":record.a_sy,
				"b_id":record.b_id.id,
				"b_username":record.b_id.username,
				'b_photo':record.b_id.player.photo,
				"b_sx":record.b_sx,
				"b_sy":record.b_sy,
				"a_steps":record.a_steps,
				"b_steps":record.b_steps,
				"gameresult":gameresult,
				"gamemap":record.gamemap,
				"loser": record.loser,
				"createTime": timezone.localtime(record.createTime).strftime('%Y-%m-%d %H:%M:%S')
			})

		return Response({
			'result':"success",
			'data':data,
			'total_page':paginator.num_pages,
			'total_count':paginator.count
			})



