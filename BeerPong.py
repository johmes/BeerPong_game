import pygame, sys, random, time, math
from pygame import mixer

screen_width = 1280
screen_height = 720

white_color = (255, 255, 255)
orange_color = (255, 200, 28)
red_color = (255, 0, 0)
green_color = (0, 255, 0)
black_color = (0, 0, 0)


class BallInit():
    def __init__(self):
        self.ball_color = white_color
        self.ball_size = [15, 15]
        self.ball_pos = [100, (screen_height/2 - (self.ball_size[1]/2))]

        self.ball = pygame.Rect(self.ball_pos[0], self.ball_pos[1], self.ball_size[0], self.ball_size[1])

    def drawBall(self, screen):
        pygame.draw.ellipse(screen, self.ball_color, self.ball) 
    
    def getBall(self):
        return self.ball

    
    def setBallPos(self, x, y):
        self.ball_pos = [x, y]



# Inherits Ball class
class Ball(BallInit):
    def __init__(self):
        BallInit.__init__(self)
        self.ball_speed = [0, 0]
    
    def set_ball_speed_x(self, x):
        self.ball_speed[0] = x

    def set_ball_speed_y(self, y):
        self.ball_speed[1] = y

    def ball_animation(self):
        self.ball.x += self.ball_speed[0]
        self.ball.y += self.ball_speed[1]
        
        if self.ball.top <= 0 or self.ball.bottom >= (screen_height - (self.ball_size[1]/2)):
            self.ball_speed[1] *= -1

        if self.ball.left <= 0 + (self.ball_size[1]/2):
            self.ball_speed[0] *= -1

        if self.ball.right >= (screen_width):
            self.ball_speed[0] *= -1


class PowerBar:
    def __init__(self):
        self.decrease_speed = -3
        self.bar_start_width = 0
        self.bar_max_width = 350
        self.bar_pos_x = 20
        self.bar_pos_y = 20
        self.bar_height = 40
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

class Aiming:
    def __init__(self):
        self.ball = Ball()
        self.bar_color = orange_color
        self.startpoint = pygame.math.Vector2(self.ball.ball_pos[0] + (self.ball.ball_size[0]/2), screen_height/2)
        self.endpoint = pygame.math.Vector2(250, 0)
        self.direction_x = 0
        self.direction_y = 0
        self.rot_speed = 0
        self.angle = 0
        self.current_endpoint = pygame.math.Vector2(0, 0)

    def drawAimer(self, screen):
        pygame.draw.line(screen, self.bar_color, self.startpoint, (self.startpoint + self.current_endpoint), 3)
        pygame.draw.line(screen, self.bar_color, self.startpoint, (self.startpoint + self.current_endpoint), 3)
        

    def AimingAnimation(self):
        self.angle = (self.angle + self.rot_speed) % 360
        self.current_endpoint = self.endpoint.rotate(self.angle)
        # if self.angle == 5:
        #     self.angle = 5
        # elif self.angle == 355:
        #     self.angle = 355


class Screen:
    def __init__(self, width, height):
        self.width = width 
        self.height = height
        self.caption = "Asteriski Beer Pong"
        self.background = None
        
        pygame.init()

        # SCREENIN POHJA
        self.screen = pygame.display.set_mode(size=(self.width, self.height), flags=0, depth=0, display=0, vsync=0)
        pygame.display.set_caption(self.caption)
        
        # Jos bg ei näy, poista "BeerPong_game/" edestä
        self.set_background("BeerPong_game/beerbong_game_bg_color.jpg")

        # ISO PAUSE TEKSTI PUNASELLA
        font = pygame.font.SysFont("", 84)
        self.pause_text = font.render("PAUSE", True, red_color)

        # TASOITA TEKSTI KESKELLE
        screen_center = self.screen.get_rect().center
        self.pause_text_rect = self.pause_text.get_rect(center=screen_center, y = 170)
    
    def draw_bg(self, screen):
        # clear screen to black
        screen.fill(black_color)
        if self.background:
            screen.blit(self.background, (0,0))
    
    def set_background(self, img=None):
        if img: 
            self.background = pygame.image.load(img)


def main():
    # MAIN STRUCTURE
    clock = pygame.time.Clock()

    run = True
    pause = False
    ballMove = False

    # Objects
    ball = Ball()
    power_bar = PowerBar()
    window = Screen(screen_width, screen_height)
    aimBar = Aiming()

    while run:
        
        # KEY EVENTIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # Pause on ESC
                if event.key == pygame.K_ESCAPE:
                    pause = not pause
            
            if not pause:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ballMove = True
                    # ENTER to restart
                    if event.key == pygame.K_RETURN:
                        main()
                        #ballMove = False

                    if event.key == pygame.K_DOWN:
                        aimBar.rot_speed = 0.4
                    elif event.key == pygame.K_UP:
                        aimBar.rot_speed = -0.4
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        power_bar.x_change = 5   
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        power_bar.x_change = 0

                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        aimBar.rot_speed = 0

        
        # DRAWS
        window.draw_bg(window.screen)
        ball.drawBall(window.screen)
        power_bar.drawBar(window.screen)
        aimBar.drawAimer(window.screen)
        
                    
        # UPDATES JA MUUTA
        if not pause:
            if ballMove:
                ball.set_ball_speed_x((power_bar.bar_start_width*0.08))
                ball.set_ball_speed_y((aimBar.endpoint.rotate(aimBar.angle)[1]+(ball.ball_size[1]*0.75))*0.08)
                ball.ball_animation()
                
            else:
                power_bar.barAnimation()
                aimBar.AimingAnimation()
        elif pause:
            # draw pause text
            window.screen.blit(window.pause_text, window.pause_text_rect.topleft)

        pygame.display.update()
        clock.tick(60) 
    pygame.quit()
    sys.exit() 
main()