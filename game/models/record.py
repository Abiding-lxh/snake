from django.db import models

class Record(models.Model):
	a_id=models.IntegerField()
	a_sx=models.IntegerField()
	a_sy=models.IntegerField()
	b_id=models.IntegerField()
	b_sx=models.IntegerField()
	b_sy=models.IntegerField()
	a_steps=models.JSONField(default=list)
	b_steps=models.JSONField(default=list)
	gamemap=models.JSONField(default=list)
	loser=models.CharField(max_length=10)
	createTime=models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		# 示例1：显示对局ID + 对战双方ID
		return f"对局{self.id}：玩家{self.a_id} vs 玩家{self.b_id}"