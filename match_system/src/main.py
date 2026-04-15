import glob
import sys
sys.path.insert(0, glob.glob('../../')[0])

from match_server.match_service import Match

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from queue import Queue
from time import sleep
from threading import Thread
from threading import Lock
from threading import Condition

from asgiref.sync import async_to_sync
from django.core.cache import cache

from snake.asgi import channel_layer
# from channels.layers import get_channel_layer

class Player:
	def __init__(self,score,id,botId,channel_name):
		self.score=score
		self.id=id
		self.botId=botId
		self.channel_name=channel_name
		self.waiting_time=0

class Pool:
	def __init__(self):
		self.players=[]
		self.lock=Lock()
		self.cv=Condition(self.lock)

	def add_player(self,player):
		with self.cv:
			self.players.append(player)
			if len(self.players)>=2:
				self.cv.notify()
	def remove_player(self,player):
		with self.cv:
			for i in range(len(self.players)-1, -1, -1):
				if self.players[i].id == player.id:
					del self.players[i]
					break

	def check_match(self,a,b):
		dt=abs(a.score-b.score)
		a_max_dif=a.waiting_time*50
		b_max_dif=b.waiting_time*50
		return dt<=a_max_dif and dt<=b_max_dif

	def match_success(self,ps):
		print("Match success %s %s",ps[0].id,ps[1].id)
		room_name="room-%s-%s"%(ps[0].id,ps[1].id)

		# channel_layer=get_channel_layer()
		for p in ps:
			async_to_sync(channel_layer.group_add)(room_name,p.channel_name)


		async_to_sync(channel_layer.group_send)(
			room_name,
			{
				'type':"start_game",
				'room_name':room_name,
				'a_id':ps[0].id,
				'a_bot_id':ps[0].botId,
				'a_score':ps[0].score,
				'a_channel_name':ps[0].channel_name,
				'b_id':ps[1].id,
				'b_bot_id':ps[1].botId,
				'b_score':ps[1].score,
				'b_channel_name':ps[1].channel_name
			})

	def increase_waiting_time(self):
		for p in self.players:
			p.waiting_time+=1

	def match(self):
		while len(self.players)>=2:
			self.players=sorted(self.players,key=lambda p:p.score)
			flag=False
			for i in range(len(self.players)-1):
				a,b=self.players[i],self.players[i+1]
				if self.check_match(a,b):
					self.match_success([a,b])
					self.players=self.players[:i]+self.players[i+2:]
					flag=True
					break
			if not flag:
				break

		self.increase_waiting_time()


pool=Pool()
queue=Queue()


class MatchHandler:
	def add_player(self,score,id,botId,channel_name):
		player=Player(score,id,botId,channel_name)
		queue.put((player,"add"))
		print(id,botId,score,"thrift add")
		return 0
	def remove_player(self,score,id,botId,channel_name):
		player=Player(score,id,botId,channel_name)
		queue.put((player,"remove"))
		print(id,botId,score,"thrift remove")
		return 0

def consumer_thread():
	while True:
		print(queue.qsize(),"consumer_thread")
		player,option=queue.get()
		print(str(player),option,"consumer_thread")
		if option=="add":
			pool.add_player(player)

		elif option=="remove":
			pool.remove_player(player)

def match_thread():
	print("Start Match")
	while True:
		with pool.cv:
			while len(pool.players)<2:
				pool.cv.wait()
			print(pool.players)
			pool.match()
			print(pool.players)
			sleep(1)
		print("match loop")

if __name__ == '__main__':
	handler = MatchHandler()
	processor = Match.Processor(handler)
	transport = TSocket.TServerSocket(host='127.0.0.1', port=9090)
	tfactory = TTransport.TBufferedTransportFactory()
	pfactory = TBinaryProtocol.TBinaryProtocolFactory()

	# server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

	# You could do one of these for a multithreaded server
	server = TServer.TThreadedServer(
		processor, transport, tfactory, pfactory)
	# server = TServer.TThreadPoolServer(
	#     processor, transport, tfactory, pfactory)

	print('Starting the server...')
	Thread(target=match_thread,daemon=True).start()
	Thread(target=consumer_thread,daemon=True).start()
	server.serve()
	print('done.')