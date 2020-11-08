import sys, pygame
from pygame.locals import *
from math import *

pygame.init()

WIDTH  = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
FPS    = pygame.time.Clock()

pygame.display.set_caption('Screen Wrapping')

class Block(object):
    def __init__(self, start_pos = (0, 0), size = (50, 50), colour = (255, 255, 255)):
        '''Initialises the Car object'''
        self.x     = start_pos[0]
        self.y     = start_pos[1]

        self.surface = pygame.Surface(size)
        self.surface.fill(colour)

    def move(self, speed = 5):
        '''Moves the car when the arrow keys are pressed'''
        keys = pygame.key.get_pressed()

        #Move the car depending on which keys have been pressed
        if keys[K_a] or keys[K_LEFT]:  self.x -= speed
        if keys[K_d] or keys[K_RIGHT]: self.x += speed
        if keys[K_w] or keys[K_UP]:    self.y -= speed
        if keys[K_s] or keys[K_DOWN]:  self.y += speed

    def wrap(self):
        '''Wrap the car around the edges of the screen'''
        self.wrap_around = False

        if self.x <  0 :
            self.x += WIDTH
            self.wrap_around = True

        if self.x  + self.surface.get_width() > WIDTH:
            self.x -= WIDTH
            self.wrap_around = True

        if self.y  < 0:
            self.y += HEIGHT
            self.wrap_around = True

        if self.y + self.surface.get_height() > HEIGHT:
            self.y -= HEIGHT
            self.wrap_around = True

        if self.wrap_around:
            SCREEN.blit(self.surface, (self.x, self.y))

        self.x %= WIDTH
        self.y %= HEIGHT

    def render(self):
        '''Renders the car on the screen'''
        
        SCREEN.blit(self.surface, (self.x, self.y))
        
def main():
    block = Block()
    
    while True:
        #Fill in the background black
        SCREEN.fill((0, 0, 0))

        #Test if the game has been quit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        block.move()
        block.wrap()
        block.render()
        
        pygame.display.update()
        FPS.tick(30)
    
if __name__ == '__main__': main()
