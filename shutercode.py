from pygame import *

from random import *

from time import  time as timer

class GameSprite(sprite.Sprite):
    def __init__ (self,picture,x,y,width,height,speed):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        self.keys = key.get_pressed()
        if self.keys[K_RIGHT] and self.rect.x < 850:
            self.rect.x += self.speed
        if self.keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('pulya.png',self.rect.centerx,self.rect.top,20,20,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 650:
            self.rect.y = 0
            self.rect.x = randint(1,1000)
            lost = lost + 1

class Aster(Enemy):
    def update(self):
        self.rect.y += self.speed
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()



window = display.set_mode((1000, 650))
display.set_caption("крутой шутер с котятами")
background = transform.scale(image.load("fonraduga.jpg"), (1000, 650))

player = Player('geroi.png',440,530,130,112,5)

enemys = sprite.Group()
for i in range (4):
    enemy = Enemy('vrag.png',randint(0,1000),0,90,85,randint(1,2))
    enemys.add(enemy)

asters = sprite.Group()
for a in range (2):
    aster = Aster('aster.png',randint(0,1000),0,70,70,randint(1,2))
    asters.add(aster)

bullets = sprite.Group()

clock = time.Clock()
FPS = 60

run = True
finish = False
font.init()
font2 = font.SysFont('EchoRevival Regular', 36)
lost = 0
score = 0
num_fire = 0 
rel_time = False

#!если честно я не очень понимаю как это работает но оно работает круто котята 

while run:
#    score += 123456789
    for e in event.get():
        if e.type == QUIT:
            run = False 
        if e.type == KEYDOWN:
            if e.key == K_SPACE:  
                if num_fire < 10 and rel_time == False:
                    player.fire()
                    num_fire = num_fire + 1
                    if num_fire >= 10 and rel_time == False:
                        rel_time = True
                        t = timer()
        if e.type == KEYDOWN:
            if e.key == K_r:
                finish = False
                score = 0
                lost = 0
                for j in enemys:
                    j.kill()
                for i in range (4):
                    enemy = Enemy('vrag.png',randint(0,1000),0,90,85,randint(1,2))
                    enemys.add(enemy)
                for h in asters:
                    h.kill()
                for a in range (2):
                    aster = Aster('aster.png',randint(0,1000),0,70,70,randint(1,2))
                    asters.add(aster)
    if not finish:
        window.blit(background,(0, 0))
        enemys.draw(window)
        enemys.update()
        asters.draw(window)
        asters.update()
        player.reset()
        player.update()
        bullets.draw(window)
        bullets.update()
        text = font2.render('пропущено: ' + str(lost), 1, (0,0,0))
        window.blit(text, (10, 20))
        text = font2.render('счет: ' + str(score), 1, (0,0,0))
        window.blit(text, (10, 60))
        if lost >= 15 or sprite.spritecollide(player, enemys, False) or sprite.spritecollide(player, asters, False):
            finish = True
            text = font2.render('проиграли((', 1, (250,250,250))
            window.blit(text,(200,225))
        sprites_list = sprite.groupcollide(enemys, bullets, True, True)
        for c in sprites_list:
            score += 1
            enemy = Enemy('vrag.png',randint(0,1000),0,90,85,randint(1,2))
            enemys.add(enemy)
        if score >= 15:
            finish = True
            text = font2.render('выиграли !! <3', 1, (250,250,250))
            window.blit(text,(200,225))
        
            text = font2.render('<3', 2, (255,102,178))
            window.blit(text,(230,280))
        if rel_time == True:
            d = timer()
            if d-t < 3:
                textperez = font2.render('перезаряд_очка', 1, (250,250,250))
                window.blit(textperez,(400,500))
            else:
                num_fire = 0
                rel_time = False 
    
    display.update()
    clock.tick(FPS)