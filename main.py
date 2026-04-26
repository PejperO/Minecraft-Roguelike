import pgzrun
import math
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "Minecraft Roguelike"
HUD = 40
CELL = 40
COLS = WIDTH // CELL
ROWS = (HEIGHT - HUD) // CELL
MENU, GAME, DEAD = 0, 1, 2
GRASS, STONE, WATER, TREE = 0, 1, 2, 3
TILE_CLR = {
    GRASS: (106, 127,  51),
    STONE: (128, 128, 128),
    WATER: ( 64, 164, 223),
    TREE:  ( 70,  95,  35),
}
IS_BLOCKED = {GRASS: False, STONE: True, WATER: True, TREE: True}
state = MENU
music_on = True
tiles = []
player = None
enemies = []
score = 0
tick = 0
SKIN = (255, 213, 185);  HAIR = ( 92,  51,  23)
BLUE = ( 73,  99, 168);  NAVY = ( 40,  40, 140);  SHOE = ( 80,  50,  30)
CGRN = (  0, 128,   0);  CDRK = (  0,  70,   0)
ZGRN = (100, 160, 100);  ZDKR = ( 50,  90,  50)

def px(x, y, w, h, clr):
    screen.draw.filled_rect(Rect(x, y, w, h), clr)

def make_world():
    def pick():
        v = random.random()
        if v < 0.07: return WATER
        if v < 0.17: return STONE
        if v < 0.27: return TREE
        return GRASS

    grid = [[pick() for _ in range(COLS)] for _ in range(ROWS)]
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            r, c = 1 + dr, 1 + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                grid[r][c] = GRASS
    return grid

def make_enemies(n):
    out = []
    for i in range(n):
        for _ in range(500):
            c = random.randint(7, COLS - 1)
            r = random.randint(7, ROWS - 1)
            if not IS_BLOCKED.get(tiles[r][c], True):
                out.append(Enemy(c, r, 'creeper'))
                break
    return out

def start_game():
    global tiles, player, enemies, score, tick
    tiles = make_world()
    player = Player(1, 1)
    enemies = make_enemies(6)
    score, tick = 0, 0
    _try_music()

def _try_music():
    try:
        if music_on:
            music.play('background')
        else:
            music.stop()
    except Exception:
        pass

def draw_steve(cx, cy, frame, face, walking):
    if walking:
        leg = int(math.sin(frame * math.pi / 2) * 9)
        bob = 0
        arm = -leg // 2
    else:
        leg, arm = 0, 0
        bob = int(math.sin(frame * math.pi / 2) * 3)

    px(cx - 8, cy + 2 + leg,  7, 11, NAVY)
    px(cx + 1, cy + 2 - leg,  7, 11, NAVY)
    px(cx - 8, cy + 13 + leg, 7,  3, SHOE)
    px(cx + 1, cy + 13 - leg, 7,  3, SHOE)
    px(cx - 9, cy - 10, 18, 14, BLUE)

    la = arm if face == 1 else -arm
    px(cx - 15, cy - 9 + la, 6, 12, SKIN)
    px(cx + 9,  cy - 9 - la, 6, 12, SKIN)

    hy = cy - 24 + bob
    px(cx - 9, hy,     18, 14, SKIN)
    px(cx - 9, hy,     18,  5, HAIR)

    ex = 1 if face == 1 else -7
    px(cx + ex,     hy + 6, 3, 3, (60, 100, 200))
    px(cx + ex + 4, hy + 6, 3, 3, (60, 100, 200))
    px(cx + ex + 1, hy + 10, 4, 2, (180, 100, 80))

