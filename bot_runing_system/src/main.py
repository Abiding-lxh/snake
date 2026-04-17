import glob
import sys
sys.path.insert(0, glob.glob('../../')[0])
import subprocess
import json
from bot_run_server.bot_run_service import BotRun

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from asgiref.sync import async_to_sync
from snake.asgi import channel_layer

from threading import Condition
from threading import Thread
from queue import Queue

bots=Queue()

from abc import ABC,abstractmethod
class BotInterface(ABC):
    @abstractmethod
    def nextStep(self,input):
        pass
import random

class Bot(BotInterface):
    class Cell:
        def __init__(self,x,y):
            self.x=x
            self.y=y

    def check_tail_increasing(self,step):
        if step<=10:
            return True
        return step%3==1
    def getCells(self,sx,sy,steps):
        res=[]
        dx=[-1,0,1,0]
        dy=[0,1,0,-1]
        x,y=sx,sy
        step=0

        res.append(Bot.Cell(x,y))
        for d in steps:
            d=int(d)
            x+=dx[d]
            y+=dy[d]
            res.append(Bot.Cell(x,y))
            step+=1
            if not self.check_tail_increasing(step):
                res.pop(0)
        return res

    def nextStep(self,input):
        rows,me_sx,me_sy,me_steps,you_sx,you_sy,you_steps=input.split("#")
        res=rows.split('$')
        g=[]
        for i in res:
            g.append([int(x) for x in i])
        me_sx,me_sy,you_sx,you_sy=map(int,[me_sx,me_sy,you_sx,you_sy])
        me_steps=me_steps.replace('[','').replace(']','')
        you_steps=you_steps.replace('[','').replace(']','')
        me_steps=[int(x) for x in me_steps]
        you_steps=[int(x) for x in you_steps]

        aCells=self.getCells(me_sx,me_sy,me_steps)
        bCells=self.getCells(you_sx,you_sy,you_steps)

        for c in aCells:
            g[c.x][c.y]=1
        for c in bCells:
            g[c.x][c.y]=1
        dx,dy=[-1,0,1,0],[0,1,0,-1]
        lst = random.sample([0,1,2,3], 4)
        for i in lst:
            x=aCells[len(aCells)-1].x+dx[i]
            y=aCells[len(aCells)-1].y+dy[i]
            if x>=0 and x<len(g) and y>=0 and y<len(g[0]) and g[x][y]==0:
                return i
        return 0

class Consumer(Thread):
    def __init__(self,id,bot_code,input,channel_name):
        super().__init__()
        self.daemon=True
        self.id=id
        self.bot_code=bot_code
        self.input=json.loads(input)
        self.channel_name=channel_name

    def getDockerInput(self):
        rows=[]
        for r in self.input['map']:
            rows.append(''.join(str(x) for x in r))
        gamemap='$'.join(rows)
        me_sx=str(self.input['me_sx'])
        me_sy=str(self.input['me_sy'])
        me_steps=''
        for x in self.input['me_steps']:
            me_steps+=(str(x))
        you_sx=str(self.input['you_sx'])
        you_sy=str(self.input['you_sy'])
        you_steps=''
        for x in self.input['you_steps']:
            you_steps+=(str(x))
        input=gamemap+'#'+me_sx+'#'+me_sy+'#'+me_steps+'#'+you_sx+'#'+you_sy+'#'+you_steps

        # print(Bot().nextStep(input),"testinggggggggggggggggggggggggggggggggggg")

        self.tmp=f'''
from abc import ABC,abstractmethod
class BotInterface(ABC):
    @abstractmethod
    def nextStep(self,input):
        pass

{self.bot_code}

input="{input}"
direction=Bot().nextStep(input)
print(direction,end='')
'''     
    def run(self):
        self.getDockerInput()
        cmd = [
            "docker", "run",
            "--rm",            # 执行完自动删除容器
            "--network=none",  # 禁止联网（防止用户代码访问外部资源）
            "--memory=128m",   # 限制内存，防内存炸弹
            "--cpus=0.4",      # 限制 CPU，防死循环占满资源
            "python:3.9-slim",
            "python", "-c", self.tmp.replace("\t","    ")
        ]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=2  #2 秒超时，自动杀死
            )
            direction=result.stdout
            if len(direction)==1 and int(direction)>=0 and int(direction)<4:
                async_to_sync(channel_layer.send)(
                    self.channel_name,
                    {
                        'type':"receive_bot_nextstep",
                        'direction':result.stdout
                    })
        except subprocess.TimeoutExpired:
            print(f"实例 {self.id} 执行超时，已强制杀死！")
        except Exception as e:
            print(f"错误：{e}")

def worker():
    while True:
        id,bot_code,input,channel_name=bots.get()
        consumer=Consumer(id,bot_code,input,channel_name)
        consumer.start()

class BotRunHandler:    
    def add_bot(self,id,botId,bot_code,input,channel_name):
        bots.put((id,bot_code,input,channel_name))
        return 0

if __name__ == '__main__':
    handler = BotRunHandler()
    processor = BotRun.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9091)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    # server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    server = TServer.TThreadedServer(
        processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)
    Thread(target=worker,daemon=True).start()
    print('Starting the server...')
    server.serve()
    print('done.')

