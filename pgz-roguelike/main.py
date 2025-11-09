import math
import random
from pygame import Rect

# Configuração do PgZero
TITLE = "Mini Roguelike"
TILE = 16
GRID_W = 40
GRID_H = 40
# Tamanho do viewport (em tiles) igual à grade para mostrar o mapa inteiro
VIEW_W_TILES = GRID_W
VIEW_H_TILES = GRID_H
WIDTH = VIEW_W_TILES * TILE
HEIGHT = VIEW_H_TILES * TILE
# Estados do jogo
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

# Cores
WHITE = (240, 240, 240)
BLACK = (20, 20, 24)
GRAY = (70, 70, 80)
LIGHT_GRAY = (160, 160, 170)
GREEN = (40, 200, 120)
RED = (220, 80, 80)
YELLOW = (240, 210, 70)
BLUE = (80, 160, 240)

# Nomes das imagens de tiles. 
TILE_FLOOR_NAME = "piso"
TILE_WALL_NAME = "parede"

HERO_PREFIX = "hero"
ENEMY_PREFIX = "enemy"
HERO_IDLE_FRAMES = 1
HERO_MOVE_FRAMES = 1
ENEMY_IDLE_FRAMES = 1
ENEMY_MOVE_FRAMES = 1
SPRITE_FPS_IDLE = 6.0
SPRITE_FPS_MOVE = 10.0
ENEMY2_PREFIX = "enemy_02"

MUSIC_ENABLED = True
SFX_ENABLED = True

# Button UI
class Button:
    def __init__(self, rect: Rect, text: str, bg, fg):
        self.rect = rect
        self.text = text
        self.bg = bg
        self.fg = fg
        self.hover = False

    def draw(self, screen):
        color = self.bg if not self.hover else LIGHT_GRAY
        screen.draw.filled_rect(self.rect, color)
        screen.draw.rect(self.rect, WHITE)
        screen.draw.text(
            self.text,
            center=self.rect.center,
            color=self.fg,
            fontsize=28,
            shadow=(1, 1),
            scolor=BLACK,
        )

    def contains(self, pos):
        return self.rect.collidepoint(pos)

