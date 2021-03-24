import pygame, sys, random, time, math, os
from pygame import mixer
import json

pygame.init()
pygame.font.init()
pygame.mixer.init()

# SCREEN
screen_width = 1280
screen_height = 720
vertical_center = screen_height/2
screen = pygame.display.set_mode(size=(screen_width, screen_height), flags=0, depth=0, display=0, vsync=0)

white_color = (255, 255, 255)
orange_color = (255, 200, 28)
red_color = (255, 0, 0)
green_color = (0, 255, 0)
black_color = (0, 0, 0)
background_color = (55,53,102)
crosshair_color = (102, 153, 255)

# HighScores {}
f = open("BeerPong_game/HighScore.json",)
HighScores = json.load(f)

current_score = 0
highScore = 1000
keys = list(HighScores.keys())
main_font = pygame.font.SysFont("Helvetica", 35)
big_font = pygame.font.SysFont("Helvetica", 84)

# SOUNDS
# hit = pygame.mixer.Sound('BeerPong_game/punch_2.wav')
#TEXTS
main_caption = "Asteriski Beer Pong"
menuRun = True
# MAINMENU
# while menuRun:
#     s = pygame.Surface((screen_width,screen_height))
#     s.fill(background_color)
#     screen.blit(s, (0,0))

#     # KEY EVENTIT
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit() 
        
#         if event.type == pygame.KEYDOWN:
#                 # ENTER to restart
#                 if event.key == pygame.K_RETURN:
#                     menuRun = False
#     pygame.display.update()

# THE GAME
# SPRITE AND IMAGE PATHS
ball_path = "BeerPonfg_game/ball.png"
crosshair_path = "BeegrPong_game/hiusristikko.png"
redcup_path = "BeerPongg_game/redcup.png"
background_path = "BeerPong_ggame/beerbong_game_bg.png"


# Cups
cups_1 = []
cups_2 = []


def mouseVisible(visible):
    pygame.mouse.set_visible(visible)

# Ball Class
class Ball(pygame.sprite.Sprite):
    def __init__(self, path, pos_x, pos_y, color, time):
        super().__init__() 
        # Jos kuvaa ei löydy, näytä 30x30 neliö
        try:
            self.image = pygame.image.load(path)
        except:
             self.image = pygame.Surface([30,30])
             self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.midtop = [pos_x, pos_y]
        self.ball_size = self.image.get_size()

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dx = 0
        self.dy = 0

    def ball_animation(self):
        self.rect.x = self.rect.x + self.dx
        self.rect.y = self.rect.y + self.dy

    def restart(self):
        self.dx = 0
        self.dy = 0
        self.rect.x = self.ball_start_pos[0]
        self.rect.y = self.ball_start_pos[1]


class Text:
    def __init__(self, text, font, color, position):
        self.text = text
        self.color = color
        self.position = position
        self.font = font
    
    def drawText(self, screen):
        self.text_render = self.font.render(self.text, True, self.color)

        screen.blit(self.text_render, self.position)


class PowerBar:
    def __init__(self):
        self.decrease_speed = -3
        self.bar_start_width = 0
        self.bar_max_width = 250
        self.bar_pos_x = 130
        self.bar_pos_y = 20
        self.bar_height = 35
        self.bar_color = None
        self.x_change = 0

        self.changeColor(green_color)

    def changeColor(self, color):
        self.bar_color = color
    
    # Piirretään power bar pohja
    def drawBar(self, screen):
        pygame.draw.rect(screen, self.bar_color, (self.bar_pos_x, self.bar_pos_y, self.bar_start_width, self.bar_height))
        
        #border for power bar
        pygame.draw.rect(screen, black_color, (self.bar_pos_x, self.bar_pos_y, self.bar_max_width, self.bar_height), 1)

        
    def barAnimation(self):
        self.bar_start_width += self.x_change

        if self.bar_start_width > 0:
            self.bar_start_width += self.decrease_speed

        if self.bar_start_width <= 0:
            self.bar_start_width = 3

        if self.bar_start_width < self.bar_max_width * (1/3):
            self.changeColor(green_color)

        if self.bar_start_width >= self.bar_max_width * (1/3):
            self.changeColor(orange_color)

        if self.bar_start_width >= self.bar_max_width * (2/3):
            self.changeColor(red_color)
            
        if self.bar_start_width > self.bar_max_width:
            self.x_change = 0

