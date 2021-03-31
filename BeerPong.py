# -*- coding: utf-8 -*-
import pygame, sys, random, time, math
from pygame import mixer
from pygame.locals import *
import json

pygame.init()
pygame.font.init()
pygame.mixer.init()

# SCREEN
screen_width = 1280
screen_height = 720
vertical_center = screen_height/2
flags = DOUBLEBUF
screen = pygame.display.set_mode((screen_width, screen_height), flags)


white_color = (255, 255, 255)
orange_color = (255, 200, 28)
red_color = (255, 0, 0)
green_color = (0, 255, 0)
black_color = (0, 0, 0)
background_color = (55,53,102)
crosshair_color = (102, 153, 255)


# HighScores {}
highScoreError = False
try:
    with open("json/HighScore.json") as f:
        HighScores = json.load(f)
        highScore = 1000
        keys = list(HighScores.keys())
except:
    highScoreError = True


# FONTS
main_font = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuilight", 35)
main_font_big = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuilight", 84)
main_font_small = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuilight", 28)
main_font_really_small = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuilight", 20)
big_font = pygame.font.SysFont("magneto", 84)
title_font = pygame.font.SysFont("Helvetica", 25, True)
list_font = pygame.font.SysFont("Helvetica", 25)
symbols = pygame.font.SysFont("segoeuisymbol", 84)

# SPRITE AND IMAGE PATHS
ball_path = "images/ball.png"
crosshair_path = "images/hiusristikko.png"
redcup_path = "images/redcup.png"
background_path = "images/beerbong_game_bg.png"
icon_path = "images/BeerPongLogo.png"

# SOUNDS

menumusic = pygame.mixer.music.load('sounds/taustamusiikki.wav')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)
# heitto
throwSound1 = pygame.mixer.Sound('sounds/throw.wav')
throwSound1.set_volume(1.8)
throwSound2 = pygame.mixer.Sound('sounds/raketti.wav')
throwSound2.set_volume(1.3)
#osuma
hitSound1 = pygame.mixer.Sound('sounds/osuma1.wav')
hitSound1.set_volume(1.5)
hitSound2 = pygame.mixer.Sound('sounds/osuma2.wav')
hitSound2.set_volume(1.5)
hitSound3 = pygame.mixer.Sound('sounds/Jerry.wav')
hitSound3.set_volume(1.3)
#ohiheitto
missSound1 = pygame.mixer.Sound('sounds/ohiheitto1.wav')
missSound1.set_volume(1.5)
missSound2 = pygame.mixer.Sound('sounds/ohiheitto2.wav')
missSound2.set_volume(1.5)
#voitto
winSound = pygame.mixer.Sound('sounds/voitto.wav')
winSound.set_volume(1.0)
#häviö
loseSound = pygame.mixer.Sound('sounds/trombone.wav')
loseSound.set_volume(1.0)

hitList = [hitSound1, hitSound2, hitSound3]
missList = [missSound1, missSound2]
throwList = [throwSound1, throwSound2]


#TEXT
main_caption = "Asteriski Beer Pong"


# POWERBAR CLASS
class PowerBar:
    def __init__(self):
        self.decrease_speed = -3
        self.bar_start_width = 3
        self.bar_max_width = 250
        self.bar_pos_x = 130
        self.bar_pos_y = screen_height-50
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

        if self.bar_start_width > 3:
            self.bar_start_width += self.decrease_speed

        elif self.bar_start_width <= 3:
            self.bar_start_width = 3

        if self.bar_start_width < self.bar_max_width * (1/3):
            self.changeColor(green_color)

        elif self.bar_start_width >= self.bar_max_width * (1/3) and self.bar_start_width < self.bar_max_width * (2/3):
            self.changeColor(orange_color)

        elif self.bar_start_width >= self.bar_max_width * (2/3):
            self.changeColor(red_color)
            
        if self.bar_start_width > self.bar_max_width:
            self.x_change = 0

    def reset(self):
        self.x_change = 0
        self.bar_start_width = 3


# TEXT CLASS
class Text:
    def __init__(self, text, font, color, position, center):
        self.text = text
        self.color = color
        self.font = font
        self.position = position
        self.center = center
    
    def drawText(self, screen):
        screen_center = screen.get_rect().center
        self.render = self.font.render(str(self.text), 1, self.color)
        if self.center:
            screen.blit(self.render, (self.position[0] - self.render.get_width()/2, self.position[1]))
        else:
            screen.blit(self.render, (self.position[0], self.position[1]))


