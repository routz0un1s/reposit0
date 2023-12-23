from pygame import *
from random import randint
from time import time as timer
window = display.set_mode((700, 500))
background=transform.scale(image.load('galaxy.jpg'),(700, 500))


clock = time.Clock()
FPS = 60
cooldown = 0

win = 0
loss = 0


mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.5)
mixer.music.play()

volume = 0.5

def music_setter():
    
    global volume
    keys = key.get_pressed()
    if keys[K_UP]:
        volume += 0.05
        mixer.music.set_volume(volume)
        mixer.music.play()
    if keys[K_DOWN]:
        volume -= 0.05
        mixer.music.set_volume (volume)
        mixer.music.play()




class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, self_x, self_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(self_x, self_y))
        self.rect  = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.x, self.rect.y, 25, 30, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global loss
        if self.rect.y > 500 :
            loss += 1
            self.rect.y = 0
            self.rect.x = randint(10, 600)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        



       

rocket = Player('rocket.png', 5, 400, 10, 100, 80)       

monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(10,600), 0, randint(1,2), 65, 50)
    monsters.add(enemy)

asteroids = sprite.Group()
for i in range(4):
    asteroid = Enemy('asteroid.png', randint(10,600), 0, randint(1,2), 65, 50)
    asteroids.add(asteroid)

num_fire = 0
rel_time = False
finished  = False

bullets = sprite.Group()

font.init()
font2 = font.Font(None, 36)
font3 = font.Font(None, 90)
gameover = font3.render('GAME OVER', 1, (255, 0, 0))
gamewon = font3.render('YOU WON!', 1, (0, 255, 0))
relshow = font3.render('WAIT 3 SECONDS!', 1, (255, 0, 0))

game = True

while game:
    window.blit(background,(0, 0))
    music_setter()
    rocket.draw()
    rocket.update()

    keys = key.get_pressed()
    
    for e in event.get():
        if keys [K_SPACE] and cooldown<3:
            rocket.fire()
        elif cooldown>13:
            cooldown = 0 
        if e.type == QUIT:
            game=False
    #     elif e.type == KEYDOWN:
    #         if e.key == K_SPACE:
    #             if num_fire < 5 and rel_time == False:
    #                 num_fire += 1
    #                 rocket.fire()
    #             elif num_fire >= 5 and rel_time == False:
    #                 last_time = timer()
    #                 rel_time = True
    # if rel_time == True:
    #     now_time = timer()
    #     if now_time - last_time < 3:
    #         window.blit(relshow, (100, 200))
    #     else:
    #         num_fire = 0
    #         rel_time = False   
     


    collide = sprite.groupcollide(monsters, bullets, True, True)
    for c in collide:
        win +=1
        enemy = Enemy('ufo.png', randint(10,600), 0, randint(1,4), 65, 50 )
        monsters.add(enemy)
    
   

     if sprite.spritecollide(rocket, monsters, False)or loss >20:
        finished = True
        window.blit(gameover, (200, 200))


    collide = sprite.groupcollide(asteroids, bullets, False, True)
    
    if win >20:
        finished = True
        window.blit(gamewon, (200,200))
    cooldown += 1
    text = font2.render('Score:' + str(win), 1, (255, 255, 255))
    window.blit(text, (10, 20))
    
    text_lose = font2.render('Missed:'+ str(loss), 1, (255, 255, 255))
    window.blit(text_lose, (10, 50))

    if not finished:

        monsters.draw(window)
        monsters.update()
    
        bullets.draw(window)
        bullets.update()

        asteroids.draw(window)
        asteroids.update()
 

           
        
    keys = key.get_pressed()
    if keys [K_r]:
        win = 0
        loss = 0
        for m in monsters:
            m.kill()
        for b in bullets :
            b.kill()
        for a in asteroids:
            a.kill()
        for i in range(5):
            enemy = Enemy('ufo.png', randint(10,600), 0, randint(1, 25), 65, 50 )
            monsters.add(enemy)
        finished = False

    display.update()
    clock.tick(FPS)


