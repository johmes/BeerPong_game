import pygame, sys, random, time, math
from pygame import mixer

pygame.display.init()
pygame.mixer.init(44100, -16,2,2048)
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 40)

speedY = random.uniform(-0.05,0.05)

def ball_restart(speed_x, speed_y, pos_x):
    global ball_speed_x, ball_speed_y
    ball.center = (pos_x, screen_height/2)
    ball_speed_y += speed_y
    ball_speed_x += speed_x

def ball_animation():
    if play == True:
        global ball_speed_x, ball_speed_y
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y *= -1
        if ball.left <= 0:
            ball_speed_x *= -1
        if ball.right >= screen_width:
            ball_speed_x *= -1
        

#colors
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)
white_color = (255,255,255)
cup_color = (220,20,60)

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode(size=(screen_width, screen_height), flags=0, depth=0, display=0, vsync=0)
pygame.display.flip()

background_image = pygame.image.load("beerbong_game_bg_color.jpg").convert()
pygame.display.set_caption('Beer Pong')

#Ball configurations
ball_speed_x = 5
ball_speed_y = 0 #speedY
ball_width = 21
ball_height = 21
play = False

#Cup configuration
cup_width = 37
cup_height = 37

#score
score1 = 0

#Num of Red Cups
# player1Cups = 10
# player2Cups = 10

# cups1 = []
# cups2 = []

# class Cup:
#     def __init__(self, x, y):
#         self.x, self.y = x, y
#         self.width, self.height = ball_width, ball_height

# for row in range(player1Cups):
#     cups1.append(Cup(row * (5+ball_width), row*30))
#     print(cups1)

ball = pygame.Rect(100, screen_height/2 - 10.5, ball_width, ball_height)
screen, cup_color, (100, screen_height/2), (screen_width/1.5,screen_height/2)


def draw(self,screen):
    luku = 4
    coord1 = (screen_width-188)
    coord2 = (screen_height/2-74)
    row = 0
    for x in range(self.lines):
        row += 40
        for rivi in range(luku):
            BFRC = pygame.Rect(coord1, coord2, cup_width, cup_height)
            pygame.draw.ellipse(screen,cup_color,BFRC)
            coord1 -= 34
            coord2 += 20
        luku -= 1
        coord1 = (screen_width-188)
        coord2 = (screen_height/2-74) + row

boid = []

#the class
class Boid:
    def __init__(self, screen):
        self.screen = screen
        self.pos = pygame.math.Vector2((screen_width-289), (screen_height/2-74))
        self.rad = 20
        self.speed = pygame.math.Vector2(-4, -4)
        self.lines = 4
        self.boid = []

    def draw(self):
        luku = 4
        row = 0
        for x in range(self.lines):
            row += 40
            for rivi in range(luku):
                pygame.draw.circle(self.screen, cup_color, (self.pos.x, self.pos.y), self.rad)
                self.boid.append([self.pos.x, self.pos.y, self.rad])
                self.pos.x -= 34
                self.pos.y += 20
            luku -= 1
            self.pos.x = (screen_width-188)
            self.pos.y = (screen_height/2-74) + row

boidList = Boid(screen).boid

boidList = boid



while True:
    #Handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space toimii")
                play = True
            # if event.key == pygame.K_UP:
            #     #TODO...
            # if event.key == pygame.K_DOWN:
            #     #TODO...
    
    ball_animation()
    #visuals
    screen.blit(background_image, [0, 0])
    for boid in boidList:
        boid.draw()
    pygame.draw.ellipse(screen, white_color, ball) 
    pygame.display.flip()
    clock.tick(60)