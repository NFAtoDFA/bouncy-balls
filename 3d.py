import random
import math
import pygame

pygame.init()

height =   700 #600
width = 1200 #900
border = 175
balls = 1000
fps = 60

#abilities
freezetime = 2 #in seconds
scantime = 1
scanDuration = 1

#and their cooldowns
freeze_cooldown = 5
scan_cooldown = 5
shapeshift_cooldown = 3
dribble_cooldown = 0.5
teleport_cooldown = 10

#visual
scan_op_max = 30

#colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
#button colors
button_col = (70,70,70)
button_col_pressed = (90,90,90)
#player colors
player_mouse_col = (200,100,100)
player_key_col = (100,170,170)
button_col_margin = 2


display = pygame.display.set_mode((width,height))
icon = pygame.image.load('ballsIcon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('hopefully 3d')
clock = pygame.time.Clock()

def wp_to_sp(x,y,z):
    res_screen_x = x 
    res_screen_y = y - z

    return [res_screen_x, res_screen_y]

class button:
    def __init__(self,name,description,cooldown):
        self.name = name
        self.dsc = description
        self.x = 0
        self.y = 0 
        self.height = 0
        self.width = 0
        self.font = pygame.font.SysFont(None,25)
        self.text = self.font.render(name,True,(220,220,220))
        if not self.dsc == 'none':
            self.small = pygame.font.SysFont(None, 15)
            self.smallText = self.small.render('press ' + self.dsc, True, (220,220,220) )
            self.textW, self.textH = self.small.size('press ' + self.dsc)
        self.pressed = True
        self.cd = cooldown
        self.timer = pygame.time.get_ticks()
    
    def press(self):
        self.pressed = True
        self.timer = pygame.time.get_ticks()

    def draw(self):
        if self.pressed == False:
            if self.dsc == 'none':
                pygame.draw.rect(display,player_mouse_col,pygame.Rect(self.x - button_col_margin, self.y - button_col_margin, self.width + 2* button_col_margin, self.height + 2 * button_col_margin))
            else:
                pygame.draw.rect(display,player_key_col,pygame.Rect(self.x - button_col_margin, self.y - button_col_margin, self.width + 2* button_col_margin, self.height + 2 * button_col_margin))
 

        pygame.draw.rect(display,button_col,pygame.Rect(self.x,self.y,self.width,self.height))
        if self.pressed == True:
            pygame.draw.rect(display,button_col_pressed,pygame.Rect(self.x,self.y,self.width - self.width * ((pygame.time.get_ticks() - self.timer) / 1000) / self.cd,self.height))
            if (pygame.time.get_ticks() - self.timer) / 1000 >= self.cd:
                self.pressed = False
        display.blit(self.text,(self.x + 5,self.y + 5))
        if not self.dsc == 'none':
            display.blit(self.smallText,(self.x + self.width - self.textW - 3,self.y + self.height - self.textH - 3))

    
    def check_pressed(self,pos):
        if pos[0] >= self.x and pos[0] <= self.x + self.width and pos[1] >= self.y and pos[1] <= self.y + self.height :
            return True

    def action(self):
        if self.pressed == False:
            self.press()
            match self.name:
                case 'freeze':
                    start_freeze()
                case 'scan':
                    start_scan()
                case 'shapeshift':
                    shapeshift()
                case 'dribble':
                    dribble()
                case 'teleport':
                    teleport(spheres)
            
def start_freeze():
    global freeze, freezetimer
    if freeze == False:
        freeze = True
        freezetimer = pygame.time.get_ticks()

def start_scan():
    global scantimer, scan
    if scan == False and scanned == False:
        scan = True           
        scantimer = pygame.time.get_ticks()

def shapeshift():
    for sphere in spheres:
        if sphere.player == True:
            sphere.reset()

def teleport(spheres):
    for sphere in spheres:
        if sphere.player == True:
            sphere.x = random.randint(border, width - border)
            sphere.y = random.randint(border, height - border)

def dribble():
    for sphere in spheres:
        sphere.big_bounce()

def position_buttons(buttons, x_space, y_space, align):
    global height, width, border
    for i,button in enumerate(buttons):
        button.height = (height - 2*border - len(buttons) * y_space) / len(buttons)
        button.width = border - 2*x_space
        if align == 'left':
            button.x = 0 + x_space
        else:
            button.x = width - button.width - x_space
        button.y = border + i * (y_space + button.height)
        button.draw()

class sphere:
    def __init__(self,x,y,z,radius,color):
        self.x = x
        self.y = y
        self.z = z
        self.r = radius
        self.c = color
        self.speed = 0
        self.xdir = random.randrange(-2.0,2.0)
        self.ydir = random.randrange(-2.0,2.0)
        self.player = False
    
    def draw(self):
        if self.player:
            if found == True:
                    pygame.draw.circle(display, red, wp_to_sp(self.x,self.y,self.z), self.r + 3)
            pygame.draw.circle(display, self.c, wp_to_sp(self.x + width,self.y,self.z), self.r)
            pygame.draw.circle(display, self.c, wp_to_sp(self.x - width,self.y,self.z), self.r)
            pygame.draw.circle(display, self.c, wp_to_sp(self.x,self.y - height,self.z), self.r)
            pygame.draw.circle(display, self.c, wp_to_sp(self.x,self.y + height,self.z), self.r)


        pygame.draw.circle(display, self.c, wp_to_sp(self.x,self.y,self.z), self.r)

    def draw_shadow(self):
        pygame.draw.ellipse(display, (40,40,40), pygame.Rect(wp_to_sp(self.x - self.r, self.y + self.r*0.5,0),(self.r*2,self.r)))
       
    def gravity(self):
        self.z -= self.speed
        self.speed += 0.2 * (self.r*self.r / 900)
        if self.z <= 1:
            self.speed *= -0.95
            self.z = 1
       
    def reset(self):
        self.c = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
        self.r = random.randint(20,30)
        self.z = random.randint(10,50)

    def move(self):
        if self.player:
            self.x += keys[3] - keys[2]
            self.y += keys[1] - keys[0]
            if self.y <= 0:
                self.y = height
            if self.y > height:
                self.y = 1
            if self.x <= 0:
                self.x = width
            if self.x > width:
                self.x = 1
        elif scanned == False:
            if self.x <= border or self.x >= width - border:
                self.xdir *= -1
            if self.y <= border or self.y >= height - border:
                self.ydir *= -1
            self.x += self.xdir * 1.0
            self.y += self.ydir * 1.0

    def collision(self, pos):
        cords = wp_to_sp(self.x,self.y,self.z)
        box = pygame.Rect(cords[0] - self.r,cords[1]-self.r,self.r*2, self.r*2)
        if box.collidepoint(pos):
            return True
        return False
    
    def big_bounce(self):
        self.speed = abs(self.speed)

class camera:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

spheres = list()

for i in range(balls):
    spheres.append(sphere(random.randint(border,width - border),random.randint(border,height- border),random.randint(0,100),random.randint(20,30),(random.randint(100,255),random.randint(100,255),random.randint(100,255))))

spheres[balls - 1].player = True

bottens = list()
bottens.append(button('freeze','left Alt',freeze_cooldown))
bottens.append(button('shapeshift','Y',shapeshift_cooldown))
bottens.append(button('teleport','X',teleport_cooldown))
bottens.append(button('testKraft','Z',3))
#bottens.append(button('test1','2',15))

bottens_r = list()
bottens_r.append(button('scan','none',scan_cooldown))
bottens_r.append(button('dribble','none',dribble_cooldown))
bottens_r.append(button('maustest','none',1))
#bottens_r.append(button('test2','none',3))

freezetimer = 0
freeze = False
frozenscreen = pygame.image.load('frozenscreen.png')
frozenscreen.convert()

found = False

keys = [0,0,0,0]

scan = False
scanned = False
scanDurationTimer = 0
green = pygame.Surface((width,height))

got = 0
outof = balls
font = pygame.font.SysFont(None, 24)

def main_loop():
    exitProgram = False
    global scan,scanned,scanDuration, scanDurationTimer, scantimer, scantime,  freeze, freezetimer, freezetime, found, got, outof 

    while not exitProgram:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitProgram = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i,sphere in enumerate(spheres):
                    if sphere.collision(pos):
                        if sphere.player == False:
                            spheres.pop(i)
                            outof -= 1
                        else:
                            #found = True
                            spheres.pop(i)
                            outof -= 1
                            if not outof ==  0:
                                spheres[random.randint(0,outof-1)].player = True
                            got += 1
                for botten in bottens_r:
                    if botten.check_pressed(pos):
                        botten.action()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    keys[0] = 1
                if event.key == pygame.K_DOWN:
                    keys[1] = 1
                if event.key == pygame.K_LEFT:
                    keys[2] = 1
                if event.key == pygame.K_RIGHT:
                    keys[3] = 1
                if event.key == pygame.K_x:
                    for button in bottens:
                        if button.name == 'teleport':
                            button.action()
                if event.key == pygame.K_s:
                    for button in bottens_r:
                        True
                if event.key == pygame.K_LALT:
                    for button in bottens:
                        if button.name == 'freeze':
                            button.action()
                if event.key == pygame.K_z:
                    for button in bottens:
                        if button.name == 'testKraft':
                            button.action()
                if event.key == pygame.K_y:
                    for button in bottens:
                        if button.name == 'shapeshift':
                            button.action()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    keys[0] = 0
                if event.key == pygame.K_DOWN:
                    keys[1] = 0
                if event.key == pygame.K_LEFT:
                    keys[2] = 0
                if event.key == pygame.K_RIGHT:
                    keys[3] = 0

        display.fill((60,60,60))
        score = font.render('Score : ' + str(got) + ' / ' + str(outof), True, (210,210,210))
        #sort the spheres by their y value
        spheres.sort(key=lambda x: x.y, reverse=False)

        for sphere in spheres:
            sphere.draw_shadow()

        #pygame.draw.rect(display,(200,0,0),pygame.Rect(border,border,width - border * 2 + 30, height - border * 2 + 30),2)  
        
        display.blit(score, (20,20))
        position_buttons(bottens,20,20,'left')
        position_buttons(bottens_r,20,20,'right')


        for sphere in spheres:
            sphere.draw()
            sphere.move()
            if sphere.player == False:
                if freeze == False:
                        sphere.gravity()
                else:
                    if (pygame.time.get_ticks() - freezetimer) / 1000 > freezetime:
                        freeze = False
            #sphere.z += random.randint(-1,2)
        if freeze == True:
            frozenscreen.set_alpha(math.sin(math.pi * 0.5 * ((pygame.time.get_ticks() - freezetimer) / 1000)) * 225) 
            display.blit(frozenscreen,(0,0))
            frozentext = font.render('Slow-Mo',True, (220,220,220))
            frozenscreen.blit(frozentext,(width/2 - 40,height - border + 30))
            

        if scan == True:
            #print('scanning')
            green.set_alpha(((math.cos((math.pi* 4 * ((pygame.time.get_ticks() - scantimer) / 1000))) + 1) * 0.5) * scan_op_max)
            green.fill((0,255,0))
            display.blit(green, (0,0))
            if (pygame.time.get_ticks() - scantimer) / 1000 >= scantime:
                scantimer = 0
                scan = False
                scanDurationTimer = pygame.time.get_ticks()
                scanned = True

        if scanned == True:
            green.set_alpha(scan_op_max)
            green.fill((0,255,0))
            display.blit(green,(0,0))
            if (pygame.time.get_ticks() - scanDurationTimer) / 1000 >= scanDuration:
                scanDurationTimer = 0
                scanned = False
        
        pygame.display.update()
        clock.tick(fps)
main_loop()
pygame.quit()
quit()