def draw_creeper(cx, cy, frame, face, walking):
    if walking:
        leg = int(math.sin(frame * math.pi / 2) * 7)
        sw = 0
    else:
        leg = 0
        sw = int(math.sin(frame * math.pi / 2) * 4)

    for lx, lm in [(-7, leg), (-1, -leg), (1, -leg), (7, leg)]:
        px(cx + lx + sw, cy + 4, 5, 9 + abs(lm) // 3, CDRK)

    px(cx - 8 + sw, cy - 8, 16, 14, CGRN)

    hx = cx - 10 + sw
    hy = cy - 26
    px(hx, hy, 20, 18, CGRN)

    px(hx + 3,  hy + 5,  4, 5, CDRK)
    px(hx + 13, hy + 5,  4, 5, CDRK)
    px(hx + 7,  hy + 11, 6, 3, CDRK)
    px(hx + 5,  hy + 12, 3, 4, CDRK)
    px(hx + 12, hy + 12, 3, 4, CDRK)

class Player:
    def __init__(self, col, row):
        self.col, self.row = col, row
        self.px = float(col * CELL)
        self.py = float(row * CELL)
        self.tx, self.ty = col * CELL, row * CELL

        self.moving = False
        self.face = 1
        self.wf = 0
        self.wt = 0
        self.inf = 0
        self.idt = 0
        self.hp = 3
        self.inv = 0

    def move(self, dc, dr):
        if self.moving:
            return
        nc, nr = self.col + dc, self.row + dr
        if 0 <= nc < COLS and 0 <= nr < ROWS and not IS_BLOCKED.get(tiles[nr][nc], True):
            self.col, self.row = nc, nr
            self.tx, self.ty = nc * CELL, nr * CELL
            self.moving = True
            if dc:
                self.face = dc
            try:
                sounds.step.stop()
                sounds.step.play()
            except Exception:
                pass

    def update(self):
        if self.moving:
            dx, dy = self.tx - self.px, self.ty - self.py
            d = math.hypot(dx, dy)
            spd = 5.0
            if d <= spd:
                self.px, self.py = float(self.tx), float(self.ty)
                self.moving = False
            else:
                self.px += dx / d * spd
                self.py += dy / d * spd
            self.wt += 1
            if self.wt >= 6:
                self.wt = 0
                self.wf = (self.wf + 1) % 4
        else:
            self.idt += 1
            if self.idt >= 20:
                self.idt = 0
                self.inf = (self.inf + 1) % 4
        if self.inv > 0:
            self.inv -= 1

    def draw(self):
        if self.inv > 0 and (self.inv // 4) % 2:
            return
        cx = int(self.px) + CELL // 2
        cy = int(self.py) + HUD + CELL // 2 + 4
        draw_steve(cx, cy, self.wf if self.moving else self.inf, self.face, self.moving)


class Enemy:
    SPEED = 2.0

    def __init__(self, col, row, kind):
        self.col, self.row = col, row
        self.px = float(col * CELL)
        self.py = float(row * CELL)
        self.tx, self.ty = col * CELL, row * CELL
        self.moving = False
        self.face = 1
        self.kind = kind
        self.wf = random.randint(0, 3)
        self.wt = 0
        self.inf = random.randint(0, 3)
        self.idt = 0
        self.at = random.randint(0, 60)
        self.ad = random.randint(45, 90)

    def update(self):
        if self.moving:
            dx, dy = self.tx - self.px, self.ty - self.py
            d = math.hypot(dx, dy)
            if d <= self.SPEED:
                self.px, self.py = float(self.tx), float(self.ty)
                self.moving = False
            else:
                self.px += dx / d * self.SPEED
                self.py += dy / d * self.SPEED
            self.wt += 1
            if self.wt >= 8:
                self.wt = 0
                self.wf = (self.wf + 1) % 4
        else:
            self.idt += 1
            if self.idt >= 15:
                self.idt = 0
                self.inf = (self.inf + 1) % 4
            self.at += 1
            if self.at >= self.ad:
                self.at = 0
                self.ad = random.randint(45, 90)
                self._ai_step()

    def _ai_step(self):
        dc = player.col - self.col
        dr = player.row - self.row
        if dc == 0 and dr == 0:
            return

        sx = (1 if dc > 0 else -1) if dc != 0 else 0
        sy = (1 if dr > 0 else -1) if dr != 0 else 0
        moves = [(sx, 0), (0, sy)] if abs(dc) >= abs(dr) else [(0, sy), (sx, 0)]
        moves += [(0, sy), (sx, 0), (-sx, 0), (0, -sy)]

        for ddx, ddy in moves:
            if ddx == 0 and ddy == 0:
                continue
            nc, nr = self.col + ddx, self.row + ddy
            if 0 <= nc < COLS and 0 <= nr < ROWS and not IS_BLOCKED.get(tiles[nr][nc], True):
                if not any(e.col == nc and e.row == nr for e in enemies if e is not self):
                    self.col, self.row = nc, nr
                    self.tx, self.ty = nc * CELL, nr * CELL
                    self.moving = True
                    if ddx:
                        self.face = ddx
                    break

    def draw(self):
        cx = int(self.px) + CELL // 2
        cy = int(self.py) + HUD + CELL // 2 + 4
        f = self.wf if self.moving else self.inf
        draw_creeper(cx, cy, f, self.face, self.moving)

    def on_player(self):
        return self.col == player.col and self.row == player.row

def _draw_menu():
    screen.fill((20, 40, 100))

    random.seed(1234)
    for _ in range(50):
        sx, sy = random.randint(0, WIDTH), random.randint(0, HEIGHT - 80)
        px(sx, sy, 2, 2, (255, 255, 200))
    random.seed()

    for c in range(COLS):
        px(c * CELL, HEIGHT - CELL, CELL - 1, CELL, TILE_CLR[GRASS])
        px(c * CELL, HEIGHT - CELL - 8, CELL - 1, 8, (130, 90, 50))

    screen.draw.text("MINECRAFT", center=(WIDTH // 2, 100), fontsize=70, color=(255, 210, 0))
    screen.draw.text("ROGUELIKE", center=(WIDTH // 2, 165), fontsize=38, color=(220, 220, 220))

    labels = ["  Start Game", f"  Music: {'ON' if music_on else 'OFF'}", "  Exit"]
    for i, label in enumerate(labels):
        bx, by = WIDTH // 2 - 130, 240 + i * 80
        px(bx, by, 260, 55, (90, 60, 30))
        screen.draw.rect(Rect(bx, by, 260, 55), (210, 175, 80))
        screen.draw.text(label, center=(WIDTH // 2, by + 27), fontsize=26, color=(255, 255, 255))




def _draw_game():
    screen.fill((10, 10, 10))

    for row in range(ROWS):
        for col in range(COLS):
            t = tiles[row][col]
            tx, ty = col * CELL, row * CELL + HUD
            px(tx, ty, CELL - 1, CELL - 1, TILE_CLR[t])
            if t == TREE:
                px(tx + 14, ty + 14, 12, CELL - 14, (102, 81, 51))
                px(tx + 5,  ty + 2,  30, 20,        ( 51, 102,  0))

    for e in enemies:
        e.draw()
    player.draw()
    px(0, 0, WIDTH, HUD, (0, 0, 0))
    screen.draw.text(f"Score: {score}", (10, 10), fontsize=22, color=(255, 220, 0))
    screen.draw.text(f"HP: {player.hp}", (190, 10), fontsize=22, color=(220, 50, 50))


def _draw_dead():
    screen.fill((25, 0, 0))
    screen.draw.text("YOU DIED", center=(WIDTH // 2, 190), fontsize=88, color=(200, 0, 0))
    screen.draw.text(f"Score: {score}", center=(WIDTH // 2, 310), fontsize=42, color=(255, 220, 0))
    screen.draw.text("press ENTER to continue", center=(WIDTH // 2, 400), fontsize=26, color=(190, 190, 190))


def draw():
    if state == MENU:
        _draw_menu()
    elif state == GAME:
        _draw_game()
    elif state == DEAD:
        _draw_dead()


def update():
    global state, score, tick
    if state != GAME:
        return

    player.update()

    tick += 1
    if tick >= 60:
        tick = 0
        score += 1

    for e in enemies:
        e.update()
        if e.on_player() and player.inv == 0:
            player.hp -= 1
            player.inv = 90
            try:
                sounds.hurt.play()
            except Exception:
                pass
            if player.hp <= 0:
                state = DEAD
                try:
                    music.stop()
                except Exception:
                    pass


def on_key_down(key):
    global state
    if state == DEAD:
        if key == keys.RETURN:
            state = MENU
        return
    if state == GAME:
        if key in (keys.W, keys.UP):    player.move(0, -1)
        if key in (keys.S, keys.DOWN):  player.move(0,  1)
        if key in (keys.A, keys.LEFT):  player.move(-1, 0)
        if key in (keys.D, keys.RIGHT): player.move(1,  0)


def on_mouse_down(pos):
    global state, music_on
    if state != MENU:
        return
    for i in range(3):
        bx, by = WIDTH // 2 - 130, 240 + i * 80
        if bx <= pos[0] <= bx + 260 and by <= pos[1] <= by + 55:
            if i == 0:
                start_game()
                state = GAME
            elif i == 1:
                music_on = not music_on
                _try_music()
            elif i == 2:
                quit()

pgzrun.go()
