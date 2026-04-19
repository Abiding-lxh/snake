### 简介
回合制游戏，两名玩家在线匹配，玩家可以亲自上阵或者使用自己的Bot（用户可上传代码创建自己的Bot代替自己出战），每一回合玩家给出下一步方向，如果未碰撞则继续游戏，否则结束游戏。 线上demo：https://snake.abiding.cn

本游戏仿照bozone网站上的贪吃蛇游戏,游戏原型：https://www.botzone.org.cn/game/Snake
### 游戏规则
玩家创建账号进入对战界面，匹配成功后进入对局，通过wasd控制蛇的方向，每一回合有5秒的反应时间，若五秒内没有输入则输，若移动期间撞到墙体或者蛇的身体则输，直到一方死亡游戏结束。
想要用Bot代替自己出战则需要先创建Bot（目前仅支持Python语言创建的Bot，具体创建规则见下一项）。
### Bot创建规则
需要实现给定接口，并重写该接口的给定函数。
函数输入为一个字符串，格式为：gamemap#me_sx#me_sy#me_steps#you_sx#you_sy#you_steps。gamemap为地图，目前是13*14的一张地图，地图每一行之间用$隔开；me_sx为自己起点横坐标，me_sy为自己起点纵坐标，me_steps为自己从游戏开始至目前回合每一回合的方向，在"[]"内。对手同理。
样例：11111111111111$10001010000010$1001010...0011$11111111111111#11#1#[0122]#1#11#[2100]

给定接口如下：
```
class BotInterface(ABC):
    @abstractmethod
    def nextStep(self,input):
        pass
```
玩家需实现一下类，nextStep需返回四个方向0,1,2,3,分别表示上、右、下、左。其中类名，方法名不能改变，且bot执行中不能有任何输出到stdout，只能通过nextStep函数返回值，否则会导致游戏无法正确获取Bot的输入。
```
class Bot(BotInterface):
    def nextStep(self,input):
        pass
        return 0
```

参考Bot实现如下，该简单Bot仅随机查看下一步四个方向是否合法，如合法则选择方向，不会做出最优选择。
```
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
```


