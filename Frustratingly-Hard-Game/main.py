# Frustratingly Hard Game
# By Jelly
# This code may be reproduced and modified so long as proper attribution is given

# Inspired by World's Hardest Game
# From Stephen Critoph

# -------------------------------------------------------------------------------

# -------
# Imports
# -------

from json import loads
from random import randint
from sys import exit
from time import sleep

from pygame import (
    display,
    draw,
    event,
    font,
    HIDDEN,
    init,
    key,
    quit,
    Rect,
    SHOWN,
    time,
)

from pygame.locals import (
    KEYUP,
    KEYDOWN,
    K_ESCAPE,
    K_w,
    K_a,
    K_s,
    K_d,
    K_c,
    K_f,
    K_F11,
    K_LEFT,
    K_DOWN,
    K_UP,
    K_RIGHT,
    QUIT
)

# ---------
# Variables
# ---------


# Window

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

# Colors

RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (75, 0, 130)
CYAN = (0, 255, 255)
BROWN = (139, 69, 190)
LIGHTBLUE = (0, 124, 230)
LIGHTRED = (238, 75, 43)
WHITE = (255, 255, 255)
DARKGREEN = (1, 50, 32)
DARKERGREEN = (1, 30, 32)
DARKGRAY = (169, 169, 169)
BLACK = (0, 0, 0)

# Directions

LEFT = 'left'
DOWN = 'down'
UP = 'up'
RIGHT = 'right'
NW = 'north west'
SW = 'south west'
NE = 'north east'
SE = 'south east'

# Projectile movement types

UPDOWN = 'up down'
SIDETOSIDE = 'side to side'
DIAGONAL = 'diagonal'

# Splash texts that appear before
# the game is launched

STFILE = open('splashtexts.json')
STREAD = STFILE.read()

SPLASHTEXTS = loads(STREAD)

del STFILE, STREAD

# Level data

# Note that this data stays static. The actual projectiles
# and walls that show up are in the 'projectiles' and 'walls'
# lists, which get cleared every level pass or player death

LFILE = open('levels.json')
LREAD = LFILE.read()

LEVELS = loads(LREAD)

del LFILE, LREAD

# Non-constant variables

completed_level = False
completed_all_levels = False
dead = False
fails = 0
fullscreen = False
game_over = False
jx = 0
jy = 0
level = 0
lives = 5
lives_start = 5
projectiles = []
seen_how_to_play_screen = False
walls = []


# -------
# Classes
# -------


class Player:
    def __init__(self, x, y, size, speed, player_display, can_move, shown_state):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.player_display = player_display
        self.can_move = can_move
        self.shown_state = shown_state

    # Gets the graphed version of the
    # player's "y" position

    def get_x(self):
        return self.x - (WINDOWWIDTH / 2)

    # Sets the player's "x" position
    # using the implemented graphed system

    def set_x(self, i):
        self.x = x(i)

    # Changes the player's "x" postion
    # using the implemented graphed system

    def change_x(self, i):
        self.x += i

    # Gets the graphed version of the
    # player's "y" position

    def get_y(self):
        return (WINDOWHEIGHT / 2) - self.y

    # Sets the player's "y" postion
    # using the implemented graphed system

    def set_y(self, i):
        self.y = y(i)

    # Changes the player's "y" position
    # using the implemented graphed system

    def change_y(self, i):
        self.y -= i

    # Gets and returns a tuple of the
    # player's graphed version of their
    # "x" and "y" positions

    def get_x_get_y(self):
        return (self.get_x(), self.get_y())

    # Sets BOTH the player's
    # "x" and "y" positions

    def set_x_set_y(self, ix, iy):
        self.x = x(ix)
        self.y = y(iy)

    # Changes BOTH the player's
    # "x" and "y" positions

    def change_x_change_y(self, ix, iy):
        self.x += ix
        self.y -= iy


class Portal:
    def __init__(self, x, y, size, color, portal_display, shown_state):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.display = portal_display
        self.shown_state = shown_state


# ---------
# Functions
# ---------


# The parent function that runs the entire game

