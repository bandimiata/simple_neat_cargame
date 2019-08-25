import pygame
import random
import os
import time
import neat
import visualize
import pickle

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont("Arial", 50)

WIN_WIDTH = 800
WIN_height = 800
VEL = 100
BG_COLOR = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0, 255, 0)
WHITE = (255,255, 255)
GREY = (100, 100, 100)

score = 0
box_counter = 0
gen = 0

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
        self.set_x()
   
    def draw(self, win):
        # pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        win.blit(car_img, (self.x-42, self.y-5))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def right(self):
        self.x += self.vel
        if self.x + self.width> 720:
            self.x = 720 - self.width

    def left(self):
        self.x -= self.vel
        if self.x < 80:
            self.x = 80

    def set_x(self):
        self.x = random.randrange(100, 500)

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
            win.blit(box_exp_img, (self.x-30, self.y-25))

    def move(self):
        self.y += VEL/3
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def draw_window(win, cars, boxes, score, box_counter, gen):
    win.fill(BG_COLOR)
    win.blit(bg, (0, 0))
    for car in cars:
        car.draw(win)
    for box in boxes:
        box.draw(win)

#    for girl in girls:
#        girl.draw(win)

    score_label = myfont.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - 30 - score_label.get_width() - 15, 10))

    gen_num = myfont.render("Generation: " + str(gen),1,(255,255,255))
    win.blit(gen_num, (WIN_WIDTH - 30 - gen_num.get_width() - 15, 110))

    if score < box_counter:
        cter_color = RED
    else:
        cter_color = WHITE

    counter_label = myfont.render("Penalty: " + str(box_counter),1,cter_color)
    win.blit(counter_label, (WIN_WIDTH - 30 - counter_label.get_width() - 15, 60))
    pygame.display.update()

def main(genomes, config):
    
    global gen
    gen += 1

    pygame.time.delay(27)
    
    nets = []
    ge = []
    cars = []

    for _, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(Car(200, 700, RED))
        ge.append(g)

    run = True
    alive = True
    
    # car = Car(200, 700, RED)
    boxes = [Boxes(0, WHITE)]
    # girls = [Girl(0)]
    add_box = False
    # add_girl = False
    score = 0
    box_counter = 0

    while run and len(cars) > 0:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        box_ind = 0
        if len(cars) > 0:
            if len(boxes) > 1 and cars[0].y + cars[0].height > boxes[0].y:
                box_ind = 1

        for z, car in enumerate(cars):
            ge[z].fitness += 0.05

            output = nets[z].activate((car.x, car.x - boxes[box_ind].x, car.y - boxes[box_ind].y - boxes[box_ind].height))
            
            if output[0] > 1:
                car.right()
            if output[1] > 1:
                car.left()

#        keys = pygame.key.get_pressed()
#
#        if keys[pygame.K_LEFT]:
#            car.x -= car.vel
#            if car.x < 80:
#                car.x = 80
#
#        if keys[pygame.K_RIGHT]:
#            car.x += car.vel
#            if car.x + car.width> 720:
#                car.x = 720 - car.width


        # rem_girl = []
        # for girl in girls:
        #     girl.draw(win)
        #     girl.move()
        #     for car in cars:
        #         kari = car.get_rect()
        #         if kari.colliderect(girl.get_rect()):
        #             if not girl.hit:
        #                 score += 5
        #                 girl.hit = True
        #             girl.passed = True

        #         if not girl.passed and girl.y > 500:
        #             add_girl = True
                    
        #         if girl.y > WIN_height:
        #             girl.passed = False
        #             rem_girl.append(girl)
        #             girl.hit = False

        # if add_girl:
        #     girls.append(Girl(0))
        #     add_girl = False
        #     girl.passed = True

        # for r in rem_girl:
        #     girls.remove(r)
        

        rem = []
        for box in boxes:
            box.move()
            for x, car in enumerate(cars):
                
                if car.x < 81 or car.x > 719 - car.width:
                    ge[x].fitness -= 1
                    cars.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                kari = car.get_rect()
                if kari.colliderect(box.get_rect()):
                    
                    
                    ge[x].fitness -= 1
                    cars.pop(x)
                    nets.pop(x)
                    ge.pop(x)

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
            for g in ge:
                g.fitness += 2
            boxes.append(Boxes(0, WHITE))
            add_box = False
            box.passed = True
            
        
        for r in rem:
            boxes.remove(r)
            score += 1
            box_counter += 1

        draw_window(win, cars, boxes, score, box_counter, gen)




def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_simple.txt')
    run(config_path)

