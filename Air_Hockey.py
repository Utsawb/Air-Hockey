from math import copysign
import os
import pygame as pg
import copy

COLOR_PALETTE = {
    "DARK PURPLE" : (36, 16, 35),
    "BLOOD RED" : (107, 5, 4),
    "CHINESE RED" : (163, 50, 11),
    "SMILY GREEN" : (71, 160, 37)
}

WIDTH = 1280
HEIGHT = 720


class Player:
    def __init__(self, pos, vel, acc, r, col, m, pn):
        # [x, y]
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.r = r
        self.col = col
        self.m = m
        self.pn = pn
        if pn == 1:
            self.up = pg.K_w
            self.down = pg.K_s
            self.right = pg.K_d
            self.left = pg.K_a
            self.bounds = [0, WIDTH/2-r]
        elif pn == 2:
            self.up = pg.K_i
            self.down = pg.K_k
            self.right = pg.K_l
            self.left = pg.K_j
            self.bounds = [WIDTH/2+r, WIDTH]

    def update(self, keystate):
        if self.pn == 1:
            self.up = pg.K_w
            self.down = pg.K_s
            self.right = pg.K_d
            self.left = pg.K_a
            self.bounds = [0, WIDTH/2-self.r]
        elif self.pn == 2:
            self.up = pg.K_i
            self.down = pg.K_k
            self.right = pg.K_l
            self.left = pg.K_j
            self.bounds = [WIDTH/2+self.r, WIDTH]


        SCALE_FACTOR = 1
        MAX_VEL = 10

        self.acc[0] = SCALE_FACTOR * (int(keystate[self.right]) - int(keystate[self.left])) 
        self.acc[1] = SCALE_FACTOR * (int(keystate[self.down]) - int(keystate[self.up])) 

        self.vel[0] = copysign(min(abs(self.vel[0] + SCALE_FACTOR * self.acc[0]), MAX_VEL), self.vel[0] + SCALE_FACTOR * self.acc[0])
        self.vel[1] = copysign(min(abs(self.vel[1] + SCALE_FACTOR * self.acc[1]), MAX_VEL), self.vel[1] + SCALE_FACTOR * self.acc[1])

        self.pos[0] = self.pos[0] + SCALE_FACTOR * self.vel[0]
        self.pos[1] = self.pos[1] + SCALE_FACTOR * self.vel[1]

        if self.pos[0] < self.r + self.bounds[0]:
            self.vel[0] *= -1
            self.pos[0] = self.r + self.bounds[0]
        elif self.pos[0] > self.bounds[1]:
            self.vel[0] *= -1
            self.pos[0] = self.bounds[1]
        if self.pos[1] < self.r:
            self.vel[1] *= -1
            self.pos[1] = self.r
        elif self.pos[1] > HEIGHT-self.r:
            self.vel[1] *= -1
            self.pos[1] = HEIGHT-self.r

        self.vel[0] *= 0.95
        self.vel[1] *= 0.95

    def draw(self, surface):
        pg.draw.circle(surface, self.col, self.pos, self.r)

class Ball:
    def __init__(self, pos, vel, acc, r, col, m):
        # [x, y]
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.r = r
        self.col = col
        self.m = m

    def update(self):
        SCALE_FACTOR = 1
        MAX_VEL = 8

        self.vel[0] = copysign(min(abs(self.vel[0] + SCALE_FACTOR * self.acc[0]), MAX_VEL), self.vel[0] + SCALE_FACTOR * self.acc[0])
        self.vel[1] = copysign(min(abs(self.vel[1] + SCALE_FACTOR * self.acc[1]), MAX_VEL), self.vel[1] + SCALE_FACTOR * self.acc[1])

        self.pos[0] = self.pos[0] + SCALE_FACTOR * self.vel[0]
        self.pos[1] = self.pos[1] + SCALE_FACTOR * self.vel[1]

        global score1
        global score2
        if self.pos[0] < self.r:
            self.vel[0] *= -1
            score2 += 1
        if self.pos[0] > WIDTH - self.r:
            self.vel[0] *= -1
            score1 += 1

        if self.pos[1] < self.r or self.pos[1] > HEIGHT-self.r:
            self.vel[1] *= -1

    def draw(self, surface):
        pg.draw.circle(surface, self.col, self.pos, self.r)

