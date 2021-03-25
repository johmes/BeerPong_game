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


# FONTS
keys = list(HighScores.keys())
main_font = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuilight", 35)
main_font_big = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuilight", 84)
main_font_small = pygame.font.SysFont("microsoftyaheimicrosoftyaheiuilight", 28)
big_font = pygame.font.SysFont("magneto", 84)
title_font = pygame.font.SysFont("Helvetica",25,True)
list_font = pygame.font.SysFont("Helvetica",25)

# SPRITE AND IMAGE PATHS
ball_path = "BeerPong_game/images/ball.png"
crosshair_path = "BeerPong_game/images/hiusristikko.png"
redcup_path = "BeerPong_game/images/redcup.png"
background_path = "BeerPong_game/images/beerbong_game_bg.png"

# SOUNDS

#TEXTS
main_caption = "Asteriski Beer Pong"
title_label = title_font.render("HighScores: ", True, (255,255,255))


# THE GAME

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

        self.start_pos_x = pos_x
        self.start_pos_y = pos_x
        self.dx = 0
        self.dy = 0

    def ball_animation(self):
        self.rect.x = self.rect.x + self.dx
        self.rect.y = self.rect.y + self.dy

    def restart(self, pos):
        
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dy = 0
        self.dx = 0

# POWERBAR CLASS
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
    def reset(self):
        self.x_change = 0
        self.bar_start_width = 3
# TEXT CLASS
class Text:
    def __init__(self, text, font, color, position):
        self.text = text
        self.color = color
        self.font = font
        self.position = position
    
    def drawText(self, screen):
        screen_center = screen.get_rect().center
        self.render = self.font.render(self.text, True, self.color)
        screen.blit(self.render, (self.position[0] - self.render.get_width()/2, self.position[1]))


# SPRITE CLASSES
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

    def alpha(self, screen):
        s = pygame.Surface((screen_width,screen_height))
        s.set_alpha(50)
        s.fill((0,0,0))
        screen.blit(s, (0,0))

    def drawHighScore(self, screen):
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
        score_label = Text(f"Score: {current_score} ", main_font, white_color, (screen_width/2, 10))
        score_label.drawText(screen)
    
    def set_background(self, img=None):
        if img: 
            try:
                self.background = pygame.image.load(img)
            except:
                self.background = pygame.Surface([screen_width,screen_height])
                self.background.fill(background_color) 


# INIT VARIABLES
FPS = 60
player1_start_pos = [screen_width*0.03, vertical_center]
player2_start_pos = [screen_width*0.96, vertical_center]


# SPRITE GROUPS
cup_group_1 = pygame.sprite.Group()
cup_group_2 = pygame.sprite.Group()
player_group = pygame.sprite.Group()
crosshair_group = pygame.sprite.Group()


# OBEJCTS
power_bar = PowerBar()
window = Screen()
tahtain = Crosshair(crosshair_path, crosshair_color)
player_1 = Ball(ball_path, player1_start_pos[0], player1_start_pos[1], white_color, time)
player_2 = Ball(ball_path, player2_start_pos[0], player2_start_pos[1], white_color, time)


#TEXTS OBJECTS
logo_text = Text(main_caption, big_font, orange_color, (screen_width/2, screen_height/2-80))
pause_text = Text("PAUSE", main_font_big, red_color, (screen_width/2, screen_height/2-50))
quit_text = Text("Main menu (Q)", main_font, white_color, (screen_width/2, screen_height/2+50))
resume_text = Text("Resume (ESC)", main_font, white_color, (screen_width/2, screen_height/2+90))
power_text = Text("POWER: ", main_font_small, white_color, (70,20))
gameover_text = Text("GAME OVER", main_font_big, orange_color, (screen_width/2, screen_height/2-50))
newgame_text = Text("New Game (ENTER)", main_font, white_color, (screen_width/2, screen_height/2+50))


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

    player_1.restart((player1_start_pos[0], player1_start_pos[1]))
    player_2.restart((player2_start_pos[0], player2_start_pos[1]))

    main()


# PAUSE 
def pauseGame():
    mouseVisible(True)
    window.alpha(screen)
    pause_text.drawText(screen)
    resume_text.drawText(screen)
    quit_text.drawText(screen)


