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
    userItem = {}
    
    def init(self):
        self.userItem = self.selectx("SELECT * FROM `botMC` WHERE `qn`={0}".format(self.se.get("user_id")))
        if self.userItem:
            self.userItem = self.userItem[0]
            self.userItem['backpack'] = json.loads(self.userItem.get('backpack'))
    
    def addBackpack(self, thi, num=1):
        if self.userItem.get("backpack").get(thi):
            self.userItem['backpack'][thi] += num
        else:
            self.userItem['backpack'][thi] = num
        self.commonx("UPDATE `botMC` SET `backpack`='{0}' WHERE `qn`={1}".format(json.dumps(self.userItem.get("backpack")), self.se.get('user_id')))
    
    def addEvent(self, doing, utill):
        self.commonx("UPDATE `botMC` SET `doing`='{0}', `doingutill`={1} WHERE `qn`={2}".format(doing, utill, self.se.get('user_id')))
    
    def mybackpack(self):
        self.init()
        if not self.userItem:
            self.send("你还没出生呢，发送 出生")
            return 
        self.send("[CQ:at,qq={0}] 您的背包：\n{1}".format(self.se.get('user_id'), self.userItem.get("backpack")))
    
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
        self.init()
        if not self.userItem:
            self.send("你还没出生呢，发送 出生")
            return 
        nowtime = int(time.time())
        rand = random.randint(60, 600)
        randtime = nowtime+rand
        gettree = int(rand/10)
        self.addBackpack("tree", gettree)
        self.addEvent("撸树", randtime)
        self.send("[CQ:at,qq={0}] 开始撸树\nface54当前时间：[|{1}|]\nface54撸树时长：[|{2}秒|]\nface54获得树木：[|{3}块|]\n请在[|{4}|]再回来领取树木吧！".format(self.se.get('user_id'), time.ctime(nowtime), rand, gettree, time.ctime(randtime)))
        
    
    def spawn(self):
        uid = self.se.get('user_id')
        self.init()
        if self.userItem:
            self.send("你还没死呢，无法重生！")
            return 
        self.commonx("INSERT INTO `botMC` (`qn`, `name`, `life`, `hungry`, `backpack`, `achievement`) VALUES ({0}, '{1}', 20, 20, '{2}', '[]');".format(uid, self.se.get('sender').get('nickname'), "{}"))
        self.send("[CQ:at,qq={0}] 您已出生！\nface54初始生命值：20\nface54初始饱食度：20\n您接下来可以尝试撸树".format(uid))