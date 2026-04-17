from game.consumers.Player import Player
import random
import json

from threading import Thread
from threading import Lock
from time import sleep
from django.core.cache import cache
from game.models.record import Record

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from bot_runing_system.src.bot_run_server.bot_run_service import BotRun
class Game(Thread):
	dx=[-1,0,1,0]
	dy=[0,1,0,-1]

	room_map={}
	room_lock=Lock()

	@classmethod
	def create_or_get(cls,rows,cols,inner_walls_count,idA,botA,idB,botB,room_name):
		with cls.room_lock:
			if room_name in cls.room_map:
				return cls.room_map[room_name]
			game=cls(rows,cols,inner_walls_count,idA,botA,idB,botB,room_name)
			cls.room_map[room_name]=game
			game.createMap()
			game.start()
			return game

	@classmethod
	def del_game(cls,room_name):
		with cls.room_lock:
			if room_name in cls.room_map:
				del cls.room_map[room_name]

	def __init__(self,rows,cols,inner_walls_count,idA,botA,idB,botB,room_name):
		super().__init__()
		self.rows=rows
		self.cols=cols
		self.inner_walls_count=inner_walls_count
		self.room_name=room_name
		self.g=[[0 for j in range(cols)] for i in range(rows)]

		self.botA=botA
		self.botB=botB
		self.botIdA=-1
		self.botIdB=-1
		self.botCodeA=""
		self.botCodeB=""
		if botA!=None:
			self.botIdA=botA.id
			self.botCodeA=botA.content
		if botB!=None:
			self.botIdB=botB.id
			self.botCodeB=botB.content

		self.playerA=Player(idA,rows-2,1,self.botIdA,self.botCodeA,[])
		self.playerB=Player(idB,1,cols-2,self.botIdB,self.botCodeB,[])

		self.nextStepA=None
		self.nextStepB=None
		self.lock=Lock()

		self.status="playing"	#playing->finished
		self.loser=""	#all:平局	A:A输	B:B输

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
		self.g=[[0 for j in range(self.cols)] for i in range(self.rows)]
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


	def setNextStepA(self,nextStepA):
		self.lock.acquire()
		try:
			self.nextStepA=nextStepA
		finally:
			self.lock.release()

	def setNextStepB(self,nextStepB):
		self.lock.acquire()
		try:
			self.nextStepB=nextStepB
		finally:
			self.lock.release()
	def getInput(self,player): #编码当前对局状态
		if player.id==self.playerA.id:
			me=self.playerA
			you=self.playerB
		else:
			me=self.playerB
			you=self.playerA
		return json.dumps({
			'map':self.g,
			'me_sx':me.sx,
			'me_sy':me.sy,
			'me_steps':me.steps,
			'you_sx':you.sx,
			'you_sy':you.sy,
			'you_steps':you.steps,
			})

	def sendBotCode(self,player):
		if player.botId==-1:
			return
		# Make socket
		transport = TSocket.TSocket('127.0.0.1', 9091)
		# Buffering is critical. Raw sockets are very slow
		transport = TTransport.TBufferedTransport(transport)
		# Wrap in a protocol
		protocol = TBinaryProtocol.TBinaryProtocol(transport)
		# Create a client to use the protocol encoder
		client = BotRun.Client(protocol)
		# Connect!
		transport.open()

		client.add_bot(player.id,player.botId,player.botCode,self.getInput(player),player.channel_name)
		# Close!
		transport.close()

	def nextStep(self):
		sleep(0.2)
		self.sendBotCode(self.playerA)
		self.sendBotCode(self.playerB)
		for i in range(50):
			sleep(0.1)
			self.lock.acquire()
			try:
				if self.nextStepA!=None and self.nextStepB!=None:
					self.playerA.steps.append(self.nextStepA)
					self.playerB.steps.append(self.nextStepB)
					return True
			finally:
				self.lock.release()
		return False

	def check_valid(self,cellsA,cellsB):
		n=len(cellsA)
		cell=cellsA[n-1]
		if self.g[cell.x][cell.y]:
			return False
		for i in range(n-1):
			if cellsA[i].x==cell.x and cellsA[i].y==cell.y:
				return False
		for i in range(n-1):
			if cellsB[i].x==cell.x and cellsB[i].y==cell.y:
				return False
		return True

	def judge(self):
		cellsA=self.playerA.getCells()
		cellsB=self.playerB.getCells()
		validA=self.check_valid(cellsA,cellsB)
		validB=self.check_valid(cellsB,cellsA)

		if not validA or not validB:
			self.status="finished"
			if not validA and not validB:
				self.loser="all"
			elif not validA:
				self.loser="A"
			else:
				self.loser="B"


	def sendAllMessage(self,message):
		channel_layer=get_channel_layer()
		message['type']="group_send_event"
		async_to_sync(channel_layer.group_send)(
			self.room_name,message)

	def sendMove(self):
		self.lock.acquire()
		try:
			resp={
				'event':"move",
				'a_direction':self.nextStepA,
				'b_direction':self.nextStepB
			}
			self.nextStepA=self.nextStepB=None
			self.sendAllMessage(resp)
		finally:
			self.lock.release()

	def saveToDatabase(self):
		Record.objects.create(
			a_id=self.playerA.id,
			a_sx=self.playerA.sx,
			a_sy=self.playerA.sy,
			b_id=self.playerB.id,
			b_sx=self.playerB.sx,
			b_sy=self.playerB.sy,
			a_steps=self.playerA.steps,
			b_steps=self.playerB.steps,
			gamemap=self.g,
			loser=self.loser
			)
	def sendResult(self):
		resp={
			'event':"result",
			'loser':self.loser,
		}
		self.saveToDatabase()
		Game.del_game(self.room_name)
		self.sendAllMessage(resp)

	def run(self):
		for i in range(1000):
			if self.nextStep():
				self.judge()
				if self.status=="playing":
					self.sendMove()
				else:
					self.sendResult()
					break
			else:
				self.status="finished"
				self.lock.acquire()
				try:
					if self.nextStepA==None and self.nextStepB==None:
						self.loser="all"
					elif self.nextStepA==None:
						self.loser="A"
					else:
						self.loser="B"
				finally:
					self.lock.release()
				self.sendResult();
				break