def main():
    global FPSCLOCK, DISPLAY, FONT, player, portal

    init()
    display.set_caption('Frustratingly Hard Game')

    player = Player(0, 0, 30, 5, '', False, 'hide')
    portal = Portal(0, 0, 40, CYAN, '', 'hide')

    FPSCLOCK = time.Clock()
    DISPLAY = display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), flags=HIDDEN)
    DISPLAY.fill(BLACK)
    FONT = font.Font('freesansbold.ttf', 18)

    display_splash_text()
    while not completed_all_levels:
        display_start_screen()
        while not game_over and not completed_all_levels:
            setup_level(level)
            run_game()
            if completed_level:
                display_win_screen()
            elif dead or game_over:
                display_game_over_screen()
    display_game_beaten_screen()


# Main function that runs the game

def run_game():
    global jx, jy, game_over, dead, completed_level

    game_over = False
    jx = 0  # jx and jy are used for
    jy = 0  # adding to the players position upon moving
    dead = False
    completed_level = False
    player.can_move = True
    player.shown_state = 'show'
    portal.shown_state = 'show'

    while not game_over and not dead and not completed_level and not completed_all_levels:
        draw_player()
        draw_projectiles()
        draw_walls()
        draw_portal()
        check_movement_events()
        check_fullscreen_events()
        check_for_quit()
        check_key_events()
        check_portal_collision()
        check_border_collision()
        check_proj_collision()
        check_wall_collision()
        update_proj_anims()
        update_player_display()
        update_fails_display()
        update_lives_display()
        update_level_display()
        display.update()
        DISPLAY.fill(BLACK)
        FPSCLOCK.tick(FPS)


# x and y functions for proper graphing

# Use these if you think that
# Pygame's graphing system sucks

def x(i):
    sx = WINDOWWIDTH / 2
    sx += i
    return int(sx)


def y(i):
    sy = WINDOWHEIGHT / 2
    if sy > 0:
        sy -= i
    else:
        sy += i
    return int(sy)


# Drawing functions

def draw_player():
    global jx, jy, player

    player.change_x(jx)
    player.change_y(jy)

    check_border_collision()  # Checks for collision with the window bounds

    if player.shown_state == 'show':
        draw.rect(DISPLAY, RED, player.player_display)

    jx = 0
    jy = 0


def draw_portal():
    global portal

    shrink_size = 10
    second_square = Rect(portal.x + shrink_size / 2, portal.y + shrink_size / 2, portal.size - shrink_size, portal.size - shrink_size)
    third_square = Rect(portal.x + (shrink_size / 2) * 2, portal.y + (shrink_size / 2) * 2, portal.size - shrink_size * 2, portal.size - shrink_size * 2)
    second_square_color = darken_color(portal.color, 50)
    third_square_color = darken_color(portal.color, 100)

    if portal.shown_state == 'show':
        portal.display = Rect(portal.x, portal.y, portal.size, portal.size)
        draw.rect(DISPLAY, portal.color, portal.display)
        draw.rect(DISPLAY, second_square_color, second_square)
        draw.rect(DISPLAY, third_square_color, third_square)


def draw_projectiles():
    for proj in projectiles:
        innerSquareColor = darken_color(proj['color'], proj['inner-square-shade'])
        proj['display'] = Rect(proj['x'], proj['y'], proj['size'], proj['size'])
        draw.rect(DISPLAY, proj['color'], proj['display'])
        draw.rect(DISPLAY, innerSquareColor, Rect(proj['x'] + 5, proj['y'] + 5, proj['size'] - 10, proj['size'] - 10))


def draw_walls():
    for w in walls:
        innerSquareColor = darken_color(w['color'], w['inner-square-shade'])
        w['rect'] = Rect(w['x'], w['y'], w['width'], w['height'])
        draw.rect(DISPLAY, w['color'], w['rect'])
        draw.rect(DISPLAY, innerSquareColor, Rect(w['x'] + 10, w['y'] + 10, w['width'] - 20, w['height'] - 20))


# Darken color function

def darken_color(color, shade):
    clr = list(color)

    for c in range(len(clr)):
        clr[c] -= shade
        if clr[c] < 0:
            clr[c] = 0

    return tuple(clr)


# This function is mainly for when
# the player gets a game over

def draw_main_objects():
    draw_player()
    draw_projectiles()
    draw_walls()
    draw_portal()
    update_fails_display()
    update_lives_display()
    update_level_display()


