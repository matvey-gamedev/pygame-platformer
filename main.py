import pygame
import random
import math
import json
import os

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

WIDTH, HEIGHT = 612, 367
GROUND_Y = 250

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game by motya")
icon = pygame.image.load('images/yagami.jpg').convert_alpha()
pygame.display.set_icon(icon)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.on_ground = False
        self.anim_count = 0
        
        self.img = pygame.image.load('images/naMeste.png').convert_alpha()
        self.walk_left = [
            pygame.image.load('images/p_left/idetNaLevo1.png').convert_alpha(),
            pygame.image.load('images/p_left/naMesteLevo1.png').convert_alpha(),
            pygame.image.load('images/p_left/idetNaLevo2.png').convert_alpha(),
            pygame.image.load('images/p_left/naMesteLevo2.png').convert_alpha()
        ]
        self.walk_right = [
            pygame.image.load('images/p_right/idetNaPravo1.png').convert_alpha(),
            pygame.image.load('images/p_right/naMestePravo1.png').convert_alpha(),
            pygame.image.load('images/p_right/idetNaPravo2.png').convert_alpha(),
            pygame.image.load('images/p_right/naMestePravo2.png').convert_alpha()
        ]

#==============================================================================================================================================================================|
#------------------------------------------------------------------------------- ОТДЕЛ ФОНОВ ----------------------------------------------------------------------------------|
#==============================================================================================================================================================================|

bg = pygame.image.load('images/bg.png').convert_alpha()
bg_x = 0

#==============================================================================================================================================================================|
#------------------------------------------------------------------------------- ОТДЕЛ ЗВУКОВ ---------------------------------------------------------------------------------|
#==============================================================================================================================================================================|
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(8)
step_snd = pygame.mixer.Sound("sounds/shagi-po-trave.mp3")  # найди любой короткий шаг
step_snd.set_volume(0.35)
step_channel = pygame.mixer.Channel(1)  # отдельный канал для шагов
step_channel.set_volume(0.35)
#==============================================================================================================================================================================|
#------------------------------------------------- ОТДЕЛ ИГРОКА: 1.Иконка 2.Список (анимка) 3.Координаты + прыжок -------------------------------------------------------------|
#==============================================================================================================================================================================|

player = pygame.image.load('images/naMeste.png').convert_alpha()

walk_left = [
    pygame.image.load('images/p_left/idetNaLevo1.png').convert_alpha(),
    pygame.image.load('images/p_left/naMesteLevo1.png').convert_alpha(),
    pygame.image.load('images/p_left/idetNaLevo2.png').convert_alpha(),
    pygame.image.load('images/p_left/naMesteLevo2.png').convert_alpha()
]

walk_right = [
    pygame.image.load('images/p_right/idetNaPravo1.png').convert_alpha(),
    pygame.image.load('images/p_right/naMestePravo1.png').convert_alpha(),
    pygame.image.load('images/p_right/idetNaPravo2.png').convert_alpha(),
    pygame.image.load('images/p_right/naMestePravo2.png').convert_alpha()
]

player_anim_count = 0

player_speed = 5
player_x = 275
player_y = 250

is_jump = False
jump_count = 8

#==============================================================================================================================================================================|
#------------------------------------------------ ОТДЕЛ ВРАГОВ: 1.Иконки + их корды 2.Список 3.Создавание ---------------------------------------------------------------------|
#==============================================================================================================================================================================|
# 1.
ghost = pygame.image.load('images/enemies/ghost.png').convert_alpha()
ghost_x = 620 

bird_left = pygame.image.load('images/enemies/bird_left.png').convert_alpha()
bird_right = pygame.image.load('images/enemies/bird_right.png').convert_alpha()
bird_left_x = 630
bird_right_x = -645
bird_left_y = 100
bird_right_y = 100

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

right_bird_timer = pygame.USEREVENT + 2
pygame.time.set_timer(right_bird_timer, 6000)

left_bird_timer = pygame.USEREVENT + 3
pygame.time.set_timer(left_bird_timer, 4500)

#==============================================================================================================================================================================|
#----------------------------------------------------------- ОТДЕЛ ПУЛЬ: 1.Иконки 2.Список 3.Перезарядка ----------------------------------------------------------------------|
#==============================================================================================================================================================================|

bullet_right = pygame.image.load('images/bullets/right_bullet.png').convert_alpha()
bullet_left = pygame.image.load('images/bullets/left_bullet.png').convert_alpha()
bullet_up = pygame.image.load('images/bullets/up_bullet.png').convert_alpha()
bullet_up_right = pygame.image.load('images/bullets/up_right.png').convert_alpha()
bullet_up_left = pygame.image.load('images/bullets/up_left.png').convert_alpha()

