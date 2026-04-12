from django.db import models

class Bot(models.Model):
	user_id=models.IntegerField(null=False)
	title=models.CharField(max_length=100)
	description=models.CharField(max_length=300)
	content=models.TextField()
	rating=models.IntegerField(default=1500)
	createTime=models.DateTimeField(auto_now_add=True)
	modifyTime=models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.title)