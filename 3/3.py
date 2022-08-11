from operator import truediv
from turtle import width
import pygame,random,sys
pygame.init()

# Initialisations
brown = (205, 127, 50)
gray = (211,211,211)
yellow=(255,255,0)
green = (0, 255, 0)
blue = (0, 0, 128)

size=width,height=1020,700
screen = pygame.display.set_mode(size)

going=True


# Circles Class
class circle(pygame.sprite.Sprite):
    """ Making a circle object """
    
    def __init__(self,x,y,r): # for broken circles
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.r=r
        self.rect=pygame.Rect((x,y),(r,r))
        self.move=[random.randint(3,6),random.randint(3,6)]
    
    def drawobj(self):
        pygame.draw.circle(screen,brown,(self.x,self.y),self.r)

    def update(self):
        if(self.x>width or self.x<0):
            self.move[0]=-self.move[0]
        if(self.y>height or self.y<0):
                self.move[1]=-self.move[1]
        self.x=self.x+self.move[0]
        self.y=self.y+self.move[1]
        self.rect=pygame.Rect((self.x,self.y),(self.r,self.r))
    
    def die(self):
        self.kill()

# Pacman's Class
class pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pac.png')
        self.image = pygame.transform.scale(self.image, (55, 40))
        self.rect = self.image.get_rect()
        self.speed=[7,7]
        self.original=self.image
        self.direction="R"
    
    def draw(self):
        screen.blit(self.image,self.rect)
    
    def die(self):
        self.kill()
    # MOVEMENTS
    def moveup(self):
        rotate = pygame.transform.rotate
        self.rect.move_ip((0,-self.speed[1]))
        self.rect.top=max(0,self.rect.top)
        self.image=rotate(self.original,90)
        self.direction="U"
    
    def moveleft(self):
        rotate = pygame.transform.rotate
        self.rect.move_ip((-self.speed[0],0))
        self.rect.left=max(0,self.rect.left)
        self.image=rotate(self.original,180)
        self.direction="L"
    
    def moveright(self):
        self.image=self.original
        self.rect.move_ip((self.speed[0],0))
        self.rect.right=min(width,self.rect.right)
        self.direction="R"
    
    def movedown(self):
        rotate = pygame.transform.rotate
        self.rect.move_ip((0,self.speed[1]))
        self.rect.bottom=min(height,self.rect.bottom)
        self.image=rotate(self.original,-90)
        self.direction="D"

# Bullet Object
class bullet(pygame.sprite.Sprite):
    def __init__(self,hero):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.jpeg')
        self.image = pygame.transform.scale(self.image, (10, 15))
        self.rect = self.image.get_rect(center=hero.rect.center)
        self.speed=20
        self.direction=hero.direction

    def update(self):
        if(self.direction=='R'):
            self.rect.move_ip(self.speed,0)
        elif(self.direction=='L'):
            self.rect.move_ip(-self.speed,0)
        elif(self.direction=='U'):
            self.rect.move_ip(0,-self.speed)
        elif(self.direction=='D'):
            self.rect.move_ip(0,self.speed)


count=0
all_circles_list = pygame.sprite.Group()
all_circles_list_original=pygame.sprite.Group()
pacman=pacman()
all_bullets_list=pygame.sprite.Group()

for i  in range(10):
    all_circles_list.add(circle(random.randint(10,400),random.randint(20,200),random.randint(5,30)))

while True:
    pygame.time.Clock().tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and going:
            all_bullets_list.add(bullet(pacman))
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and (not going):
            going=True
            pacman.rect=pygame.Rect((0,0),(pacman.rect.w,pacman.rect.h))
            all_circles_list.empty()
            all_bullets_list.empty()
            pacman.image=pacman.original
            for i  in range(10):
                all_circles_list.add(circle(random.randint(10,400),random.randint(20,200),random.randint(5,30)))
            count=0
    
    if going:
        key_input = pygame.key.get_pressed()   
        if key_input[pygame.K_LEFT]:
            pacman.moveleft()
        if key_input[pygame.K_UP]:
            pacman.moveup()
        if key_input[pygame.K_RIGHT]:
            pacman.moveright()
        if key_input[pygame.K_DOWN]:
            pacman.movedown()

    
    screen.fill(gray)
    if going:
        all_circles_list.update()
        all_bullets_list.update()

    if going:
    # Check for collision
        for circleobj in all_circles_list.sprites():
            if pygame.sprite.spritecollideany(circleobj, all_bullets_list):
                count+=1
                if(circleobj.r>8):
                    all_circles_list.add(circle(circleobj.x+1,circleobj.y+1,circleobj.r//2))
                    all_circles_list.add(circle(circleobj.x-1,circleobj.y-1,circleobj.r//2))
                else:
                    all_circles_list.add(circle(circleobj.x+1,circleobj.y+1,30))
                circleobj.die()

    # Check for collision of pacman and circle
        if pygame.sprite.spritecollideany(pacman,all_circles_list):
            going=False
            
    if not going:
            screen.fill(gray)
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('GAME OVER !! Your score is '+str(count)+' .Press R to restart !', True, green, blue)
            textpos = text.get_rect()
            textpos.center=(width//2,height//2)
            screen.blit(text, textpos)

    
    for circleobj in all_circles_list.sprites():
        circleobj.drawobj()
        
    all_bullets_list.draw(screen)
    pacman.draw()
    
    pygame.display.flip()

