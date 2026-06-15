from pygame import *
from random import *
from config import *
init()

ANCHO, ALTO = 800, 700
TITULO = 'Proyecto shooter'
BACK_COLOR = (80,212,187)
WHITE=(255,255,255)
BLACK= (0,0,0)
COLOR= (200,200,223)
PLAYER_IMG = 'src/nave_proye_espacio-remo.png'
ENEMY_IMG = 'src/enemigo_proye_shooter-remove.png'
FONDO = 'src/fondo espacio proye.jpg'
YOUWIN='src/Ganaste.png'
FPS= 60
GAMEOVER= 'src/gameoverwhite.jpg'
STARS_IMG='src/Estrellas shooter.png'
BULLETS= 'src/bala_disparo_shooter-remove.png'
TEXT_FONT='src/BitcountPropDoubleInk-VariableFont_CRSV,ELSH,ELXP,SZP1,SZP2,XPN1,XPN2,YPN1,YPN2,slnt,wght.ttf'

#parametros
points= 0
misses= 0
lives= 5
star_spawn = randint(60, 360)


pantalla= display.set_mode((ANCHO, ALTO))
display.set_caption(TITULO)

lose= transform.scale(image.load(GAMEOVER), (ANCHO,ALTO))
background= transform.scale(image.load(FONDO), (ANCHO,ALTO))
winnner= transform.scale(image.load(YOUWIN),(ANCHO,ALTO))


font_1= font.Font(TEXT_FONT,30)




class Character(sprite.Sprite):
    def __init__(self,sprite_img,cord_x,cord_y, sprite_width , sprite_height , speed=0):
        super().__init__()

        self.width= sprite_width
        self.height= sprite_height
        self.image = transform.scale(image.load(sprite_img),(sprite_width,sprite_height))
        self.rect= self.image.get_rect()
        self.rect.x=cord_x
        self.rect.y=cord_y
        self.speed= speed
    
    def reset(self):
        pantalla.blit(self.image, (self.rect.x, self.rect.y) )

#CLASES DERIVADAS
class Player(Character):
    def update(self):
        keys= key.get_pressed()
        if keys[K_d] and self.rect.x <=ANCHO - self.rect.w:
            self.rect.x += self.speed
        elif keys[K_a] and self.rect.x >=0:
            self.rect.x -= self.speed

    def shoot(self):
        
        bala= Bullet(BULLETS,self.rect.centerx, self.rect.top, 10,10,5)
        bullets.add(bala)

class Items(Character):
    def __init__(self,sprite_img,cord_x,cord_y, sprite_width , sprite_height , speed, bonus):
        super().__init__(sprite_img,cord_x,cord_y, sprite_width , sprite_height , speed)
        self.bonus=bonus

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= ALTO:
            self.kill()



class Enemigo(Character):
    def update(self):
        global misses

        self.rect.y+= self.speed
        if self.rect.y>= ALTO:
            self.rect.x = randint(0,ANCHO)
            self.speed= randint(1,6 )
            self.rect.y= -60
            misses+=1

class Bullet(Character):
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y <= 0:
            self.kill()



player= Player(PLAYER_IMG, (ANCHO- 90)//2, (ALTO-90), 90,90,5)


aliens= sprite.Group()
bullets=sprite.Group()
estrellas=sprite.Group()


for i in range(5):
    enemy= Enemigo(ENEMY_IMG, randint(0,ANCHO-140), -60,120,90,randint(1,5))
    aliens.add(enemy)


for i in range(1):
    goodornot= randint(0,2)
    if goodornot==1:
        stars= Items(STARS_IMG,randint(0,ANCHO-90), -60 ,90,90,2,2)
    else:
        stars= Items(BADSTAR,randint(0,ANCHO-90), -60 ,90,90,2,-2)
    
    estrellas.add(stars)

#colisiones estrellas +5, pensar en buffos(aumentar velocidad de la nave temporalmente)


run=True
done= False
clock= time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run= False

        if e.type== KEYDOWN:
            if e.key == K_r:
                done = False
            if e.key == K_SPACE:
                player.shoot()    
        
                
    
    star_spawn -= 1

    if star_spawn <= 0:
        goodornot = randint(0, 2)
        
        if goodornot == 1:
            bonus = 2 
            img = STARS_IMG
        
        else:
            bonus= -2
            img = BADSTAR

        stars = Items(img, randint(0, ANCHO-90), -60, 90, 90, 2, bonus)
        estrellas.add(stars)
        star_spawn = randint(80, 200)
        

    if not done:
        pantalla.blit(background,(0,0))
        player.reset()
        player.update()
        aliens.draw(pantalla)
        aliens.update()
        bullets.draw(pantalla)
        bullets.update()
        estrellas.draw(pantalla)
        estrellas.update()

        puntaje_text= font_1.render(f'Puntaje= {points}', 1 , WHITE)
        puntaje_misses= font_1.render(f'Fallos= {misses}', 1 , WHITE)
        puntaje_vidas= font_1.render(f'Vidas= {lives}', 1 , (170,220,180))

        pantalla.blit(puntaje_vidas,(600,20))
        pantalla.blit(puntaje_text,(20,20))
        pantalla.blit(puntaje_misses,(20,45))

        if sprite.groupcollide(bullets,aliens,True,True):
            pantalla.fill(COLOR)
            points+=5  
            enemy= Enemigo(ENEMY_IMG, randint(0,ANCHO-140), -60,120,90,randint(1,5))
            aliens.add(enemy)
        
        if sprite.spritecollide(player, estrellas, True):
            for star in sprite.spritecollide(player, estrellas, True):
                points += abs(star.bonus) * 5
                player.speed += star.bonus
                print(f"Velocidad: {player.speed}")  # Para debug
    

            goodornot = randint(0, 2)
            if goodornot == 1:
                bonus = 1 
                img = STARS_IMG
            else: 
                bonus = -1
                img = BADSTAR
            stars = Items(img, randint(0, ANCHO-90), -60, 90, 90, 2, bonus)
            estrellas.add(stars)
                

        if sprite.spritecollide(player,aliens, True):
            lives-= 1
            enemy= Enemigo(ENEMY_IMG, randint(0,ANCHO-140), -60,120,90,randint(1,5))
            aliens.add(enemy)

        if lives== 0 or misses==10:
            done=True
            pantalla.fill(BLACK)

            pantalla.blit(lose,(0,0))
        
        if points== 300:
            done=True
            pantalla.fill(BLACK)
            pantalla.blit(winnner,(0,0))          

    display.update()
    clock.tick(FPS)


quit()