# Menu display functions

def display_start_screen():
    global level, lives, game_over

    r_red = randint(0, 255)
    r_green = randint(0, 255)
    r_blue = randint(0, 255)
    change_color_rate = 20

    check_key_events()

    while game_over or not lives <= 0:
        r_red += change_color_rate
        r_green += change_color_rate
        r_blue += change_color_rate

        if r_red > 255:
            r_red = randint(0, 255)
        if r_green > 255:
            r_green = randint(0, 255)
        if r_blue > 255:
            r_blue = randint(0, 255)

        logo_font = font.Font('freesansbold.ttf', 40)
        press_any_key_font = font.Font('freesansbold.ttf', 30)
        logo_surf = logo_font.render('Frustratingly Hard Game', True, (r_red, r_green, r_blue))
        press_any_key_surf = press_any_key_font.render('Press Any Key', True, WHITE)
        logo_rect = logo_surf.get_rect()
        press_any_key_rect = press_any_key_surf.get_rect()
        logo_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
        press_any_key_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT - 200))

        DISPLAY.fill(BLACK)
        DISPLAY.blit(logo_surf, logo_rect)
        DISPLAY.blit(press_any_key_surf, press_any_key_rect)
        display.update()
        FPSCLOCK.tick(FPS)

        for e in event.get():
            if e.type == QUIT:
                close()
            if e.type == KEYDOWN:
                if game_over:
                    level = 1
                    lives = lives_start
                    game_over = False
                else:
                    level = 1
                return


def display_win_screen():
    global level, completed_all_levels

    key_down_events = key.get_pressed()
    win_font = font.Font('freesansbold.ttf', 70)
    press_a_key_font = font.Font('freesansbold.ttf', 30)

    you_surf = win_font.render('YOU', True, GREEN)
    win_surf = win_font.render('WIN!!', True, GREEN)
    press_a_key_surf = press_a_key_font.render('Press a key to continue', True, WHITE)
    you_rect = you_surf.get_rect()
    win_rect = win_surf.get_rect()
    press_a_key_rect = press_a_key_surf.get_rect()
    you_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 30)
    win_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 25)
    press_a_key_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 70)

    while True in key_down_events:
        key_down_events = key.get_pressed()
        check_key_events()
        draw_main_objects()
        DISPLAY.blit(you_surf, you_rect)
        DISPLAY.blit(win_surf, win_rect)
        DISPLAY.blit(press_a_key_surf, press_a_key_rect)
        display.update()
        DISPLAY.fill(BLACK)

    event.get()

    while True:
        for e in event.get():
            if e.type == KEYDOWN:
                if level > len(LEVELS):
                    player.x = WINDOWWIDTH
                    player.y = WINDOWHEIGHT
                    portal.x = 0
                    portal.y = 0
                    player.shown_state = 'hide'
                    portal.shown_state = 'hide'
                    completed_all_levels = True
                    display.update()
                    DISPLAY.fill(BLACK)
                level += 1
                return

        draw_main_objects()
        DISPLAY.blit(you_surf, you_rect)
        DISPLAY.blit(win_surf, win_rect)
        DISPLAY.blit(press_a_key_surf, press_a_key_rect)
        display.update()
        DISPLAY.fill(BLACK)


def display_game_over_screen():
    global lives, fails, game_over

    lives -= 1

    if lives <= 0:
        game_over = True

    if not game_over:
        top_text = 'UR DED'
        bottom_text = 'LMFAOOO'
    else:
        top_text = 'GAME OVER'
        bottom_text = 'LLLLLLLLL'
        fails += 1

    key_down_events = key.get_pressed()
    main_font_display = font.Font('freesansbold.ttf', 70)
    sub_font_display = font.Font('freesansbold.ttf', 30)
    top_surf = main_font_display.render(top_text, True, LIGHTRED)
    top_rect = top_surf.get_rect()
    bottom_surf = main_font_display.render(bottom_text, True, LIGHTRED)
    bottom_rect = bottom_surf.get_rect()
    press_a_key_surf = sub_font_display.render('Press a key to restart', True, WHITE)
    press_a_key_rect = press_a_key_surf.get_rect()
    top_rect.center = (x(0), y(30))
    bottom_rect.center = (x(0), y(-25))
    press_a_key_rect.center = (x(0), y(-70))

    while True in key_down_events:
        key_down_events = key.get_pressed()
        check_key_events()
        draw_main_objects()
        DISPLAY.blit(top_surf, top_rect)
        DISPLAY.blit(bottom_surf, bottom_rect)
        DISPLAY.blit(press_a_key_surf, press_a_key_rect)
        display.update()
        DISPLAY.fill(BLACK)

    event.get()

    while True:
        for e in event.get():
            if e.type == KEYDOWN:
                return

        draw_main_objects()
        DISPLAY.blit(top_surf, top_rect)
        DISPLAY.blit(bottom_surf, bottom_rect)
        DISPLAY.blit(press_a_key_surf, press_a_key_rect)
        display.update()
        DISPLAY.fill(BLACK)