# SPRITE CLASS
class Cups(pygame.sprite.Sprite):
    def __init__(self, path, pos_x, pos_y, color):
        super().__init__()
        
        try:
            self.image = pygame.image.load(path)
        except:
            # Jos kuvaa ei löydy, näytä 40x40 neliö
             self.image = pygame.Surface([40,40])
             self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.midtop = [pos_x, pos_y]

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, path, color):
        super().__init__()

        try:
            self.image = pygame.image.load(path)
            self.rect = self.image.get_rect()
        except:
             self.image = pygame.Surface([30,30])
             self.image.fill(color)
             
        self.rect = self.image.get_rect()


    def update(self):
        self.rect.center = pygame.mouse.get_pos()


def createCuplist(x_ofset, reverse, list):
    addToY = 0
    # Lisätään pelaajien mukit omiin listoihin.
    for i in range(4):
        for j in range(4-i):
            y = 264 + (51 * j) + addToY
            if reverse == True:
                x = x_ofset - (44 * i)
            else:
                x = x_ofset + (44 * i)
            list.append(Cups(redcup_path, x, y, red_color))
        addToY += 25

def drawLine(pos1, pos2):
    pygame.draw.line(screen, (255,255,255), pos1, pos2)

class Button:
    def __init__(self, width, height, x, y, color, text):
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.color = color
        self.text = text

        self.button = pygame.Rect(self.width, self.height, x, y)

    def drawButton(self, screen):
        pygame.draw.rect(screen, self.color, self.button)

class Screen:
    def __init__(self):
        self.caption = main_caption
        self.background = None
        pygame.display.set_caption(self.caption)
        
        self.set_background(background_path)

        # ISO PAUSE TEKSTI PUNASELLA
        font = pygame.font.SysFont("", 84)
        self.pause_text = font.render("PAUSE", True, red_color)

        # TASOITA TEKSTI KESKELLE
        screen_center = screen.get_rect().center
        self.pause_text_rect = self.pause_text.get_rect(center=screen_center, x= screen_width/2-113, y = screen_height/2-43)
    
    

    main_font = pygame.font.SysFont("Helvetica", 35)

    def alpha(self, screen):
        s = pygame.Surface((screen_width,screen_height))
        s.set_alpha(50)
        s.fill((0,0,0))
        screen.blit(s, (0,0))

    def drawHighScore(self, screen):
        title_font = pygame.font.SysFont("Helvetica",25,True)
        list_font = pygame.font.SysFont("Helvetica",25)
        title_label = title_font.render("HighScores: ",1,(255,255,255))
        screen.blit(title_label,(0.60*screen_width, 5))
        s=1
        y = 30
        for i in range(0,5):
            list_label = list_font.render((str(s)+".    "+(str(keys[i]))),1,(150,150,150))
            screen.blit(list_label,(0.60*screen_width,y ))
            list_label = list_font.render(str(HighScores[keys[i]]),1,(100,255,150))
            screen.blit(list_label,(0.75*screen_width,y ))
            s += 1
            y += 23


    def draw_bg(self, screen):
        # clear screen to black
        screen.fill(background_color)
        if self.background:
            screen.blit(self.background, (0,0))
        
        #Score teksti
        score_label = main_font.render(f"Score: {current_score} ",1,(255,255,255))
        screen.blit(score_label, (screen_width/2 -score_label.get_width()/2,10))
    
    def set_background(self, img=None):
        if img: 
            try:
                self.background = pygame.image.load(img)
            except:
                self.background = pygame.Surface([screen_width,screen_height])
                self.background.fill(background_color)


