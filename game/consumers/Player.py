
from game.consumers.Cell import Cell

class Player:

	def __init__(self,id,sx,sy,botId,botCode,steps):

		self.id=id
		self.botId=botId
		self.botCode=botCode
		self.sx=sx
		self.sy=sy
		self.steps=steps if steps is not None else []
		self.channel_name=""

	def check_tail_increasing(self,step):
		if step<=10:
			return True
		return step%3==1

	def getCells(self):
		res=[]
		dx=[-1,0,1,0]
		dy=[0,1,0,-1]
		x,y=self.sx,self.sy
		step=0

		res.append(Cell(x,y))
		for d in self.steps:
			x+=dx[d]
			y+=dy[d]
			res.append(Cell(x,y))
			step+=1
			if not self.check_tail_increasing(step):
				res.pop(0)
		return res