# Tile map generation 
class TileMap:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.walls = set()
        self._use_images = None  
        self._generate_matrix()

    def is_blocked(self, gx, gy):
        return (gx, gy) in self.walls

    def is_occupied(self, gx, gy):
        return (gx, gy) in self.walls

    def random_floor_cell(self):
        while True:
            x = random.randint(1, self.w - 2)
            y = random.randint(1, self.h - 2)
            if not self.is_blocked(x, y):
                return (x, y)

    def draw(self, screen, cam):
        screen.fill(BLACK)
        cam_x, cam_y = cam
        use_images = self._use_images
        x0 = max(0, cam_x // TILE)
        y0 = max(0, cam_y // TILE)
        x1 = min(self.w, (cam_x + WIDTH + TILE - 1) // TILE)
        y1 = min(self.h, (cam_y + HEIGHT + TILE - 1) // TILE)
        for x in range(x0, x1):
            for y in range(y0, y1):
                px, py = x * TILE - cam_x, y * TILE - cam_y
                is_wall = (x, y) in self.walls
                if use_images is None:
                    try:
                        screen.blit(TILE_WALL_NAME if is_wall else TILE_FLOOR_NAME, (px, py))
                        self._use_images = True
                        use_images = True
                    except Exception:
                        self._use_images = False
                        use_images = False
                if use_images:
                    try:
                        screen.blit(TILE_WALL_NAME if is_wall else TILE_FLOOR_NAME, (px, py))
                    except Exception:
                        rect = Rect(px, py, TILE, TILE)
                        screen.draw.filled_rect(rect, GRAY if is_wall else (30, 30, 36))
                else:
                    rect = Rect(px, py, TILE, TILE)
                    screen.draw.filled_rect(rect, GRAY if is_wall else (30, 30, 36))

    def _generate_matrix(self):
        self.walls.clear()
        for x in range(self.w):
            self.walls.add((x, 0))
            self.walls.add((x, self.h - 1))
        for y in range(self.h):
            self.walls.add((0, y))
            self.walls.add((self.w - 1, y))

class SpriteAnimator:
    def __init__(self):
        self.t = 0.0

    def update(self, dt):
        self.t += dt

    def phase(self, speed=10.0):
        return math.sin(self.t * speed)

class Character:
    def __init__(self, tilemap: TileMap, gx: int, gy: int, color_body, color_accent, sprite_name=None):
        self.map = tilemap
        self.gx = gx
        self.gy = gy
        self.x = gx * TILE + TILE // 2
        self.y = gy * TILE + TILE // 2
        self.target_px = (self.x, self.y)
        self.moving = False
        self.move_speed = 6 * TILE  # pixels por segundo
        self.anim = SpriteAnimator()
        self.color_body = color_body
        self.color_accent = color_accent
        self.dir = (0, 1)
        self.alive = True
        self.sprite_name = sprite_name

    def can_step(self, dx, dy):
        nx, ny = self.gx + dx, self.gy + dy
        if self.map.is_occupied(nx, ny):
            return False
        return True

    def try_move(self, dx, dy):
        if self.moving:
            return False
        if self.can_step(dx, dy):
            self.gx += dx
            self.gy += dy
            self.dir = (dx, dy)
            self.target_px = (self.gx * TILE + TILE // 2, self.gy * TILE + TILE // 2)
            self.moving = True
            self._play_step()
            return True
        return False

    def _play_step(self):
        if not SFX_ENABLED:
            return
        try:
            sounds.step.play()
        except Exception:
            pass

    def update(self, dt):
        self.anim.update(dt)
        if self.moving:
            dx = self.target_px[0] - self.x
            dy = self.target_px[1] - self.y
            dist = math.hypot(dx, dy)
            if dist <= 0.1:
                self.x, self.y = self.target_px
                self.moving = False
            else:
                step = self.move_speed * dt
                if step >= dist:
                    self.x, self.y = self.target_px
                    self.moving = False
                else:
                    self.x += dx / dist * step
                    self.y += dy / dist * step

    def draw(self, screen, cam):
        cam_x, cam_y = cam
        cx, cy = int(self.x) - cam_x, int(self.y) - cam_y
        if self.sprite_name:
            try:
                screen.blit(self.sprite_name, (cx - TILE // 2, cy - TILE // 2))
                return
            except Exception:
                pass
        body_r = int(TILE * 0.35)
        swing = 6 if self.moving else 2
        phase = self.anim.phase(12.0)
        leg_offset = int(phase * swing)
        screen.draw.filled_rect(Rect(cx - body_r - 6, cy + body_r - 6, 10, 8), self.color_accent)
        screen.draw.filled_rect(Rect(cx + body_r - 4, cy + body_r - 6, 10, 8), self.color_accent)
        screen.draw.filled_rect(Rect(cx - body_r - 6, cy + body_r - 6 + leg_offset, 10, 6), self.color_accent)
        screen.draw.filled_rect(Rect(cx + body_r - 4, cy + body_r - 6 - leg_offset, 10, 6), self.color_accent)
        body_rect = Rect(cx - body_r, cy - body_r, body_r * 2, body_r * 2)
        screen.draw.filled_rect(body_rect, self.color_body)
        screen.draw.rect(body_rect, WHITE)
        ex = int(self.dir[0] * 6)
        ey = int(self.dir[1] * 4)
        eye = Rect(cx - 4 + ex, cy - 6 + ey, 8, 8)
        screen.draw.filled_rect(eye, WHITE)
        screen.draw.filled_rect(Rect(eye.x + 2, eye.y + 2, 4, 4), BLACK)

class Enemy(Character):
    def __init__(self, tilemap, gx, gy):
        super().__init__(tilemap, gx, gy, RED, YELLOW, ENEMY_PREFIX)
        self.retarget_cooldown = 0.0
        self.move_speed = 3 * TILE

    def _play_step(self):
        return

    def in_territory(self, gx, gy):
        return True

    def random_step_towards(self, tx, ty):
        options = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = self.gx + dx, self.gy + dy
            if self.map.is_occupied(nx, ny):
                continue
            if not self.in_territory(nx, ny):
                continue
            d2 = (tx - nx) * (tx - nx) + (ty - ny) * (ty - ny)
            options.append((d2, dx, dy))
        if options:
            options.sort(key=lambda t: t[0])
            _, dx, dy = options[0]
            self.try_move(dx, dy)

    def update(self, dt):
        super().update(dt)
        self.retarget_cooldown -= dt

class Hero(Character):
    def __init__(self, tilemap, gx, gy):
        super().__init__(tilemap, gx, gy, BLUE, GREEN, HERO_PREFIX)

class Enemy2(Enemy):
    def __init__(self, tilemap, gx, gy):
        super().__init__(tilemap, gx, gy)
        self.color_body = (200, 100, 220)
        self.color_accent = (255, 230, 120)
        self.sprite_name = ENEMY2_PREFIX

class Game:
    def __init__(self):
        self.state = STATE_MENU
        self.map = TileMap(GRID_W, GRID_H)
        self.hero = Hero(self.map, 2, 2)
        self.enemies = []
        self._spawn_enemies()
        self.game_over_msg_time = 0.0
        self._init_menu()
        self._start_music()

    def _random_free_cell(self):
        for _ in range(200):
            x = random.randint(1, GRID_W - 2)
            y = random.randint(1, GRID_H - 2)
            if not self.map.is_occupied(x, y):
                return (x, y)
        return self.map.random_floor_cell()

    def _start_music(self):
        if not MUSIC_ENABLED:
            return
        try:
            music.set_volume(0.6)
            music.play("theme")
        except Exception:
            pass

    def _stop_music(self):
        try:
            music.stop()
        except Exception:
            pass

    def _init_menu(self):
        bw = 280
        bh = 56
        mx = WIDTH // 2 - bw // 2
        my = HEIGHT // 2 - 120
        self.btn_start = Button(Rect(mx, my, bw, bh), "Start Game", LIGHT_GRAY, BLACK)
        self.btn_audio = Button(Rect(mx, my + 80, bw, bh), self._audio_label(), LIGHT_GRAY, BLACK)
        self.btn_exit = Button(Rect(mx, my + 160, bw, bh), "Exit", LIGHT_GRAY, BLACK)

    def _audio_label(self):
        m = "On" if MUSIC_ENABLED else "Off"
        s = "On" if SFX_ENABLED else "Off"
        return f"Music: {m}  Sounds: {s}"

    def _spawn_enemies(self):
        self.enemies = []
        count_each = 21
        for _ in range(count_each):
            gx, gy = self._random_free_cell()
            self.enemies.append(Enemy(self.map, gx, gy))
        for _ in range(count_each):
            gx, gy = self._random_free_cell()
            self.enemies.append(Enemy2(self.map, gx, gy))

    def reset(self):
        self.map = TileMap(GRID_W, GRID_H)
        self.hero = Hero(self.map, 2, 2)
        self._spawn_enemies()
        self.state = STATE_PLAYING
        self.game_over_msg_time = 0.0

    def update(self, dt):
        if self.state == STATE_MENU:
            return
        if self.state == STATE_GAME_OVER:
            self.game_over_msg_time += dt
            return
        # Jogando
        self.hero.update(dt)
        for e in self.enemies:
            e.update(dt)
            # Perseguir o herói: dar um passo em direção ao herói quando não estiver se movendo e o cooldown tiver acabado
            if (not e.moving) and (e.retarget_cooldown <= 0):
                e.random_step_towards(self.hero.gx, self.hero.gy)
                e.retarget_cooldown = random.uniform(0.2, 0.6)
        # Colisão herói-inimigo
        for e in self.enemies:
            if (e.gx == self.hero.gx) and (e.gy == self.hero.gy):
                self.state = STATE_GAME_OVER
                self.game_over_msg_time = 0.0
                self._play_hit()
                break

    def _play_hit(self):
        if not SFX_ENABLED:
            return
        try:
            sounds.hit.play()
        except Exception:
            pass

    def draw(self, screen):
        if self.state == STATE_MENU:
            self._draw_menu(screen)
            return
        cam_x, cam_y = 0, 0
        cam = (0, 0)
        self.map.draw(screen, cam)
        self.hero.draw(screen, cam)
        for e in self.enemies:
            e.draw(screen, cam)
        # HUD
        screen.draw.text(
            "Setas/WASD para mover. ESC: menu",
            topleft=(5, 6),
            color=WHITE,
            fontsize=15,
            shadow=(1, 1),
            scolor=BLACK,
        )
        if self.state == STATE_GAME_OVER:
            screen.draw.text(
                "GAME OVER",
                center=(WIDTH // 2, HEIGHT // 2 - 10),
                color=YELLOW,
                fontsize=18,
                shadow=(1, 1),
                scolor=BLACK,
            )
            screen.draw.text(
                "Click ou Enter: menu",
                center=(WIDTH // 2, HEIGHT // 2 + 20),
                color=WHITE,
                fontsize=12,
                shadow=(1, 1),
                scolor=BLACK,
            )

    def _draw_menu(self, screen):
        screen.fill(BLACK)
        title_rect = Rect(0, 40, WIDTH, 60)
        screen.draw.text(
            "Mini Roguelike",
            center=title_rect.center,
            color=YELLOW,
            fontsize=56,
            shadow=(2, 2),
            scolor=BLACK,
        )

        for b in (self.btn_start, self.btn_audio, self.btn_exit):
            b.draw(screen)
        screen.draw.text(
            "Cley Gabriel",
            center=(WIDTH // 2, HEIGHT - 30),
            color=WHITE,
            fontsize=20,
            shadow=(1, 1),
            scolor=BLACK,
        )

    def on_key_down(self, key):
        if self.state == STATE_MENU:
            if key == keys.RETURN:
                self.reset()
            return
        if key == keys.ESCAPE:
            self.state = STATE_MENU
            return
        if self.state == STATE_GAME_OVER:
            if key == keys.RETURN:
                self.reset()
            return
        # Movimento
        if key in (keys.LEFT, keys.A):
            self.hero.try_move(-1, 0)
        elif key in (keys.RIGHT, keys.D):
            self.hero.try_move(1, 0)
        elif key in (keys.UP, keys.W):
            self.hero.try_move(0, -1)
        elif key in (keys.DOWN, keys.S):
            self.hero.try_move(0, 1)

    def on_mouse_move(self, pos):
        if self.state != STATE_MENU:
            return
        self.btn_start.hover = self.btn_start.contains(pos)
        self.btn_audio.hover = self.btn_audio.contains(pos)
        self.btn_exit.hover = self.btn_exit.contains(pos)

    def on_mouse_down(self, pos, button):
        if self.state == STATE_MENU:
            if self.btn_start.contains(pos):
                self.reset()
                return
            if self.btn_audio.contains(pos):
                self.toggle_audio()
                self.btn_audio.text = self._audio_label()
                return
            if self.btn_exit.contains(pos):
                # Encerrar o loop do jogo parando a música e lançando SystemExit
                self._stop_music()
                raise SystemExit
        elif self.state == STATE_GAME_OVER:
            self.state = STATE_MENU

    def toggle_audio(self):
        global MUSIC_ENABLED, SFX_ENABLED
        # Alternar ambos por simplicidade
        MUSIC_ENABLED = not MUSIC_ENABLED
        SFX_ENABLED = not SFX_ENABLED
        try:
            music.set_volume(0.6 if MUSIC_ENABLED else 0.0)
        except Exception:
            pass

# PgZero hooks
_game = Game()

def update(dt):
    _game.update(dt)

def draw():
    _game.draw(screen)

def on_key_down(key):
    _game.on_key_down(key)

def on_mouse_move(pos):
    _game.on_mouse_move(pos)

def on_mouse_down(pos, button):
    _game.on_mouse_down(pos, button)

def __main__():
    import pgzrun 
    pgzrun.go()

if __name__ == "__main__":
    __main__()