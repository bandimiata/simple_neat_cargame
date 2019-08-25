import pygame
import random


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont("Arial", 50)

WIN_WIDTH = 800
WIN_height = 800
VEL = 15
BG_COLOR = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0, 255, 0)
WHITE = (255,255, 255)
GREY = (100, 100, 100)

score = 0
box_counter = 0

win = pygame.display.set_mode((WIN_WIDTH, WIN_height))
pygame.display.set_caption("Simple 1.0")
car_img = pygame.transform.scale(pygame.image.load('Car.png'),[125, 80])
bg = pygame.transform.scale(pygame.image.load('bg.png').convert_alpha(), (800,800))
box_img = pygame.transform.scale(pygame.image.load('truck.png').convert_alpha(), (250,230))
girl_img = pygame.transform.scale(pygame.image.load('girl.png').convert_alpha(), (100,100))
girl_dead_img = pygame.transform.scale(pygame.image.load('girl_dead.png').convert_alpha(), (100,100))
box_exp_img = pygame.transform.scale(pygame.image.load('exp.png').convert_alpha(), (150,150))

class Car:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vel = VEL/2
        self.height = 60
        self.width = 40

   
    def draw(self, win):
        # pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        win.blit(car_img, (self.x-42, self.y-5))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Girl:
    def __init__(self, y):
        self.y = y
        self.x = 0
        self.vel = VEL
        self.height = 100
        self.width = 70
        
        self.set_x()

        self.passed = False
        self.hit = False

    def set_x(self):
        self.x = random.randrange(50, 650)

    def draw(self, win):
        # pygame.draw.rect(win, WHITE, (self.x, self.y, self.width, self.height))
        if not self.hit:
            win.blit(girl_img, (self.x-20, self.y))
        else:
            win.blit(girl_dead_img, (self.x-20, self.y))


    def move(self):
        self.y += VEL/3

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Boxes:
    def __init__(self, y, color):
        self.y = y
        self.x = 0
        self.vel = VEL
        self.height = 175
        self.width = 80
        self.color = color

        self.set_x()

        self.passed = False
        self.hit = False
        

    def set_x(self):
        self.x = random.randrange(50, 650)

    def draw(self, win):
        # pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        if not self.hit:
            win.blit(box_img, (self.x-92, self.y-25))
        else:
            win.blit(box_exp_img, (self.x-92, self.y-25))

    def move(self):
        self.y += VEL/3
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def draw_window(win, car, boxes, girls, score, box_counter):
    win.fill(BG_COLOR)
    win.blit(bg, (0, 0))
    car.draw(win)
    for box in boxes:
        box.draw(win)

    for girl in girls:
        girl.draw(win)

    score_label = myfont.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - 30 - score_label.get_width() - 15, 10))

    if score < box_counter:
        cter_color = RED
    else:
        cter_color = WHITE

    counter_label = myfont.render("Penalty: " + str(box_counter),1,cter_color)
    win.blit(counter_label, (WIN_WIDTH - 30 - score_label.get_width() - 15, 60))
    pygame.display.update()

def main():
    pygame.time.delay(27)
    
    run = True
    alive = True
    car = Car(200, 700, RED)
    boxes = [Boxes(0, WHITE)]
    girls = [Girl(0)]
    add_box = False
    add_girl = False
    score = 0
    box_counter = 0

    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        draw_window(win,car, boxes, girls, score, box_counter)
    
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            car.x -= car.vel
            if car.x < 80:
                car.x = 80

        if keys[pygame.K_RIGHT]:
            car.x += car.vel
            if car.x + car.width> 720:
                car.x = 720 - car.width        


        rem_girl = []
        for girl in girls:
            girl.draw(win)
            girl.move()

            kari = car.get_rect()
            if kari.colliderect(girl.get_rect()):
                if not girl.hit:
                    score += 5
                    girl.hit = True
                girl.passed = True

            if not girl.passed and girl.y > 500:
                add_girl = True
                
            if girl.y > WIN_height:
                girl.passed = False
                rem_girl.append(girl)
                girl.hit = False

        if add_girl:
            girls.append(Girl(0))
            add_girl = False
            girl.passed = True

        for r in rem_girl:
            girls.remove(r)
        

        rem = []
        for box in boxes:
            box.draw(win)
            box.move()

            kari = car.get_rect()
            if kari.colliderect(box.get_rect()):
                if not box.hit:
                    score -= box_counter
                    box.hit = True
                box.passed = True
                

            if not box.passed and box.y > 500:
                add_box = True
                
            if box.y > WIN_height:
                rem.append(box)
                box.passed = False
                box.hit = False

        
        
        if add_box:
            boxes.append(Boxes(0, WHITE))
            add_box = False
            box.passed = True
            
        
        for r in rem:
            boxes.remove(r)
            score += 1
            box_counter += 1

        if score < 0:
            score = 0
            pygame.time.delay(1000)
            run = False
main()