#GAME OVER
def gameOver():
    quit_text = Text("Main menu (Q)", main_font, white_color, (screen_width/2, screen_height/2+90))
    mouseVisible(True)
    window.alpha(screen)
    gameover_text.drawText(screen)
    newgame_text.drawText(screen)
    quit_text.drawText(screen)


def main():
    # MAIN STRUCTURE
    clock = pygame.time.Clock()
    
    power_bar.reset()

    run = True
    itsOver = False
    pause = False
    drunk = False
    ballMove = False
    player1 = False
    player2 = True
    previousXPos = 0
    previousYPos = 0
    time = 0

    while run:
        mousePos = pygame.mouse.get_pos()

        # DRAWS
        window.draw_bg(screen)
        cup_group_1.draw(screen)
        cup_group_2.draw(screen)
        player_group.draw(screen)
        power_bar.drawBar(screen)
        power_text.drawText(screen)
        window.drawHighScore(screen)

        # COLLIDE DETECTION
        if pygame.sprite.spritecollide(player_1, cup_group_2, True):
            print("Hit")
            #current_score += 10

            if len(cup_group_2) == 0:
                itsOver = True
                
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
                    # 'HARD RESET'
                    if event.key == ord('f'):   
                        initGame()
                        
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == ord('a') or event.key == ord('d'):
                        power_bar.x_change = 5   
                    
                    if itsOver:
                        if event.key == pygame.K_RETURN:  
                            initGame()
                        elif event.key == ord('q'):
                            game_menu()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == ord('a') or event.key == ord('d'):
                        power_bar.x_change = 0 
            elif pause:
                if event.type == pygame.KEYDOWN:
                    # Go to main menu
                    if event.key == ord('q'):
                        game_menu()
        
        
        # UPDATES JA MUUTA
        if not pause:
            mouseVisible(False)
            if ballMove:
                speed = power_bar.bar_start_width/4
                time += 0.05

                if player1:
                    if drunk:
                        deviationY = 100 * random.random() * ((-0.71) - 0.71) + 0.71
                        deviationX = 100 * random.random() * ((-0.41) - 0.71) + 0.41
                    else: 
                        deviationX = 0
                        deviationY = 0

                    angle = math.atan2((mousePos[1]+deviationY)-player1_start_pos[1], (mousePos[0]+deviationX)-player1_start_pos[0])
                    

                    if player_1.rect.x > previousXPos:
                        player_1.dx = (speed * math.cos(angle)) + (-9.81* (time)**2)
                        player_1.dy = speed * math.sin(angle)
                        previousXPos = player_1.rect.x
                    else:
                        if not itsOver:
                            pygame.time.wait(1000)
                            player_1.restart((player1_start_pos[0], player1_start_pos[1]))
                            player1 = False
                            player2 = True                           
                            main()

                    player_1.ball_animation()

                if player2:
                    if drunk:
                        deviationY = 100 * random.random() * ((-0.71) - 0.71) + 0.71
                        deviationX = 100 * random.random() * ((-0.41) - 0.71) + 0.41
                    else: 
                        deviationX = 0
                        deviationY = 0

                    angle = math.atan2((mousePos[1]+deviationY)-player2_start_pos[1], (mousePos[0]+deviationX)-player2_start_pos[0])
                    

                    if player_2.rect.x > previousXPos:
                        player_2.dx = (speed * math.cos(angle)) + (-9.81* (time)**2)
                        player_2.dy = speed * math.sin(angle)
                        previousXPos = player_2.rect.x
                    else:
                        if not itsOver:
                            pygame.time.wait(1000)
                            player_2.restart((player2_start_pos[0], player2_start_pos[1]))
                            player1 = True
                            player2 = False
                            main()

                    player_2.ball_animation()
 
            else:
                crosshair_group.draw(screen)
                cup_group_1.update()
                cup_group_2.update()
                crosshair_group.update()
                player_group.update()
                power_bar.barAnimation()

        elif pause:
            pauseGame()

        if itsOver:
            gameOver()

        pygame.display.update()
        clock.tick(FPS)

# MAINMENU        
def game_menu():
    
    while True:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 

            if event.type == pygame.KEYDOWN:
                # ENTER to restart
                if event.key == pygame.K_RETURN:
                    initGame()


        screen.fill(background_color)
        logo_text.drawText(screen)
        newgame_text.drawText(screen)

        pygame.display.update()
        clock.tick(60)   
game_menu()