bullets = []

max_ammo = 5
ammo = 5

shoot_cd = 250
last_shot_time = 0

is_reloading = False
reload_time = 2000  
reload_start_time = 0

bullet_reload_delay = 350   
last_reload_step = 0

shake_start_time = 0
is_shaking = False

#==============================================================================================================================================================================|
#-------------------------------------------------------------------- Счет с экраном проигрыша --------------------------------------------------------------------------------|
#==============================================================================================================================================================================|

score_bird_kills = 0
score_ghost_kills = 0
score_kills = 0

label = pygame.font.Font(None , 40)
score_label = pygame.font.Font(None, 20)
lose_label = label.render('Вы проиграли!', False, (193, 196, 199))
restart_label = label.render('Играть заново', False, (115, 132, 148))
score_bird = score_label.render(f'Птиц подбито: {score_bird_kills}', False, (175, 238, 238))
score_ghost = score_label.render(f'Призраков убито: {score_ghost_kills}', False, (128, 128, 128))
score_all = score_label.render(f'Всего убито/подбито: {score_kills}', False, (128, 0, 0))
restart_label_rect = restart_label.get_rect(topleft=(200, 200))

#==============================================================================================================================================================================|
#-------------------------------------------------------------- ФУНКЦИИ + СТЕЙТ(СЛОВАРЬ) --------------------------------------------------------------------------------------|
#==============================================================================================================================================================================|
panel_w, panel_h = 460, 360

btn_start_rect = pygame.Rect(0, 0, 260, 52)
btn_best_rect  = pygame.Rect(0, 0, 260, 52)
btn_quit_rect  = pygame.Rect(0, 0, 260, 52)

btn_back_rect  = pygame.Rect(0, 0, 220, 48)  # для сцены "best"

btn_restart_rect = pygame.Rect(0, 0, 220, 48)
btn_menu_rect = pygame.Rect(0, 0, 220, 48)

state = {
    "spawners": [],
    # физика игрока
    "player_vx": 0,
    "player_vy": 0,
    "on_ground": True,

    # камера (скролл уровня)
    "camera_x": 0,

    # звук шагов
    "step_sound_playing": False,

    # уровень
    "level_w": 3000,   # ширина уровня в пикселях (пример)
    "platforms": [],   # список pygame.Rect в координатах мира

    "run_start_time": pygame.time.get_ticks(),
    "run_time_ms": 0,

    "running": True,
    "gameplay": False,
    # фон
    "bg_x": bg_x,
    # игрок
    "player_x": player_x,
    "player_y": player_y,
    "player_speed": player_speed,
    "player_anim_count": player_anim_count,
    "is_jump": is_jump,
    "jump_count": jump_count,

    "enemies": [],

    "bullets": bullets,

    # патроны / перезарядка
    "max_ammo": max_ammo,
    "ammo": ammo,
    "shoot_cd": shoot_cd,
    "last_shot_time": last_shot_time,

    "is_reloading": is_reloading,
    "reload_time": reload_time,
    "reload_start_time": reload_start_time,
    "bullet_reload_delay": bullet_reload_delay,
    "last_reload_step": last_reload_step,

    "shake_start_time": shake_start_time,
    "is_shaking": is_shaking,

    # счет
    "score_bird_kills": score_bird_kills,
    "score_ghost_kills": score_ghost_kills,
    "score_kills": score_kills,

    "scene": "menu",  # "menu" | "game" | "game_over"
    "game_over_start_time": 0,
    "walk_off_frames": 0,
}

state["platforms"] = [
    pygame.Rect(0, GROUND_Y + 40, 3000, 200),     # “земля” (широкая)
    pygame.Rect(450, 240, 120, 20),
    pygame.Rect(750, 210, 140, 20),
    pygame.Rect(1050, 260, 160, 20),
]

state["spawners"] = [
    {"x": 600, "done": False, "kind": "ghost", "pos": (800, GROUND_Y), "speed": 4},
    {"x": 900, "done": False, "kind": "ghost", "pos": (1200, GROUND_Y), "speed": 6},

    {"x": 700, "done": False, "kind": "bird_left", "pos": (1100, 120), "speed": 5},
    {"x": 1300, "done": False, "kind": "bird_right", "pos": (1400, 90), "speed": 5},

    {"x": 900, "done": False, "kind": "walker", "pos": (1050, 220), "speed": 2, "range": (1000, 1200)},
]


SAVE_FILE = "save.json"