def display_game_beaten_screen():
    main_font = font.Font('freesansbold.ttf', 40)
    reward_font = font.Font('freesansbold.ttf', 20)
    beat_surf = main_font.render('YOU JUST BEAT THE GAME!!', True, WHITE)
    reward_surf = reward_font.render('Claim the code to your reward here:', True, WHITE)
    yt_link_surf = reward_font.render('https://www.youtube.com/watch?v=dQw4w9WgXcQ', True, RED)
    beat_rect = beat_surf.get_rect()
    reward_rect = reward_surf.get_rect()
    yt_link_rect = yt_link_surf.get_rect()
    beat_rect.center = (x(0), y(5))
    reward_rect.center = (x(0), y(-20))
    yt_link_rect.center = (x(0), y(-40))

    while True:
        check_key_events()
        check_fullscreen_events()
        check_for_quit()
        DISPLAY.blit(beat_surf, beat_rect)
        DISPLAY.blit(reward_surf, reward_rect)
        DISPLAY.blit(yt_link_surf, yt_link_rect)
        display.update()
        DISPLAY.fill(BLACK)


def display_splash_text():
    global DISPLAY

    sleep(1)
    DISPLAY = display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), flags=SHOWN)
    SPLASHELEMENT = randint(0, len(SPLASHTEXTS) - 1)
    splash_spacing = y(0)

    for space in range(int(len(SPLASHTEXTS[SPLASHELEMENT]['texts']) / 2)):
        if isinstance(SPLASHTEXTS[SPLASHELEMENT]['text-data']['spacing'], list):
            splash_spacing -= SPLASHTEXTS[SPLASHELEMENT]['text-data']['spacing'][space]
        elif isinstance(SPLASHTEXTS[SPLASHELEMENT]['text-data']['spacing'], int):
            splash_spacing -= SPLASHTEXTS[SPLASHELEMENT]['text-data']['spacing']
        else:
            raise Exception('key \'spacing\' must be either int or list or ints, not ' +
                            str(type(SPLASHTEXTS[SPLASHELEMENT]['text-data']['spacing'])))

    for text in range(len(SPLASHTEXTS[SPLASHELEMENT]['texts'])):
        if isinstance(SPLASHTEXTS[SPLASHELEMENT]['text-data']['color'], list):
            for element in SPLASHTEXTS[SPLASHELEMENT]['text-data']['color']:
                if isinstance(element, list) or isinstance(element, tuple):
                    COLOR = tuple(SPLASHTEXTS[SPLASHELEMENT]['text-data']['color'][text])
                    break
                elif isinstance(element, int):
                    COLOR = tuple(SPLASHTEXTS[SPLASHELEMENT]['text-data']['color'])
                    break
                else:
                    raise Exception('\'' + str(element) + '\' must be either list or tuple, not ' + str(type(element)))
        elif isinstance(SPLASHTEXTS[SPLASHELEMENT]['text-data']['color'][text], tuple):
            COLOR = SPLASHTEXTS[SPLASHELEMENT]['text-data']['color'][text]
        else:
            raise Exception('key \'color\' must be either list/tuple or list or lists/tuples, not ' +
                            str(type(SPLASHTEXTS[SPLASHELEMENT]['text-data']['color'])))

        if isinstance(SPLASHTEXTS[SPLASHELEMENT]['text-data']['size'], list):
            splash_font = font.Font('freesansbold.ttf', SPLASHTEXTS[SPLASHELEMENT]['text-data']['size'][text])
        elif isinstance(SPLASHTEXTS[SPLASHELEMENT]['text-data']['size'], int):
            splash_font = font.Font('freesansbold.ttf', SPLASHTEXTS[SPLASHELEMENT]['text-data']['size'])
        else:
            raise Exception('key \'size\' must be either int or list of ints, not ' +
                            type(SPLASHTEXTS[SPLASHELEMENT]['text-data']['size']))

        splash_surf = splash_font.render(SPLASHTEXTS[SPLASHELEMENT]['texts'][text], True, COLOR)
        splash_rect = splash_surf.get_rect()
        splash_rect.center = (x(0), splash_spacing)
        DISPLAY.blit(splash_surf, splash_rect)
        display.update()

        if isinstance(SPLASHTEXTS[SPLASHELEMENT]['text-data']['spacing'], list):
            splash_spacing += SPLASHTEXTS[SPLASHELEMENT]['text-data']['spacing'][text]
        elif isinstance(SPLASHTEXTS[SPLASHELEMENT]['text-data']['spacing'], int):
            splash_spacing += SPLASHTEXTS[SPLASHELEMENT]['text-data']['spacing']
        else:
            raise Exception('key \'spacing\' must be either int or list of ints, not ' +
                            str(type(SPLASHTEXTS[SPLASHELEMENT]['text-data']['spacing'])))

        if isinstance(SPLASHTEXTS[SPLASHELEMENT]['delays'], list):
            sleep(SPLASHTEXTS[SPLASHELEMENT]['delays'][text])
        elif isinstance(SPLASHTEXTS[SPLASHELEMENT]['delays'], (int, float)):
            sleep(SPLASHTEXTS[SPLASHELEMENT]['delays'])
        else:
            raise Exception('key \'delays\' must be either int, float or list of ints and floats, not ' +
                            str(type(SPLASHTEXTS[SPLASHELEMENT]['delays'])))

    DISPLAY = display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), flags=HIDDEN)
    sleep(1)
    DISPLAY = display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), flags=SHOWN)


