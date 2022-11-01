from math import copysign
import pygame as pg
import copy

COLOR_PALETTE = {
    "DARK PURPLE" : (36, 16, 35),
    "BLOOD RED" : (107, 5, 4),
    "CHINESE RED" : (163, 50, 11),
    "SMILY GREEN" : (71, 160, 37)
}

class Player:
    def __init__(self, pos, vel, acc, r, col, m):
        # [x, y]
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.r = r
        self.col = col
        self.m = m

    def update(self, keystate):
        SCALE_FACTOR = 1
        MAX_VEL = 10

        self.acc[0] = SCALE_FACTOR * (int(keystate[pg.K_d]) - int(keystate[pg.K_a]))
        self.acc[1] = SCALE_FACTOR * (int(keystate[pg.K_s]) - int(keystate[pg.K_w]))

        self.vel[0] = copysign(min(abs(self.vel[0] + SCALE_FACTOR * self.acc[0]), MAX_VEL), self.vel[0] + SCALE_FACTOR * self.acc[0])
        self.vel[1] = copysign(min(abs(self.vel[1] + SCALE_FACTOR * self.acc[1]), MAX_VEL), self.vel[1] + SCALE_FACTOR * self.acc[1])

        self.pos[0] = self.pos[0] + SCALE_FACTOR * self.vel[0]
        self.pos[1] = self.pos[1] + SCALE_FACTOR * self.vel[1]

        if self.pos[0] < self.r or self.pos[0] > 1280-self.r:
            self.vel[0] *= -1
        if self.pos[1] < self.r or self.pos[1] > 720-self.r:
            self.vel[1] *= -1

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
        MAX_VEL = 10

        self.vel[0] = copysign(min(abs(self.vel[0] + SCALE_FACTOR * self.acc[0]), MAX_VEL), self.vel[0] + SCALE_FACTOR * self.acc[0])
        self.vel[1] = copysign(min(abs(self.vel[1] + SCALE_FACTOR * self.acc[1]), MAX_VEL), self.vel[1] + SCALE_FACTOR * self.acc[1])

        self.pos[0] = self.pos[0] + SCALE_FACTOR * self.vel[0]
        self.pos[1] = self.pos[1] + SCALE_FACTOR * self.vel[1]

        if self.pos[0] < self.r or self.pos[0] > 1280-self.r:
            self.vel[0] *= -1
        if self.pos[1] < self.r or self.pos[1] > 720-self.r:
            self.vel[1] *= -1

    def draw(self, surface):
        pg.draw.circle(surface, self.col, self.pos, self.r)

def scaler(a, b):
    return [a[0]*b, a[1]*b]
def length_squared(a):
    return a[0]**2 + a[1]**2
def check_collision(a: Player, b: Ball):
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
screen = pg.display.set_mode((1280, 720), pg.HWSURFACE | pg.DOUBLEBUF)
surface = pg.Surface((1280, 720))
FPS = 60
clock = pg.time.Clock()
player = Player([1280/2, 720/2], [0, 0], [0, 0], 25, COLOR_PALETTE["BLOOD RED"], 1)
ball = Ball([1280/4*3, 720/4], [0, 0], [0, 0], 25, COLOR_PALETTE["SMILY GREEN"], 1)

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
    
    # Update
    if check_collision(player, ball):
        temp = copy.copy(player)
        player.vel = update_collision(player, ball)
        ball.vel = update_collision(ball, temp)
    player.update(keystate)
    ball.update()

    # Draw
    surface.fill(COLOR_PALETTE["DARK PURPLE"])
    ball.draw(surface)
    player.draw(surface)

    # Push to switch buffer
    screen.blit(surface, (0, 0))
    pg.display.flip()