# SPRITE CLASSES #

# Ball Class
class Ball(pygame.sprite.Sprite):
    def __init__(self, path, pos_x, pos_y, color, time):
        super().__init__() 
        # Jos kuvaa ei löydy, näytä 30x30 neliö
        self.score = 0
        self.path = path
        self.start_pos_x = pos_x
        self.start_pos_y = pos_x
        self.colot = color
        self.dx = 0
        self.dy = 0
        
        try:
            self.image = pygame.image.load(self.path)
        except:
            self.image = pygame.Surface([30,30]).convert()
            self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.midtop = [self.start_pos_x, self.start_pos_y]
        self.ball_size = self.image.get_size()


    def ball_animation(self):
        self.rect.x = self.rect.x + self.dx
        self.rect.y = self.rect.y + self.dy

    def restart(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dy = 0
        self.dx = 0

    def updateScore(self, points):
        self.score += points

    def getScore(self):
        return self.score

    def resetScore(self):
        self.score = 0
    

class Cups(pygame.sprite.Sprite):
    def __init__(self, path, pos_x, pos_y, color):
        super().__init__()
        
        try:
            self.image = pygame.image.load(path)
        except:
            # Jos kuvaa ei löydy, näytä 40x40 neliö
             self.image = pygame.Surface([40,40]).convert()
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
             self.image = pygame.Surface([30,30]).convert()
             self.image.fill(color)
             
        self.rect = self.image.get_rect()


    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Gameboard(pygame.sprite.Sprite):
    def __init__(self, path, color):
        super().__init__()

        try:
            self.image = pygame.image.load(path)
        except:
             self.image = pygame.Surface([screen_width, screen_height]).convert()
             self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.midtop = [screen_width/2, 0]

class Screen:
    def __init__(self):
        self.caption = main_caption
        self.background = None
        pygame.display.set_caption(self.caption)
        pygame.display.set_icon(pygame.image.load(icon_path))


    def alpha(self, screen):
        s = pygame.Surface((screen_width,screen_height)).convert_alpha()
        s.set_alpha(50)
        s.fill((0,0,0))
        screen.blit(s, (0,0))

    def drawHighScore(self, screen):
        title_label = title_font.render("HighScores: ", 1, (255,255,255))
        screen.blit(title_label,(0.45*screen_width, 5))
        s=1
        y = 30
        count = 0
        if highScoreError:
            list_label = list_font.render("Error Loading Highscore",1,(150,150,150))
            screen.blit(list_label,(0.45*screen_width,y ))
        else:
            for i in range(0,5):
                list_label = list_font.render((str(s)+".    "+(str(keys[i]))),1,(150,150,150))
                screen.blit(list_label,(0.45*screen_width,y ))

                list_label = list_font.render(str(HighScores[keys[i]]),1,(100,255,150))
                screen.blit(list_label,(screen_width/2 + 80, y))
                s += 1
                y += 23

 
    def draw_bg(self, screen):
        # clear screen to black
        screen.fill(background_color)
        if self.background:
            screen.blit(self.background, (0,0))
        else:
            screen.blit(screen, (0,0))


# INIT VARIABLES
player1_start_pos = [screen_width*0.03, vertical_center]
player2_start_pos = [screen_width*0.96, vertical_center]

FPS = 60
fpsOn = True
player1 = True
player2 = False

# SPRITE GROUPS
cup_group_1 = pygame.sprite.Group()
cup_group_2 = pygame.sprite.Group()
player_group = pygame.sprite.Group()
crosshair_group = pygame.sprite.Group()
game_area = pygame.sprite.Group()


# OBEJCTS
power_bar = PowerBar()
window = Screen()
tahtain = Crosshair(crosshair_path, crosshair_color)
gameboard = Gameboard(background_path, background_color)
player_1 = Ball(ball_path, player1_start_pos[0], player1_start_pos[1], white_color, time)
player_2 = Ball(ball_path, player2_start_pos[0], player2_start_pos[1], white_color, time)


#TEXTS OBJECTS
logo_text = Text(main_caption, big_font, orange_color, (screen_width/2, screen_height/2-80), True)
pause_text = Text("PAUSE", symbols, red_color, (screen_width/2, screen_height/2-50), True)
quit_text = Text("Main menu (Q)", main_font, white_color, (screen_width/2, screen_height/2+50), True)
resume_text = Text("Resume (ESC)", main_font, white_color, (screen_width/2, screen_height/2+90), True)
power_text = Text("POWER: ", main_font_small, white_color, (70,screen_height-50), True)
gameover_text = Text("GAME OVER", main_font_big, orange_color, (screen_width/2, screen_height/2-50), True)
newgame_text = Text("New Game (ENTER)", main_font, white_color, (screen_width/2, screen_height/2+50), True)
mute_text = Text("Press m to mute", main_font, black_color, (1100,600), True)
unmute_text = Text("Press n to unmute", main_font, black_color,(1100,650), True)


# ADD CUPS TO GROUP
def createCuplist(x_ofset, reverse, group):
    addToY = 0
    # Lisätään pelaajien mukit omiin listoihin.
    for i in range(4):
        for j in range(4-i):
            y = 264 + (51 * j) + addToY
            if reverse == True:
                x = x_ofset - (44 * i)
            else:
                x = x_ofset + (44 * i)
            group.add(Cups(redcup_path, x, y, red_color))
        addToY += 25


def drawLine(pos1, pos2):
    pygame.draw.line(screen, (255,255,255), pos1, pos2)


def mouseVisible(visible):
    pygame.mouse.set_visible(visible)


# DO INITIAL STUFF BEFORE GAME LAUNCH
def initGame():
    createCuplist(132, False, cup_group_1)
    createCuplist(1148, True, cup_group_2)
    crosshair_group.add(tahtain)
    player_group.add(player_1)
    player_group.add(player_2)
    game_area.add(gameboard)
    player_1.restart((player1_start_pos[0], player1_start_pos[1]))
    player_2.restart((player2_start_pos[0], player2_start_pos[1]))

    main()

def drawScore(screen):
    if player1:
        color1 = orange_color
    else:
        color1 = white_color
    
    if player2:
        color2 = orange_color
    else:
        color2 = white_color

    player1_draw = main_font.render(f"Johannes: {player_1.getScore()}", 1, color1)
    screen.blit(player1_draw,(20, 10))

    player2_draw = main_font.render(f"Milo: {player_2.getScore()}", 1, color2)
    screen.blit(player2_draw,(screen_width-(player2_draw.get_width()+20), 10))

def scoreReset():
    player_1.resetScore()
    player_2.resetScore()
    
# PAUSE 
def pauseGame():
    mouseVisible(True)
    window.alpha(screen) 
    pause_text.drawText(screen)
    resume_text.drawText(screen)
    quit_text.drawText(screen)


#GAME OVER
def gameOver():
    quit_text = Text("Main menu (Q)", main_font, white_color, (screen_width/2, screen_height/2+90), True)
    mouseVisible(True)
    window.alpha(screen)
    gameover_text.drawText(screen)
    newgame_text.drawText(screen)
    quit_text.drawText(screen)




def main():
    # MAIN STRUCTURE
    clock = pygame.time.Clock()
    player_1.restart((player1_start_pos[0], player1_start_pos[1]))
    player_2.restart((player2_start_pos[0], player2_start_pos[1]))
    power_bar.reset()
    
    global player1, player2
    run = True
    isGameover = False
    pause = False
    ballMove = False
    previousXPos1 = 0
    previousXPos2 = 1280
    time = 0

    while run:
        mousePos = pygame.mouse.get_pos()
        # DRAWS    
        window.draw_bg(screen)
        game_area.draw(screen)        
        cup_group_1.draw(screen)
        cup_group_2.draw(screen)
        player_group.draw(screen)
        power_bar.drawBar(screen)
        window.drawHighScore(screen)
        drawScore(screen)
        power_text.drawText(screen)
        mute_text.drawText(screen)
        unmute_text.drawText(screen)
        fps_text = Text(f"{round(clock.get_fps(),0)} FPS", main_font_small, orange_color,(screen_width/2,680), True)
        if fpsOn:
            fps_text.drawText(screen)

        # COLLIDE DETECTION
        if pygame.sprite.spritecollide(player_1, cup_group_2, True):
            rect1 = player_1
            rect2 = cup_group_2
            if len(cup_group_2) <= 0:
                player_1.updateScore(50)
                isGameover = True
                pygame.mixer.Sound.play(winSound)
            else:
                player_1.updateScore(10)
                player1 = False
                player2 = True   
                idx = random.randint(0,2)
                pygame.mixer.Sound.play(hitList[idx])                      
                main()

        elif pygame.sprite.spritecollide(player_2, cup_group_1, True):
            if len(cup_group_1) <= 0:
                player_2.updateScore(50)
                isGameover = True   
                pygame.mixer.Sound.play(loseSound)
            else:
                player_2.updateScore(10)
                player1 = True
                player2 = False
                idx = random.randint(0,2)
                pygame.mixer.Sound.play(hitList[idx])                           
                main()               

        # KEY EVENTIT
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Pause on ESC
                if event.key == pygame.K_ESCAPE:
                    if not isGameover:
                        pause = not pause
                # 'HARD RESET'
                if event.key == ord('f'):
                    player1 = True
                    player2 = False                          
                    initGame()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not pause and not isGameover:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not ballMove: # 1 = left click
                        ballMove = True
                        idz = random.randint(0,1)
                        pygame.mixer.Sound.play(throwList[idz])

                elif event.type == pygame.KEYDOWN:   
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == ord('a') or event.key == ord('d'):
                        power_bar.x_change = 5
                    elif event.key == pygame.K_m:
                        pygame.mixer.music.pause()
                    elif event.key == pygame.K_n:
                        pygame.mixer.music.unpause()   

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == ord('a') or event.key == ord('d'):
                        power_bar.x_change = 0 
            elif pause:
                if event.type == pygame.KEYDOWN:
                    # Go to main menu
                    if event.key == ord('q'):
                        scoreReset()
                        player1 = True
                        player2 = False                           
                        game_menu()
            elif isGameover:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        scoreReset()
                        player1 = True
                        player2 = False     
                        initGame()
                    elif event.key == ord('q'):
                        scoreReset()
                        player1 = True
                        player2 = False                            
                        game_menu()
  
        
        # UPDATES JA MUUTA
        if not pause:
            mouseVisible(False)
            if ballMove:
                speed = power_bar.bar_start_width/4
                time += 0.04

                if player1 and not isGameover:
                    player_1.ball_animation()
                    angle = math.atan2((mousePos[1])-player1_start_pos[1], (mousePos[0])-player1_start_pos[0])
                    

                    if player_1.rect.x > previousXPos1:
                        player_1.dx = (speed * math.cos(angle)) + (-9.81* (time)**2)
                        player_1.dy = speed * math.sin(angle)
                        previousXPos1 = player_1.rect.x
                    else:
                        pygame.mixer.Sound.play(missSound1)
                        pygame.time.wait(2000)                       
                        player1 = False
                        player2 = True                           
                        main()
                    
                elif player2 and not isGameover:
                    player_2.ball_animation()

                    angle = math.atan2((mousePos[1])-player2_start_pos[1], (mousePos[0])-player2_start_pos[0])


                    if player_2.rect.x < previousXPos2:
                        player_2.dx = (speed * math.cos(angle)) + (9.81* (time)**2)
                        player_2.dy = (speed * math.sin(angle))
                        previousXPos2 = player_2.rect.x
                    else:
                        pygame.mixer.Sound.play(missSound1)
                        pygame.time.wait(2000)
                        player1 = True
                        player2 = False                                                     
                        main()
 
            else:
                crosshair_group.draw(screen)
                cup_group_1.update()
                cup_group_2.update()
                crosshair_group.update()
                player_group.update()
                power_bar.barAnimation()

        elif pause and not isGameover:
            pauseGame()

        if isGameover:
            ballMove = False
            gameOver()

        pygame.display.update()
        clock.tick(FPS)

# MAINMENU        
def game_menu():
    clock = pygame.time.Clock()
    while True:
        fps_text = Text(f"{round(clock.get_fps(),0)} FPS", main_font_small, orange_color,(screen_width/2,680), True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 

            elif event.type == pygame.KEYDOWN:
                # ENTER to restart
                if event.key == pygame.K_RETURN:
                    initGame()

        window = Screen()
        window.draw_bg(screen)
        logo_text.drawText(screen)
        newgame_text.drawText(screen)
        if fpsOn:
            fps_text.drawText(screen)
            
        pygame.display.update()
        clock.tick(FPS)   
game_menu()