from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.cache import cache
from channels.db import database_sync_to_async
from game.models.player import Player
from game.consumers.Game import Game

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from match_system.src.match_server.match_service import Match

class MultiPlayer(AsyncWebsocketConsumer):
	async def connect(self):
		self.user=self.scope['user']
		if self.user.is_authenticated:
			await self.accept()
			print('accept')
		else:
			print("连接失败")
			await self.close()
		def db_get_player(user):
			return Player.objects.get(user__username=self.user.username)
		self.player=await database_sync_to_async(Player.objects.get)(user=self.user)


	async def disconnect(self, close_code):
		if hasattr(self,'game') and self.game:
			self.game=None
		if hasattr(self,'room_name') and self.room_name:
			print('disconnect')
			await self.channel_layer.group_discard(self.room_name, self.channel_name)

	async def start_matching(self,data):
		print("start-matching")
		# Make socket
		transport = TSocket.TSocket('127.0.0.1', 9090)
		# Buffering is critical. Raw sockets are very slow
		transport = TTransport.TBufferedTransport(transport)

		# Wrap in a protocol
		protocol = TBinaryProtocol.TBinaryProtocol(transport)

		# Create a client to use the protocol encoder
		client = Match.Client(protocol)

		# Connect!
		transport.open()

		client.add_player(self.player.score,self.user.id,999,self.channel_name)

		# Close!
		transport.close()	

	async def stop_matching(self,data):
		print("stop-matching")
		# Make socket
		transport = TSocket.TSocket('127.0.0.1', 9090)
		# Buffering is critical. Raw sockets are very slow
		transport = TTransport.TBufferedTransport(transport)

		# Wrap in a protocol
		protocol = TBinaryProtocol.TBinaryProtocol(transport)

		# Create a client to use the protocol encoder
		client = Match.Client(protocol)

		# Connect!
		transport.open()


		client.remove_player(self.player.score,self.user.id,999,self.channel_name)

		# Close!
		transport.close()
		pass
	async def move(self,data):
		direction=data['direction']
		if self.game.playerA.id==self.user.id:
			self.game.setNextStepA(direction)
		elif self.game.playerB.id==self.user.id:
			self.game.setNextStepB(direction)
	
	async def start_game(self,data):
		aId=data['a_id']
		aBotId=data['a_bot_id']
		bId=data['b_id']
		bBotId=data['b_bot_id']
		self.room_name=data['room_name']

		self.game=Game.create_or_get(aId,bId,self.room_name)
		with Game.room_lock:
			print(Game.room_map)
		print(self.user,self.game)

		respGame={
				'a_id':self.game.playerA.id,
				'a_sx':self.game.playerA.sx,
				'a_sy':self.game.playerA.sy,
				'b_id':self.game.playerB.id,
				'b_sx':self.game.playerB.sx,
				'b_sy':self.game.playerB.sy,
				'map':self.game.g
			}
		print(self.user.id,aId,bId,"start_game")
		if self.user.id==aId:
			opponent_channel_name=data['b_channel_name']
		elif self.user.id==bId:
			opponent_channel_name=data['a_channel_name']

		await self.channel_layer.send(
			opponent_channel_name,
			{
				'type':"single_send_event",
				'event':"start-matching",
				'id':self.user.id,
				'username':self.user.username,
				'photo':self.player.photo,
				'game':respGame
			})

	async def single_send_event(self,data):
		await self.send(text_data=json.dumps(data))
	async def group_send_event(self,data):
		if data['event']=="result":
			self.game=None
		await self.send(text_data=json.dumps(data))
	async def receive(self, text_data):
		data = json.loads(text_data)
		print(data)
		event=data['event']
		if event=="start-matching":
			await self.start_matching(data)
		elif event=="stop-matching":
			await self.stop_matching(data)
		elif event=="move":
			await self.move(data)