# Level setup function

def setup_level(lvl):
    global projectiles, completed_all_levels

    projectiles.clear()
    walls.clear()

    if not lvl > len(LEVELS):
        player.set_x(LEVELS[level - 1]['player']['start-x'])
        player.set_y(LEVELS[level - 1]['player']['start-y'])
        portal.x = x(LEVELS[level - 1]['portal']['start-x'])
        portal.y = y(LEVELS[level - 1]['portal']['start-y'])

        for element in LEVELS[level - 1]['projectiles']:
            projectiles.append({
                'x': x(element['data']['start-x']),
                'y': y(element['data']['start-y']),
                'size': element['data']['size'],
                'move-style': element['data']['move-style'],
                'dir': element['data']['start-dir'],
                'speed': element['data']['speed'],
                'range': element['data']['range'],
                'moved': 0,
                'color': element['display']['color'],
                'inner-square-shade': element['display']['inner-square-shade']
            })

        for element in LEVELS[level - 1]['walls']:
            walls.append({
                'x': x(element['x']),  # NOTE: Pygame will start drawing the
                'y': y(element['y']),  # rect from the TOP LEFT CORNER
                'width': element['width'],
                'height': element['height'],
                'color': element['color'],
                'inner-square-shade': element['inner-square-shade']
            })

    else:
        player.x = WINDOWWIDTH
        player.y = WINDOWHEIGHT
        portal.x = 0
        portal.y = 0
        completed_all_levels = True


# Update functions

def update_player_display():
    player.player_display = Rect(player.x, player.y, player.size, player.size)


def update_fails_display():
    fails_font = font.Font('freesansbold.ttf', 20)
    fails_surf = fails_font.render('Fails: %s' % fails, True, WHITE)
    fails_rect = fails_surf.get_rect()
    fails_rect.center = (x(273), y(-185))
    DISPLAY.blit(fails_surf, fails_rect)


