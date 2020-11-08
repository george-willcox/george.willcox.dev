import sys, pygame
from pygame.locals import *
from math import *

pygame.init()

WIDTH  = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
FPS    = pygame.time.Clock()

pygame.display.set_caption('Screen Wrapping')

track = pygame.image.load('Track.png').convert()

def on_track(sprite):
    '''Tests to see if car is on the track.'''
    if sprite.x > 1 and sprite.x < WIDTH - 1 and sprite.y > 1 and sprite.y < HEIGHT - 1:
        if track.get_at((int(sprite.x), int(sprite.y))).r == 163 or track.get_at((int(sprite.x), int(sprite.y))).r == 0 or track.get_at((int(sprite.x), int(sprite.y))).r == 255:
            return True
    return False

class Car(object):
    def __init__(self, start_pos = (73, 370), start_angle = 90, image = 'Car.png'):
        '''Initialises the Car object'''
        self.x     = start_pos[0]
        self.y     = start_pos[1]
        self.angle = start_angle
        self.speed = 0

        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (48, 48))

        self.rotcar   = pygame.transform.rotate(self.image, self.angle)

    def move(self, forward_speed = 1, rearward_speed = 0.2):
        '''Moves the car when the arrow keys are pressed'''
        keys = pygame.key.get_pressed()

        #Move the car depending on which keys have been pressed
        if keys[K_a] or keys[K_LEFT]:
            self.angle += self.speed
        if keys[K_d] or keys[K_RIGHT]:
            self.angle -= self.speed
        if keys[K_w] or keys[K_UP]:
            self.speed += forward_speed
        if keys[K_s] or keys[K_DOWN]:
            self.speed -= rearward_speed

        #Keep the angle between 0 and 359 degrees
        self.angle %= 359

        #Apply friction
        if on_track(self): self.speed *= 0.95
        else: self.speed *= 0.75

        #Change the position of the car
        self.x += self.speed * cos(radians(self.angle))
        self.y -= self.speed * sin(radians(self.angle))

    def wrap(self):
        '''Wrap the car around the edges of the screen'''
        self.wrap_around = False

        if self.x <  0 :
            self.x += WIDTH
            self.wrap_around = True

        if self.x  + self.rotcar.get_width() > WIDTH:
            self.x -= WIDTH
            self.wrap_around = True

        if self.y  < 0:
            self.y += HEIGHT
            self.wrap_around = True

        if self.y + self.rotcar.get_height() > HEIGHT:
            self.y -= HEIGHT
            self.wrap_around = True

        if self.wrap_around:
            SCREEN.blit(self.rotcar, self.rotcar.get_rect(center = (self.x, self.y)))
 
        self.x %= WIDTH
        self.y %= HEIGHT

    def render(self):
        '''Renders the car on the screen'''
        self.rotcar   = pygame.transform.rotate(self.image, self.angle)
        
        SCREEN.blit(self.rotcar, self.rotcar.get_rect(center = (self.x, self.y)))

def main():
    car   = Car()
    
    while True:
        #Blit the track to the background
        SCREEN.blit(track, (0, 0))

        #Test if the game has been quit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        car.move()
        car.wrap()
        car.render()
        
        pygame.display.update()
        FPS.tick(30)
    
if __name__ == '__main__': main()
