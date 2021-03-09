import sys
import pygame

class Screen:
    def __init__(self, width, height):
        self.width = width 
        self.height = height
        
        pygame.init()

        self.screen = pygame.display.set_mode(size=(self.width, self.height), flags=0, depth=0, display=0, vsync=0)

        self.background = None

        self.set_background("beerbong_game_bg_color.jpg")

        # ISO PAUSE TEKSTI PUNASELLA
        font = pygame.font.SysFont("", 84)
        self.pause_text = font.render("PAUSE", True, (255, 0, 0))

        # TASOITA TEKSTI KESKELLE
        screen_center = self.screen.get_rect().center
        self.text_pause_rect = self.text_pause.get_rect(center=screen_center)
    
    def draw(self, screen):
        screen.blit(self.bg, [0, 0])

    # getterit screen pituudelle ja korkeudelle
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def draw_bg(self, screen):
         # clear screen to black
        screen.fill( (0,0,0) )
        if self.background:
            screen.blit(self.background, (0,0))

    def set_background(self, img=None):
        if img: 
            self.background = pygame.image.load(img)

    def run(self):

        clock = pygame.time.Clock()

        run = True
        pause = False

        while run:
            # KEY EVENTIT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    # Pause on ESC
                    if event.key == pygame.K_ESCAPE:
                        pause = not pause
                        

            # UPDATES JA MUUTA
            # if not pause:
            #     # change elements position
            #     self.player.update()

            # DRAWS

            self.draw_bg(self.screen)

            if pause:
                # draw pause text
                self.screen.blit(self.text_pause, self.text_pause_rect.topleft)

            pygame.display.update()

            # ruudun päivitys 60 FPS 
            clock.tick(60) 
        
        pygame.quit()

Screen(1280,720).run()