def scaler(a, b):
    '''
        Returns a list with items multiplied by scaler, aka scaler multiplication of a matrix

        Parameters:
            a (list): a list of 2 floats
            b (float): a scaler float

        Returns:
            scaler multiplied matrix (list): computed scaler multiplication
    '''
    return [a[0]*b, a[1]*b]
def length_squared(a):
    '''
        Finds the length of a vector squared

        Parameters:
            a (list): a list of 2 floats
        
        Retuns:
            distance squared (float): x^2 + y^2

    '''
    return a[0]**2 + a[1]**2
def check_collision(a: Player, b: Ball):
    '''
        Checks if a ball and player are colided

        Parameter:
            a (Player): the player
            b (Ball): the ball
        
        Returns:
            is_colided (bool): are the collided
    '''
    distance_squared = (b.pos[0] - a.pos[0])**2 + (b.pos[1] - a.pos[1])**2
    return distance_squared < (a.r + b.r)**2
def dot(a, b):
    return sum([a[0]*b[0], a[1]*b[1]])
def sub(a, b):
    return [a[0] - b[0], a[1] - b[1]]
def update_collision(a, b):
    # x = dot(sub(b1.vel, b2.vel), sub(b1.pos, b2,pos))
    # y = lensq(sub(b1.pos, b2.pos))
    # z = sub(b1.pos, b2.pos)
    # b1.vel = sub(b1.vel, scaler(z, 2 * y/x ))
    m = 2 * b.m / (a.m + b.m)
    x = dot(sub(a.vel, b.vel), sub(a.pos, b.pos))
    y = length_squared(sub(a.pos, b.pos))
    z = sub(a.pos, b.pos)
    return sub(a.vel, scaler(z, m * y / x))


# Initialize PyGame PreReqs
pg.init()
pg.display.set_caption("Air Hockey")
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)
surface = pg.Surface((WIDTH, HEIGHT))
FPS = 60
clock = pg.time.Clock()
font = pg.font.Font(None, 48)


# Inittialize game objects
player = Player([WIDTH/4, HEIGHT/2], [0, 0], [0, 0], 25, COLOR_PALETTE["BLOOD RED"], 1, 1)
player2 = Player([WIDTH/4*3, HEIGHT/2], [0, 0], [0, 0], 25, COLOR_PALETTE["BLOOD RED"], 1, 2)
ball = Ball([WIDTH/2, HEIGHT/4], [0, 0], [0, 0], 25, COLOR_PALETTE["SMILY GREEN"], 1)
score1 = 0
score2 = 0
scene = 0

# Game Loop
while True:
    # FPS Lock
    clock.tick(FPS)

    # Game State Grab
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            pg.quit()
            quit()
    keystate = pg.key.get_pressed()

    if scene == 0:
        try: 
            # File IO
            img = pg.image.load("directions.png").convert()
        except:
            os._exit(1)
        screen.blit(img, (0, 0))
        pg.display.flip()

        if keystate[pg.K_RETURN]:
            scene = 1
                
    if scene == 1:
        # Update
        if check_collision(player, ball):
            temp = copy.copy(player)
            player.vel = update_collision(player, ball)
            ball.vel = update_collision(ball, temp)
        if check_collision(player2, ball):
            temp = copy.copy(player2)
            player2.vel = update_collision(player2, ball)
            ball.vel = update_collision(ball, temp)
        player.update(keystate)
        player2.update(keystate)
        ball.update()

        # Draw
        surface.fill(COLOR_PALETTE["DARK PURPLE"])
        pg.draw.line(surface, COLOR_PALETTE["CHINESE RED"], (WIDTH/2+25/2, 0), (WIDTH/2+25/2, HEIGHT), 25)

        text_surface = font.render(str(score1), False, (255, 255, 255))
        text_surface2 = font.render(str(score2), False, (255, 255, 255))

        ball.draw(surface)
        player.draw(surface)
        player2.draw(surface)

        # Push to switch buffer
        screen.blit(surface, (0, 0))
        screen.blit(text_surface, (WIDTH/2-50, HEIGHT/2))
        screen.blit(text_surface2, (WIDTH/2+50, HEIGHT/2))
        pg.display.flip()