def main():
    # MAIN STRUCTURE
    clock = pygame.time.Clock()

    FPS = 60
    run = True
    pause = False
    ballMove = False
    player1 = True
    player2 = False
    drunk = False
    time = 0
    previousXPos = 0
    previousYPos = 0
    cup_group_1 = pygame.sprite.Group()
    cup_group_2 = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    crosshair_group = pygame.sprite.Group()
    player1_start_pos = [screen_width*0.03, vertical_center]
    player2_start_pos = [screen_width*0.96, vertical_center]
    mousePos = pygame.mouse.get_pos()


    # OBEJCTS
    power_bar = PowerBar()
    window = Screen()
    createCuplist(132, False, cups_1)
    createCuplist(1148, True, cups_2)
    tahtain = Crosshair(crosshair_path, crosshair_color)
    
    player_1 = Ball(ball_path, player1_start_pos[0], player1_start_pos[1], white_color, time)
    player_2 = Ball(ball_path, player2_start_pos[0], player2_start_pos[1], white_color, time)

    #TEXTS
    pause_text = Text("PAUSE", big_font, red_color, window.pause_text_rect.topleft)
    power_text = Text("POWER: ", main_font, white_color, (10,20))

    # SPRITE GROUPS
    for cup in cups_1:
        cup_group_1.add(cup)
    for cup in cups_2:
        cup_group_2.add(cup)
    crosshair_group.add(tahtain)
    player_group.add(player_1)
    player_group.add(player_2)

    while run:
        if pygame.sprite.spritecollide(player_1, cup_group_2, True):
            print("Hit")

        elif pygame.sprite.spritecollide(player_2, cup_group_1, True):
            print("Hit")

        # KEY EVENTIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 

            if event.type == pygame.KEYDOWN:
                # Pause on ESC
                if event.key == pygame.K_ESCAPE:
                    pause = not pause

            if not pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not ballMove: # 1 = left click
                        ballMove = True
            
                elif event.type == pygame.KEYDOWN:
                    # ENTER to restart
                    if event.key == pygame.K_RETURN:
                        main()

                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == ord('a') or event.key == ord('d'):
                        power_bar.x_change = 5   

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == ord('a') or event.key == ord('d'):
                        power_bar.x_change = 0

        
        # DRAWS
        window.draw_bg(screen)
        cup_group_1.draw(screen)
        cup_group_2.draw(screen)
        player_group.draw(screen)
        power_bar.drawBar(screen)
        power_text.drawText(screen)
        window.drawHighScore(screen)
        
        
        # UPDATES JA MUUTA
        if not pause:
            mouseVisible(False)
            if ballMove:
                speed = power_bar.bar_start_width/10
                if player1:
                    time += 0.17 
                    if drunk:
                        deviationY = 100 * random.random() * ((-0.71) - 0.71) + 0.71
                        deviationX = 100 * random.random() * ((-0.41) - 0.71) + 0.41
                    else: 
                        deviationX = 0
                        deviationY = 0

                    angle = math.atan2((mousePos[1]+deviationY)-player1_start_pos[1], (mousePos[0]+deviationX)-player1_start_pos[0])
                    
                    # Täällä on joku random ongelma plz auttakaa
                    # player_1.dx = speed * math.cos(angle)
                    # player_1.dy = speed * math.sin(angle)

                    if player_1.rect.x > previousXPos:
                        player_1.dx = (math.cos(angle) * speed * time) + ((-4.81 * (time)**2)/2)
                        player_1.dy = math.sin(angle) * speed
                        previousXPos = player_1.rect.x
                    else:
                        pygame.time.wait(1000)
                        main()
                    # Ongelma loppuu tähän ...toisibn sanoen se on koko tähtäys mekanismi.

                    player_1.ball_animation()
 
            else:
                crosshair_group.draw(screen)
                cup_group_1.update()
                cup_group_2.update()
                crosshair_group.update()
                player_group.update()
                power_bar.barAnimation()

        elif pause:
            # draw pause text
            mouseVisible(True)
            Button(screen_width/2-100, screen_height/2+50, 200, 50, red_color, "EXIT GAME").drawButton(screen)
            window.alpha(screen)
            pause_text.drawText(screen)
        pygame.display.update()
        clock.tick(FPS) 
main()