def load_save():
    default = {
        "best_kills": 0,
        "best_time_ms": 0,

        "games_played": 0,
        "deaths": 0,

        "total_kills": 0,
        "total_bird_kills": 0,
        "total_ghost_kills": 0,

        "total_time_ms": 0,
    }

    if not os.path.exists(SAVE_FILE):
        return default

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return default

    # backward-compatible: если каких-то ключей нет — подставим дефолт
    for k, v in default.items():
        if k not in data:
            data[k] = v
    return data

def save_save(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

save_data = load_save()

state["best_kills"] = save_data["best_kills"]
state["best_time_ms"] = save_data["best_time_ms"]

state["games_played"] = save_data["games_played"]
state["deaths"] = save_data["deaths"]
state["total_kills"] = save_data["total_kills"]
state["total_bird_kills"] = save_data["total_bird_kills"]
state["total_ghost_kills"] = save_data["total_ghost_kills"]
state["total_time_ms"] = save_data["total_time_ms"]

def hit_enemy_by_bullet(enemies, bullet_rect): 
    for e in enemies:
        if bullet_rect.colliderect(e["rect"]):
            kind = e["kind"]
            enemies.remove(e)
            return kind
    return None

def update_spawners(state, ghost_img):
    px = state["player_x"]  # игрок в мировых координатах

    for s in state["spawners"]:
        if (not s["done"]) and px >= s["x"]:
            s["done"] = True

            if s["kind"] == "ghost":
                r = ghost_img.get_rect(topleft=s["pos"])
                state["enemies"].append({"kind": "ghost", "rect": r, "speed": s["speed"]})

            elif s["kind"] == "walker":
                r = pygame.Rect(s["pos"][0], s["pos"][1], 40, 40)  # размер подгони под спрайт
                state["enemies"].append({
                    "kind": "walker",
                    "rect": r,
                    "vx": s["speed"],
                    "range": s["range"],  # (min_x, max_x)
                })
            elif s["kind"] == "bird_left":
                r = bird_left.get_rect(topleft=s["pos"])
                state["enemies"].append({"kind": "bird_left", "rect": r, "speed": s["speed"]})

            elif s["kind"] == "bird_right":
                r = bird_right.get_rect(topleft=s["pos"])
                state["enemies"].append({"kind": "bird_right", "rect": r, "speed": s["speed"]})

def clamp(v, a, b):
    return max(a, min(b, v))

def update_camera_center_smooth(state):
    # куда камера "хочет" прийти (центр на игроке)
    target = state["player_x"] - WIDTH // 2

    # границы камеры
    max_cam = state["level_w"] - WIDTH
    target = clamp(target, 0, max_cam)

    # плавность (0.08..0.2). Меньше = плавнее, но "ленивее"
    smooth = 0.12

    # lerp
    state["camera_x"] += (target - state["camera_x"]) * smooth

    # чтобы не было дробей в blit (иногда мерцает)
    state["camera_x"] = int(state["camera_x"])


def update_bullets(bullets, enemies, score, camera_x):
    for b in bullets[:]:
        rect = b["rect"]
        rect.x += b["vx"]
        rect.y += b["vy"]

        # границы относительно камеры
        left = camera_x - 80
        right = camera_x + WIDTH + 80
        top = -80
        bottom = HEIGHT + 80

        if rect.x < left or rect.x > right or rect.y < top or rect.y > bottom:
            bullets.remove(b)
            continue

        hit_kind = hit_enemy_by_bullet(enemies, rect)
        if hit_kind is not None:
            bullets.remove(b)
            if hit_kind == "ghost":
                score["ghost"] += 1
            else:
                score["bird"] += 1
            score["all"] += 1

def reset_run(state):
    state["gameplay"] = True
    state["scene"] = "game"  # если scene у тебя есть, иначе строку можно убрать
    state["bg_x"] = 0
    # позиция игрока
    state["player_x"] = 150
    state["player_y"] = GROUND_Y
    # сброс прыжка/анимации (это фикс "падает после рестарта")
    state["is_jump"] = False
    state["jump_count"] = 8
    state["player_anim_count"] = 0
    # очистка мира
    state["enemies"].clear()
    state["bullets"].clear()
    # счет
    state["score_bird_kills"] = 0
    state["score_ghost_kills"] = 0
    state["score_kills"] = 0
    # патроны/перезарядка
    state["ammo"] = state["max_ammo"]
    state["is_reloading"] = False
    state["last_shot_time"] = 0
    state["is_shaking"] = False
    state["shake_start_time"] = 0
    state["reload_start_time"] = 0
    state["last_reload_step"] = 0
    state["run_start_time"] = pygame.time.get_ticks()
    state["run_time_ms"] = 0  
    step_channel.stop()
    state["step_sound_playing"] = False
    state["walk_off_frames"] = 0
    for s in state["spawners"]:
        s["done"] = False

def handle_events(state, now, ghost, bird_left, bird_right,
                  ghost_timer, left_bird_timer, right_bird_timer):
    """
    Обрабатывает события pygame:
    - выход
    - спавн врагов по таймерам
    - старт перезарядки по R
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state["running"] = False
            return

        # спавн врагов

        # перезарядка
        if state["scene"] == "game" and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if state["ammo"] < state["max_ammo"] and not state["is_reloading"]:
                state["is_reloading"] = True
                state["reload_start_time"] = now
                state["last_reload_step"] = now

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = event.pos

            if state["scene"] == "game_over":
                if btn_restart_rect.collidepoint(mouse):
                    reset_run(state)
                elif btn_menu_rect.collidepoint(mouse):
                    state["scene"] = "menu"
                    state["gameplay"] = False

            elif state["scene"] == "menu":
                if btn_start_rect.collidepoint(mouse):
                    reset_run(state)  # стартуем новый забег
                elif btn_best_rect.collidepoint(mouse):
                    state["scene"] = "best"
                    state["gameplay"] = False
                elif btn_quit_rect.collidepoint(mouse):
                    state["running"] = False

            elif state["scene"] == "best":
                if btn_back_rect.collidepoint(mouse):
                    state["scene"] = "menu"
                    state["gameplay"] = False

        if state["scene"] == "menu" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            reset_run(state)

def update_player(state, keys):
    state["player_x"] = int(state["player_x"])
    state["player_y"] = int(state["player_y"])
    SPEED = 5
    GRAVITY = 0.7
    JUMP_V = -12

    # 1) горизонтальная скорость
    vx = 0
    if keys[pygame.K_a]:
        vx = -SPEED
    elif keys[pygame.K_d]:
        vx = SPEED

    state["player_vx"] = vx

    # 2) прыжок (только если стоим на земле)
    if keys[pygame.K_SPACE] and state["on_ground"]:
        state["player_vy"] = JUMP_V
        state["on_ground"] = False
        # TODO: jump sound

    # 3) гравитация
    state["player_vy"] += GRAVITY
    if state["player_vy"] > 16:
        state["player_vy"] = 16

    # 4) движение по X + коллизии по X
    state["player_x"] += state["player_vx"]
    player_rect = player.get_rect(topleft=(state["player_x"], state["player_y"]))

    for p in state["platforms"]:
        if player_rect.colliderect(p):
            if state["player_vx"] > 0:  # вправо
                player_rect.right = p.left
            elif state["player_vx"] < 0:  # влево
                player_rect.left = p.right
            state["player_x"] = player_rect.x

    # 5) движение по Y + коллизии по Y
    state["player_y"] += state["player_vy"]
    player_rect = player.get_rect(topleft=(state["player_x"], state["player_y"]))

    state["on_ground"] = False
    for p in state["platforms"]:
        if player_rect.colliderect(p):
            if state["player_vy"] > 0:  # падаем вниз
                player_rect.bottom = p.top
                state["player_vy"] = 0
                state["on_ground"] = True
            elif state["player_vy"] < 0:  # летим вверх (удар головой)
                player_rect.top = p.bottom
                state["player_vy"] = 0
            state["player_y"] = player_rect.y

    # 6) анимация шага: только когда идем и на земле
    if state["on_ground"] and state["player_vx"] != 0:
        state["player_anim_count"] = (state["player_anim_count"] + 1) % 4
    else:
        state["player_anim_count"] = 0

    if state["player_x"] < 0:
        state["player_x"] = 0

def update_enemies(state, player_rect):
    for e in state["enemies"][:]:
        kind = e["kind"]
        rect = e["rect"]

        if kind == "ghost":
            rect.x -= e["speed"]
            if rect.x < -50:
                state["enemies"].remove(e)
                continue

        elif kind == "bird_left":
            rect.x -= e["speed"]
            if rect.x < -50:
                state["enemies"].remove(e)
                continue

        elif kind == "bird_right":
            rect.x += e["speed"]
            if rect.x > state["level_w"] + 50:
                state["enemies"].remove(e)
                continue

        elif kind == "walker":
            rect.x += e["vx"]
            left_x, right_x = e["range"]
            if rect.x <= left_x or rect.x >= right_x:
                e["vx"] *= -1

        if player_rect.colliderect(rect):
            # чтобы сработало 1 раз
            if state["scene"] == "game":
                now = pygame.time.get_ticks()
                state["game_over_start_time"] = now
                state["scene"] = "game_over"

                # финальное время забега
                state["run_time_ms"] = now - state["run_start_time"]

                # totals
                state["games_played"] += 1
                state["deaths"] += 1
                state["total_time_ms"] += state["run_time_ms"]
                state["total_kills"] += state["score_kills"]
                state["total_bird_kills"] += state["score_bird_kills"]
                state["total_ghost_kills"] += state["score_ghost_kills"]

                # bests
                if state["score_kills"] > state["best_kills"]:
                    state["best_kills"] = state["score_kills"]
                if state["run_time_ms"] > state["best_time_ms"]:
                    state["best_time_ms"] = state["run_time_ms"]

                save_save({
                    "best_kills": state["best_kills"],
                    "best_time_ms": state["best_time_ms"],
                    "games_played": state["games_played"],
                    "deaths": state["deaths"],
                    "total_kills": state["total_kills"],
                    "total_bird_kills": state["total_bird_kills"],
                    "total_ghost_kills": state["total_ghost_kills"],
                    "total_time_ms": state["total_time_ms"],
                })

            return

def draw(screen, bg, score_label, state,
         player, walk_left, walk_right, keys,
         ghost, bird_left, bird_right):
    now = pygame.time.get_ticks()
    px = state["player_x"] - state["camera_x"]
    py = state["player_y"]
    # фон
    screen.blit(bg, (state["bg_x"], 0))
    screen.blit(bg, (state["bg_x"] + WIDTH, 0))

    # счет
    s1 = score_label.render(f'Птиц подбито: {state["score_bird_kills"]}', False, (175, 238, 238))
    s2 = score_label.render(f'Призраков убито: {state["score_ghost_kills"]}', False, (128, 128, 128))
    s3 = score_label.render(f'Всего убито/подбито: {state["score_kills"]}', False, (128, 0, 0))
    screen.blit(s1, (2, 2))
    screen.blit(s2, (2, 27))
    screen.blit(s3, (2, 50))

    if state["scene"] == "game":
        time_s = state["run_time_ms"] // 1000
        t = score_label.render(f'Время: {time_s}', True, (220, 220, 220))
        screen.blit(t, (WIDTH - 110, 2))

        for p in state["platforms"]:
            r = pygame.Rect(p.x - state["camera_x"], p.y, p.w, p.h)
            pygame.draw.rect(screen, (60, 200, 60), r)
        # ---------- HUD: патроны + тряска ----------
        now = pygame.time.get_ticks()

        # тряска когда 0 патронов (у тебя состояние уже есть)
        shake_offset = 0
        if state["ammo"] == 0:
            if not state["is_shaking"]:
                state["is_shaking"] = True
                state["shake_start_time"] = now

        if state["is_shaking"]:
            if now - state["shake_start_time"] < 3000:
                shake_offset = random.randint(-3, 3)
            else:
                state["is_shaking"] = False

        # рисуем индикатор патронов около игрока
        for i in range(state["max_ammo"]):
            rect_x = px - 28 + i * 20 + shake_offset
            rect_y = py - 20
            w, h = 18.5, 14
            base_color = (255, 140, 0) if i < state["ammo"] else (80, 80, 80)
            pygame.draw.ellipse(screen, base_color, (rect_x, rect_y, w, h))

            highlight = (
                min(base_color[0] + 60, 255),
                min(base_color[1] + 60, 255),
                min(base_color[2] + 60, 255)
            )
            highlight_surface = pygame.Surface((w, h // 2), pygame.SRCALPHA)
            pygame.draw.ellipse(highlight_surface, (*highlight, 120), (0, 0, w, h // 2))
            screen.blit(highlight_surface, (rect_x, rect_y))

        # ---------- HUD: дуга перезарядки ----------
        if state["is_reloading"]:
            progress = (now - state["reload_start_time"]) / state["reload_time"]
            if progress > 1:
                progress = 1
            angle = progress * 360
            pygame.draw.arc(screen, (255,165,0), (px - 10, py - 50, 60, 60), 0, 
            math.radians(angle), 3)
        # игрок
        x = state["player_x"] - state["camera_x"]
        y = state["player_y"]

        if keys[pygame.K_a]:
            screen.blit(walk_left[state["player_anim_count"]], (x, y))
        elif keys[pygame.K_d]:
            screen.blit(walk_right[state["player_anim_count"]], (x, y))
        else:
            screen.blit(player, (x, y))

        # враги (рисуем теми же rect, которые обновляются в update_enemies)
        for e in state["enemies"]:
            if e["kind"] == "ghost":
                screen.blit(ghost, (e["rect"].x - state["camera_x"], e["rect"].y))
            elif e["kind"] == "bird_left":
                screen.blit(bird_left, (e["rect"].x - state["camera_x"], e["rect"].y))
            elif e["kind"] == "bird_right":
                screen.blit(bird_right, (e["rect"].x - state["camera_x"], e["rect"].y))

        for b in state["bullets"]:
            rect = b["rect"]
            screen.blit(b["img"], (rect.x - state["camera_x"], rect.y))

    elif state["scene"] == "game_over":
        # --- overlay (сначала затемнение) ---
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        # --- animation (потом считаем t, размеры панели) ---
        t = (now - state["game_over_start_time"]) / 800
        if t < 0: t = 0
        if t > 1: t = 1
        t = 1 - (1 - t) * (1 - t)  # easeOutQuad

        scale = 0.85 + 0.15 * t
        w = int(panel_w * scale)
        h = int(panel_h * scale)

        panel_rect = pygame.Rect(0, 0, w, h)
        panel_rect.center = (WIDTH // 2, HEIGHT // 2)

        # --- panel (рисуем панель) ---
        pygame.draw.rect(screen, (25, 25, 32), panel_rect, border_radius=18)
        pygame.draw.rect(screen, (130, 130, 160), panel_rect, width=2, border_radius=18)

        # --- title ---
        title = label.render("Вы проиграли", True, (240, 240, 245))
        screen.blit(title, title.get_rect(center=(panel_rect.centerx, panel_rect.y + 45)))

        # --- текущая статистика (этой игры) ---
        stat = score_label.render(f'Всего убийств: {state["score_kills"]}', True, (200, 200, 210))
        stat_bird = score_label.render(f'Подбито птиц: {state["score_bird_kills"]}', True, (200, 200, 210))
        stat_ghost = score_label.render(f'Призраков убито: {state["score_ghost_kills"]}', True, (200, 200, 210))

        screen.blit(stat, stat.get_rect(center=(panel_rect.centerx, panel_rect.y + 85)))
        screen.blit(stat_bird, stat_bird.get_rect(center=(panel_rect.centerx, panel_rect.y + 105)))
        screen.blit(stat_ghost, stat_ghost.get_rect(center=(panel_rect.centerx, panel_rect.y + 125)))

        # --- лучшие результаты (под текущими убийствами) ---
        best_time_s = state["best_time_ms"] // 1000
        best_k = score_label.render(f'Лучший счёт: {state["best_kills"]}', True, (200, 200, 210))
        best_t = score_label.render(f'Лучшее время: {best_time_s} сек', True, (200, 200, 210))

        screen.blit(best_k, best_k.get_rect(center=(panel_rect.centerx, panel_rect.y + 155)))
        screen.blit(best_t, best_t.get_rect(center=(panel_rect.centerx, panel_rect.y + 175)))

        # (необязательно) время этой попытки тоже можно показать:
        time_s = state["run_time_ms"] // 1000
        cur_time = score_label.render(f'Время этой игры: {time_s} сек', True, (200, 200, 210))
        screen.blit(cur_time, cur_time.get_rect(center=(panel_rect.centerx, panel_rect.y + 195)))

        # --- кнопки ---
        btn_restart_rect.center = (panel_rect.centerx, panel_rect.centery + 55)
        btn_menu_rect.center = (panel_rect.centerx, panel_rect.centery + 110)

        mouse = pygame.mouse.get_pos()
        hover_restart = btn_restart_rect.collidepoint(mouse)
        hover_menu = btn_menu_rect.collidepoint(mouse)

        pygame.draw.rect(screen, (70, 160, 255) if hover_restart else (60, 140, 255),
                        btn_restart_rect, border_radius=14)
        pygame.draw.rect(screen, (255, 255, 255), btn_restart_rect, width=2, border_radius=14)

        pygame.draw.rect(screen, (100, 100, 110) if hover_menu else (80, 80, 90),
                        btn_menu_rect, border_radius=14)
        pygame.draw.rect(screen, (255, 255, 255), btn_menu_rect, width=2, border_radius=14)

        t1 = score_label.render("Играть заново", True, (255, 255, 255))
        screen.blit(t1, t1.get_rect(center=btn_restart_rect.center))

        t2 = score_label.render("Меню", True, (255, 255, 255))
        screen.blit(t2, t2.get_rect(center=btn_menu_rect.center))
       
    elif state["scene"] == "menu":
        screen.fill((15, 15, 20))

        title = label.render("МЕНЮ", True, (240, 240, 245))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 70)))

        # позиции кнопок
        btn_start_rect.center = (WIDTH // 2, 150)
        btn_best_rect.center  = (WIDTH // 2, 215)
        btn_quit_rect.center  = (WIDTH // 2, 280)

        mouse = pygame.mouse.get_pos()
        hs = btn_start_rect.collidepoint(mouse)
        hb = btn_best_rect.collidepoint(mouse)
        hq = btn_quit_rect.collidepoint(mouse)

        def draw_btn(rect, text, hover):
            pygame.draw.rect(screen, (70,160,255) if hover else (60,140,255), rect, border_radius=14)
            pygame.draw.rect(screen, (255,255,255), rect, width=2, border_radius=14)
            t = score_label.render(text, True, (255,255,255))
            screen.blit(t, t.get_rect(center=rect.center))

        draw_btn(btn_start_rect, "Начать игру", hs)
        draw_btn(btn_best_rect, "Мои лучшие результаты", hb)
        draw_btn(btn_quit_rect, "Выйти из игры", hq)

        hint = score_label.render("Enter — начать", True, (200, 200, 210))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 330)))

    elif state["scene"] == "best":
        screen.fill((15, 15, 20))

        title = label.render("ЛУЧШИЕ РЕЗУЛЬТАТЫ", True, (240, 240, 245))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        best_time_s = state["best_time_ms"] // 1000
        total_time_s = state["total_time_ms"] // 1000

        lines = [
            f'Лучший счёт: {state["best_kills"]}',
            f'Лучшее время: {best_time_s} сек',
            f'Сыграно игр: {state["games_played"]}',
            f'Смертей: {state["deaths"]}',
            f'Всего убийств: {state["total_kills"]}',
            f'Птиц всего: {state["total_bird_kills"]}',
            f'Призраков всего: {state["total_ghost_kills"]}',
            f'Общее время: {total_time_s} сек',
        ]

        y = 110
        for s in lines:
            t = score_label.render(s, True, (210, 210, 220))
            screen.blit(t, (70, y))
            y += 24

        btn_back_rect.center = (WIDTH // 2, 320)
        mouse = pygame.mouse.get_pos()
        hover_back = btn_back_rect.collidepoint(mouse)

        pygame.draw.rect(screen, (100,100,110) if hover_back else (80,80,90), btn_back_rect, border_radius=14)
        pygame.draw.rect(screen, (255,255,255), btn_back_rect, width=2, border_radius=14)
        t = score_label.render("Назад", True, (255,255,255))
        screen.blit(t, t.get_rect(center=btn_back_rect.center))

#                                       ЦИКЛ WHILE (игра)
while state["running"]:
    now = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    handle_events(state, now, ghost, bird_left, bird_right,
              ghost_timer, left_bird_timer, right_bird_timer)
    if state["scene"] == "game":
        state["run_time_ms"] = now - state["run_start_time"] 
                                                # ЗАПОЛНЕНИЕ ЭКРАНА ФОНОМ И СЧЕТОМ

    #==============================================================================================================================================================================|
    #------------------------------------------------- Хитбоксы + задавания списков врагов и их передвижения ----------------------------------------------------------------------|
    #==============================================================================================================================================================================|
    if state["scene"] == "game":
    # 1) физика игрока
        update_player(state, keys)
        walking_now = state["on_ground"] and state["player_vx"] != 0

        if walking_now:
            state["walk_off_frames"] = 0
            if not state["step_sound_playing"]:
                step_channel.play(step_snd, loops=-1)
                state["step_sound_playing"] = True
        else:
            state["walk_off_frames"] += 1
            # выключаем только если 4 кадра подряд не идём
            if state["walk_off_frames"] >= 4 and state["step_sound_playing"]:
                step_channel.stop()
                state["step_sound_playing"] = False

    # 2) камера (КАЖДЫЙ КАДР)
        update_camera_center_smooth(state)
        state["bg_x"] = -(state["camera_x"] % WIDTH)

        # 4) спавнеры
        update_spawners(state, ghost)

        # 5) стрельба (создание пуль) — тут без изменений, но ВАЖНО: это ДО update_bullets
        if (not state["is_reloading"]) and state["ammo"] > 0 and (now - state["last_shot_time"] >= state["shoot_cd"]):
            if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                rect = bullet_up_right.get_rect(topleft=(state["player_x"] + 30, state["player_y"] + 3))
                state["bullets"].append({"rect": rect, "vx": 10, "vy": -10, "img": bullet_up_right})
                state["ammo"] -= 1
                state["last_shot_time"] = now
            elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                rect = bullet_up_left.get_rect(topleft=(state["player_x"] - 30, state["player_y"] + 3))
                state["bullets"].append({"rect": rect, "vx": -10, "vy": -10, "img": bullet_up_left})
                state["ammo"] -= 1
                state["last_shot_time"] = now
            elif keys[pygame.K_UP]:
                rect = bullet_up.get_rect(topleft=(state["player_x"], state["player_y"] + 3))
                state["bullets"].append({"rect": rect, "vx": 0, "vy": -10, "img": bullet_up})
                state["ammo"] -= 1
                state["last_shot_time"] = now
            elif keys[pygame.K_RIGHT]:
                rect = bullet_right.get_rect(topleft=(state["player_x"] + 30, state["player_y"] + 3))
                state["bullets"].append({"rect": rect, "vx": 10, "vy": 0, "img": bullet_right})
                state["ammo"] -= 1
                state["last_shot_time"] = now
            elif keys[pygame.K_LEFT]:
                rect = bullet_left.get_rect(topleft=(state["player_x"] - 30, state["player_y"] + 3))
                state["bullets"].append({"rect": rect, "vx": -10, "vy": 0, "img": bullet_left})
                state["ammo"] -= 1
                state["last_shot_time"] = now

        # 6) апдейт пуль — ОДИН РАЗ
        score = {"bird": state["score_bird_kills"], "ghost": state["score_ghost_kills"], "all": state["score_kills"]}
        update_bullets(state["bullets"], state["enemies"], score, state["camera_x"])
        state["score_bird_kills"] = score["bird"]
        state["score_ghost_kills"] = score["ghost"]
        state["score_kills"] = score["all"]

        # 7) коллизия с врагами (после пуль)
        player_rect = player.get_rect(topleft=(state["player_x"], state["player_y"]))
        update_enemies(state, player_rect)
    #==============================================================================================================================================================================|
    #-------------------------------------------------------- Передвижение игрока и заднего фона ----------------------------------------------------------------------------------|
    #==============================================================================================================================================================================|

        state["bg_x"] = -(state["camera_x"] % WIDTH)
    #==============================================================================================================================================================================|
    #--------------------------------------------------------- Перезарядка (функция + аним) ---------------------------------------------------------------------------------------|
    #==============================================================================================================================================================================|

        if state["ammo"] == 0 and not state["is_shaking"]:
            state["is_shaking"] = True
            state["shake_start_time"] = pygame.time.get_ticks()

        shake_offset = 0
        current_time = pygame.time.get_ticks()
        if state["is_shaking"]:
            if current_time - state["shake_start_time"] < 3000:
                shake_offset = random.randint(-3, 3)
            else:
                state["is_shaking"] = False

        current_time = pygame.time.get_ticks()

        if state["is_reloading"]:

            if current_time - state["last_reload_step"] >= state["bullet_reload_delay"]:

                if state["ammo"] < state["max_ammo"]:
                    state["ammo"] += 1
                    state["last_reload_step"] = current_time

                if state["ammo"] == state["max_ammo"]:
                    state["is_reloading"] = False

    #==============================================================================================================================================================================|
    #----------------------------------------------------------------------------------- Стрельба ---------------------------------------------------------------------------------|
    #==============================================================================================================================================================================|

        if (not state["is_reloading"]) and state["ammo"] > 0 and (now - state["last_shot_time"] >= state["shoot_cd"]):

            if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                rect = bullet_up_right.get_rect(topleft=(state["player_x"] + 30, state["player_y"] + 3))
                state["bullets"].append({"rect": rect, "vx": 10, "vy": -10, "img": bullet_up_right})
                state["ammo"] -= 1
                state["last_shot_time"] = now

            elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                rect = bullet_up_left.get_rect(topleft=(state["player_x"] - 30, state["player_y"] + 3))
                state["bullets"].append({"rect": rect, "vx": -10, "vy": -10, "img": bullet_up_left})
                state["ammo"] -= 1
                state["last_shot_time"] = now

            elif keys[pygame.K_UP]:
                rect = bullet_up.get_rect(topleft=(state["player_x"], state["player_y"] + 3))
                state["bullets"].append({"rect": rect, "vx": 0, "vy": -10, "img": bullet_up})
                state["ammo"] -= 1
                state["last_shot_time"] = now

            elif keys[pygame.K_RIGHT]:
                rect = bullet_right.get_rect(topleft=(state["player_x"] + 30, state["player_y"] + 3))
                state["bullets"].append({"rect": rect, "vx": 10, "vy": 0, "img": bullet_right})
                state["ammo"] -= 1
                state["last_shot_time"] = now

            elif keys[pygame.K_LEFT]:
                rect = bullet_left.get_rect(topleft=(state["player_x"] - 30, state["player_y"] + 3))
                state["bullets"].append({"rect": rect, "vx": -10, "vy": 0, "img": bullet_left})
                state["ammo"] -= 1
                state["last_shot_time"] = now

    #==============================================================================================================================================================================|
    #---------------------------------------------------------------------- Экран проигрыша ---------------------------------------------------------------------------------------|
    #==============================================================================================================================================================================|

    draw(screen, bg, score_label, state,
     player, walk_left, walk_right, keys,
     ghost, bird_left, bird_right)
    pygame.display.update()

    clock.tick(30)