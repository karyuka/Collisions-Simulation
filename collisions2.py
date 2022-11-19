import pygame as pg
import math
import random


WIDTH, HEIGHT = 900, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Collisions Simulation")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (66, 90, 245)
GREEN = (0, 255, 0)
PURPLE = (74, 19, 237)
BLUE2 = (19, 157, 237)
BLUE3 = (20, 75, 224)
COLORS = [BLUE, BLUE3, PURPLE, BLUE2]


dt = 1
V = 2

class Particles:

    particles = []
    
    def __init__(self, x, y, m, r, vx, vy, color, main = False):
        self.x = x
        self.y = y
        self.m = m
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = color
        self.main = main


    def check_collision(particle1, particle2):
            dx = particle2.x - particle1.x
            dy = particle2.y - particle1.y
            r = math.sqrt(dx**2 + dy**2)
            if r <= (particle1.r + particle2.r):
                    vinkel = math.atan2(dy, dx)
                    return vinkel


    def vectorizeVel(particle1, particle2):
        dx_1, dy_1 = particle1.x, particle1.y
        dx_2, dy_2 = particle2.x, particle2.y
        vinkel_1 = math.atan2(dy_1, dx_1)
        vinkel_2 = math.atan2(dy_2, dx_1)
        v01 = particle1.vy / math.sin(vinkel_1)
        v02 = particle2.vy / math.sin(vinkel_2)
        return v01, v02

    def transferEnergy(particle1, particle2, vinkel):
         v0A, v0B = particle1.vectorizeVel(particle2)
         mA, mB = particle1.m, particle2.m
         vB =  1#( - mA * (math.sqrt(4 * mB**2 * v0A**2 + 4 * mB**2 * v0B**2 - 8 * v0A * v0B * mB**2) - 2 * mB * (mA * v0A + mB * v0B))) / (2 * mA * mB + 2 * mB**2)
         vA =  -1#(mA * v0A + mB * v0B - mB * vB) / mAa

         particle1.vx = vA * math.cos(vinkel)
         particle1.vy = vA * math.sin(vinkel)
         particle2.vx = vB * math.cos(vinkel)
         particle2.vy = vB * math.cos(vinkel)
    
    
    def update_pos(particles):
        for particle1 in particles:
            if particle1.x + particle1.r + 2 >= WIDTH: 
                particle1.vx = - particle1.vx #+ 0.3 * particle1.vx
            if particle1.x + particle1.r - 40 <= 0:
                particle1.vx = -particle1.vx  #+ 0.3 * particle1.vx
            if particle1.y + particle1.r + 2 >= HEIGHT: 
                particle1.vy = -particle1.vy #+ 0.3 * particle1.vy
            if particle1.y + particle1.r - 40 <= 0:
                particle1.vy = - particle1.vy #+ 0.3 * particle1.vy
            for particle2 in particles:
                if particle1 == particle2:
                    continue
                vinkel = Particles.check_collision(particle1, particle2)
                if vinkel:
                    Particles.transferEnergy(particle1, particle2, vinkel)

    def draw(self):
        self.x += self.vx * dt
        self.y += self.vy * dt
        pg.draw.circle(WIN, self.color, (self.x, self.y), self.r)

    def create_particels(n):
        for i in range(n):
            m = 4
            r = m + 10
            x = random.randint(0, WIDTH - r)
            y = random.randint(0, HEIGHT - r)
            vy = random.randint(-1, 1)
            vx = random.randint(-1, 1)
            color = random.choice(COLORS)
            new_particle = Particles(x, y, m, r, vx, vy, color)
            Particles.particles.append(new_particle)



def control_movement(player, keys):
    if keys[pg.K_a] and player.x - player.r - 2 >= 0:
        player.x -= V
    if keys[pg.K_d] and player.x + player.r + 2 <= WIDTH:
        player.x += V
    if keys[pg.K_w] and player.y - player.r - 2 >= 0:
        player.y -= V
    if keys[pg.K_s] and player.y + player.r + 2 <= HEIGHT:
        player.y += V

    pg.draw.circle(WIN, player.color, (player.x, player.y), player.r)
            

def main():
    clock = pg.time.Clock()

    player = Particles(WIDTH/2, HEIGHT/2, 4, 10, 0, 0, PURPLE, True)
    Particles.create_particels(50)
    # particle1 = Particles(WIDTH / 2 - 300, HEIGHT / 2, 5, 20, 4, 0)
    # particle2 = Particles(WIDTH / 2 + 300, HEIGHT / 2, 2, 20, -3, 0)
    # Particles.particles.append(particle1)
    # Particles.particles.append(particle2)
    particles = Particles.particles
    particles.append(player)

    run = True
    while run:
        clock.tick(60)


        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
        WIN.fill(BLACK)

        for particle in particles:
            if particle.main == True:
                continue
            Particles.draw(particle)

            
        keys_pressed = pg.key.get_pressed()

        control_movement(player, keys_pressed)
        
        Particles.update_pos(particles)


        pg.display.update()

    pg.quit()



main()