def update_lives_display():
    lives_font = font.Font('freesansbold.ttf', 20)
    lives_surf = lives_font.render('Lives: %s' % lives, True, WHITE)
    lives_rect = lives_surf.get_rect()
    lives_rect.center = (x(275), y(-205))
    DISPLAY.blit(lives_surf, lives_rect)


def update_level_display():
    level_font = font.Font('freesansbold.ttf', 20)
    level_surf = level_font.render('Level: %s' % level, True, WHITE)
    level_rect = level_surf.get_rect()
    level_rect.center = (x(275), y(-225))
    DISPLAY.blit(level_surf, level_rect)


def update_proj_anims():
    for proj in projectiles:
        if not proj['moved'] >= proj['range']:
            if proj['move-style'] == UPDOWN:
                if proj['dir'] == UP:
                    proj['y'] -= proj['speed']
                else:
                    proj['y'] += proj['speed']

            elif proj['move-style'] == SIDETOSIDE:
                if proj['dir'] == RIGHT:
                    proj['x'] += proj['speed']
                else:
                    proj['x'] -= proj['speed']

            elif proj['move-style'] == DIAGONAL:
                if proj['dir'] == NW:
                    proj['x'] -= proj['speed']
                    proj['y'] -= proj['speed']
                elif proj['dir'] == SE:
                    proj['x'] += proj['speed']
                    proj['y'] += proj['speed']
                elif proj['dir'] == NE:
                    proj['x'] += proj['speed']
                    proj['y'] -= proj['speed']
                elif proj['dir'] == SW:
                    proj['x'] -= proj['speed']
                    proj['y'] += proj['speed']

            proj['moved'] += proj['speed']

        else:
            proj['moved'] = 0
            if proj['move-style'] == UPDOWN:
                if proj['dir'] == UP:
                    proj['dir'] = DOWN
                else:
                    proj['dir'] = UP
            elif proj['move-style'] == SIDETOSIDE:
                if proj['dir'] == LEFT:
                    proj['dir'] = RIGHT
                else:
                    proj['dir'] = LEFT
            elif proj['move-style'] == DIAGONAL:
                if proj['dir'] == NW:
                    proj['dir'] = SE
                elif proj['dir'] == SE:
                    proj['dir'] = NW
                elif proj['dir'] == NE:
                    proj['dir'] = SW
                else:
                    proj['dir'] = NE


# Event check functions

def check_movement_events():
    global jx, jy, completed_level

    pressed = key.get_pressed()

    if pressed[K_c] or pressed[K_ESCAPE]:
        close()

    if player.can_move:
        if pressed[K_w] or pressed[K_UP]:
            jy += player.speed
        if pressed[K_a] or pressed[K_LEFT]:
            jx -= player.speed
        if pressed[K_s] or pressed[K_DOWN]:
            jy -= player.speed
        if pressed[K_d] or pressed[K_RIGHT]:
            jx += player.speed


def check_fullscreen_events():
    pressed = key.get_pressed()

    if pressed[K_f] or pressed[K_F11]:
        display.toggle_fullscreen()


def check_border_collision():
    update_player_display()

    if player.x >= WINDOWWIDTH - player.size:
        player.x = WINDOWWIDTH - player.size
    if player.x <= 0:
        player.x = 0
    if player.y >= WINDOWHEIGHT - player.size:
        player.y = WINDOWHEIGHT - player.size
    if player.y <= 0:
        player.y = 0

    update_player_display()


def check_proj_collision():
    global lives, dead, game_over

    draw_projectiles()

    for proj in projectiles:
        if Rect.colliderect(player.player_display, proj['display']):
            dead = True


def check_wall_collision():
    global dead, walls, game_over

    draw_walls()

    for w in walls:
        if Rect.colliderect(player.player_display, w['rect']):
            dead = True


def check_portal_collision():
    global completed_level

    draw_portal()

    if Rect.colliderect(player.player_display, portal.display):
        completed_level = True


def check_key_events():
    if len(event.get(QUIT)) > 0:
        close()

    key_up_events = event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_c or key_up_events[0].key == K_ESCAPE:
        close()
    return key_up_events[0].key


def check_for_quit():
    if len(event.get(QUIT)) > 0:
        close()


# Function that closes the game

def close():
    quit()
    exit()


# Run the game

if __name__ == '__main__':
    main()
