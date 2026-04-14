
import random

class Game:
	dx=[-1,0,1,0]
	dy=[0,1,0,-1]

	def __init__(self,rows,cols,inner_walls_count):
		self.rows=rows
		self.cols=cols
		self.inner_walls_count=inner_walls_count
		self.g=[[0 for j in range(cols)] for i in range(rows)]

	def check_connectivity(self,sx,sy,tx,ty):
		if sx==tx and sy==ty:
			return True
		self.g[sx][sy]=1
		for i in range(4):
			x=sx+Game.dx[i]
			y=sy+Game.dy[i]
			if x>=0 and x<self.rows and y>=0 and y<self.cols and self.g[x][y]==0:
				if self.check_connectivity(x,y,tx,ty):
					self.g[sx][sy]=0
					return True;
		self.g[sx][sy]=0
		return False
	def draw(self):
		for r in range(self.rows):
			self.g[r][0]=self.g[r][self.cols-1]=1
		for c in range(self.cols):
			self.g[0][c]=self.g[self.rows-1][c]=1

		for i in range(int(self.inner_walls_count/2)):
			for j in range(1000):
				r=random.randint(0,self.rows-1)
				c=random.randint(0,self.cols-1)
				if self.g[r][c] or self.g[self.rows-1-r][self.cols-1-c]:
					continue
				if r==self.rows-2 and c==1 or r==1 and c==self.cols-2:
					continue
				self.g[r][c]=self.g[self.rows-1-r][self.cols-1-c]=1
				break
		return self.check_connectivity(self.rows-2,1,1,self.cols-2)
	def createMap(self):
		for i in range(1000):
			if self.draw():
				break