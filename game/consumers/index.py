from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.cache import cache
from channels.db import database_sync_to_async
from game.models.player import Player
from game.consumers.Game import Game

class MultiPlayer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user=self.scope['user']
        
        if self.user.is_authenticated:
            await self.accept()
            print('accept')
        else:
            print("连接失败")
            await self.close()
        self.room_name = "room"

        

    async def disconnect(self, close_code):
        print('disconnect')
        await self.channel_layer.group_discard(self.room_name, self.channel_name)


    async def start_matching(self,data):
        print("start-matching")
        for i in range(1000):
            name="room-%d"%(i)
            if not cache.has_key(name) or len(cache.get(name))<2:
                self.room_name=name
                break
        if not self.room_name:
            return
        if not cache.has_key(self.room_name):
            cache.set(self.room_name,[],3600)
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        def db_get_player(user):
            return Player.objects.get(user=user)
        self.player=await database_sync_to_async(Player.objects.get)(user=self.user)
        players=cache.get(self.room_name)
        players.append({
            'id':self.user.id,
            'username':self.user.username,
            'photo':self.player.photo
            })
        cache.set(self.room_name,players,3600)
        print(self.user,self.user.is_authenticated)
        if len(players)>=2:
            game=Game(13,14,20)
            game.createMap()
            for p in players:
                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        'type':"group_send_event",
                        'event':"start-matching",
                        'id':p['id'],
                        'username':p['username'],
                        'photo':p['photo'],
                        'gamemap':game.g
                    })

    async def stop_matching(self,data):
        print("stop-matching")
        pass
    async def group_send_event(self,data):
        await self.send(text_data=json.dumps(data))
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        event=data['event']
        if event=="start-matching":
            await self.start_matching(data)
        elif event=="stop-matching":
            await self.stop_matching(data)