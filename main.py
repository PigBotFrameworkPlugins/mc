import sys, time, random, json
sys.path.append("../..")
from bot import bot

'''
DATABASE TABLE:
=========================================================
id           INT(11)        PRIMARY_KEY   AUTO_INCREMENT
qn           BIGINT
name         VARCHAR(255)
backpack     LONGTEXT
life         INT(11)
hungry       INT(11)
achievement  LONGTEXT
xp           INT(11)
doing        VARCHAR(255)
doingutill   INT(11)
=========================================================
'''

class mc(bot):
    userItem = []
    
    def init(self):
        self.userItem = self.selectx("SELECT * FROM `botMC` WHERE `qn`={0}".format(self.se.get("user_id")))
        if self.userItem:
            self.userItem = self.userItem[0]
            self.userItem['backpack'] = json.loads(self.userItem.get('backpack'))
            self.CrashReport(self.userItem, "userItem")
    
    def getBackpack(self, thi):
        return self.userItem.get("backpack").get(thi) if self.userItem.get("backpack").get(thi) else 0
    
    def addBackpack(self, thi, num=1):
        if self.userItem.get("backpack").get(thi):
            self.userItem['backpack'][thi] += num
        else:
            self.userItem['backpack'][thi] = num
        self.commonx("UPDATE `botMC` SET `backpack`='{0}' WHERE `qn`={1}".format(json.dumps(self.userItem.get("backpack"), ensure_ascii=False), self.se.get('user_id')))
    
    def addEvent(self, doing, utill):
        self.commonx("UPDATE `botMC` SET `doing`='{0}', `doingutill`={1} WHERE `qn`={2}".format(doing, utill, self.se.get('user_id')))
        
    def ifDoing(self):
        return True if (self.userItem.get("doing") and self.userItem.get("doingutill")) and (self.userItem.get("doingutill") > int(time.time())) else False
    
    def addHungry(self, num):
        self.userItem['hungry'] += num
        self.commonx("UPDATE `botMC` SET `hungry`={0} WHERE `qn`={1}".format(self.userItem.get("hungry"), self.se.get('user_id')))
    
    def mybackpack(self):
        self.init()
        if not self.userItem:
            self.send("你还没出生呢，发送 出生")
            return 
        message = ""
        for i in self.userItem.get("backpack"):
            message += "[face54{}: {}组余{}个]\n".format(i, int((self.userItem.get("backpack").get(i)-self.userItem.get("backpack").get(i)%64)/64), self.userItem.get("backpack").get(i)%64)
        self.send("[CQ:at,qq={0}] 您的背包：\n{1}".format(self.se.get('user_id'), message))
    
    def mystatus(self):
        self.init()
        self.send("[CQ:at,qq={}] 您的状态：\nface54您的血量：{}\nface54您的饱食度：{}\nface54您的经验：{}".format(self.se.get("user_id"), self.userItem.get("life"), self.userItem.get("hungry"), self.userItem.get("xp")))
    
    def whatimdoing(self):
        self.init()
        if not self.userItem:
            self.send("你还没出生呢，发送 出生")
            return 
        if ((not self.userItem.get("doing")) and (not self.userItem.get("doingutill"))) or (self.userItem.get("doingutill") < int(time.time())):
            self.send("[CQ:at,qq={0}] 您的角色正在休息呢，赶紧找个事干吧！".format(self.se.get("user_id")))
        else:
            self.send("[CQ:at,qq={0}] [|您正在{1} 直到{2}|]".format(self.se.get("user_id"), self.userItem.get("doing"), time.ctime(self.userItem.get("doingutill"))))
        
    def cuttree(self):
        if self.check():
            return
        nowtime = int(time.time())
        rand = random.randint(60, 600)
        randtime = nowtime+rand
        gettree = int(rand/10)
        hungry = int(rand/60)
        self.addBackpack("原木", gettree)
        self.addEvent("撸树", randtime)
        self.addHungry(-1*hungry)
        self.send("[CQ:at,qq={0}] 开始撸树\nface54当前时间：[|{1}|]\nface54撸树时长：[|{2}秒|]\nface54获得树木：[|{3}块|]\nface54消耗{4}点饱食度\n请在[|{5}|]再回来领取树木吧！".format(self.se.get('user_id'), time.ctime(nowtime), rand, gettree, hungry, time.ctime(randtime)))
        
    
    def spawn(self):
        uid = self.se.get('user_id')
        self.init()
        if self.userItem:
            self.send("你还没死呢，无法重生！")
            return 
        self.commonx("INSERT INTO `botMC` (`qn`, `name`, `life`, `hungry`, `backpack`, `achievement`) VALUES ({0}, '{1}', 20, 20, '{2}', '[]');".format(uid, self.se.get('sender').get('nickname'), "{}"))
        self.send("[CQ:at,qq={0}] 您已出生！\nface54初始生命值：20\nface54初始饱食度：20\n您接下来可以尝试撸树\n\n提示：MC功能机器人发送的所有时间都是UTC时间，与CST时间时差8小时！".format(uid))
        
    def dig(self):
        uid = self.se.get("user_id")
        if self.check():
            return
        nowtime = int(time.time())
        rand = random.randint(60, 600)
        pix = int(rand/60)
        randtime = nowtime+rand
        stone = random.randint(0, rand)
        coal = random.randint(0, int(rand/2))
        gold = random.randint(0, rand-coal)
        iron = random.randint(0, rand-coal-gold)
        diam = random.randint(0, rand-coal-gold-iron)
        message = ""
        
        if self.getBackpack("原木") >= 2*pix:
            self.addBackpack("石头", stone)
            message += "\n    圆石：{}".format(stone)
        else:
            return self.send("你的木头不够啦，快去撸树吧")
        if self.getBackpack("石头") >= 3*pix:
            self.addBackpack("石头",-3*pix)
            self.addBackpack("铁锭", iron)
            self.addBackpack("煤炭", coal)
            message += "\n    煤炭：{}\n    铁锭：{}".format(coal, iron)
        else:
            message += "\n    煤炭：石头不够\n    铁锭：石头不够"
        if self.getBackpack("铁锭") >= 3*pix:
            self.addBackpack("铁锭",-3*pix)
            self.addBackpack("金锭", gold)
            message += "\n    金锭：{}".format(gold)
        else:
            message += "\n    金锭：铁锭不够"
        if self.getBackpack("金锭") >= 3*pix:
            self.addBackpack("金锭",-3*pix)
            self.addBackpack("钻石", diam)
            message += "\n    钻石：{}".format(diam)
        else:
            message += "\n    钻石：金锭不够"
        
        self.addHungry(-1*pix)
        self.addBackpack("原木", -2*pix)
        self.addEvent("挖矿", randtime)
        self.send("[CQ:at,qq={0}] 开始挖矿\nface54当前时间：[|{1}|]\nface54挖矿时长：[|{2}秒|]\nface54获得矿物：[{3}]\nface54消耗{4}把镐子\nface54消耗{5}点饱食度\n请在[|{6}|]再回来吧！".format(self.se.get('user_id'), time.ctime(nowtime), rand, message, pix, pix, time.ctime(randtime)))
        
    def check(self):
        self.init()
        if not self.userItem:
            self.send("你还没出生呢，发送 出生")
            return True
        if self.ifDoing():
            self.send("您先把手头的事干完把！")
            return True
        if self.userItem.get("hungry") <= 3:
            self.send("您太饿了，等明天恢复饱食度之后再进行操作吧！")
            return True
        return False
        
    def mobsComing(self):
        self.init()
        if self.userItem:
            self.send("[CQ:at,qq={}] 遇到怪物\n".format(self.se.get("user_id")))
        else:
            return False
        return True