import pygame #import pygame module, the main module the game will run
from sys import exit #basically imports the exit option on the pygame window
import os
import random

#X = wall, O = skip, P = pac man, ' ' = food, + = power pellet
#Ghosts: b = blue, o = orange, p = pink, r = red
TILE_MAP = [
    "XXXXXXXXXXXXXXXXXXX",
    "X        X        X",
    "X XX XXX X XXX XX X",
    "X+               +X",
    "X XX X XXXXX X XX X",
    "X    X       X    X",
    "XXXX XXXX XXXX XXXX",
    "OOOX X       X XOOO",
    "XXXX X XXrXX X XXXX",
    "O       bpo       O",
    "XXXX X XXXXX X XXXX",
    "OOOX X       X XOOO",
    "XXXX X XXXXX X XXXX",
    "X        X        X",
    "X XX XXX X XXX XX X",
    "X+ X     P     X +X",
    "XX X X XXXXX X X XX",
    "X    X   X   X    X",
    "X XXXXXX X XXXXXX X",
    "X                 X",
    "XXXXXXXXXXXXXXXXXXX" 
]

#game variables
ROW_COUNT = 21
COLUMN_COUNT = 19
TILE_SIZE = 32
GAME_WIDTH = COLUMN_COUNT * TILE_SIZE
GAME_HEIGHT = ROW_COUNT * TILE_SIZE

DIRECTIONS = ['U', 'D', 'L', 'R']

class Block(pygame.Rect): #inheritance, i am creating a new class (block) that takes functionalities of the rect obj and i can create more of them without altering the original rect obj
    def __init__(self, x, y, width, height, image):
        pygame.Rect.__init__(self, x, y, width, height)
        self.image = image
        self.direction = 'R'

        self.velocity_x = 0
        self.velocity_y = 0

        self.start_x = x
        self.start_y = y

        self.scared = False
        self.start_image = image

        self.animation_index = 1
        self.last_animation_time = pygame.time.get_ticks()

    def update_direction(self, direction):
        prev_direction = self.direction
        self.direction = direction
        self.update_velocity()
        self.x += self.velocity_x
        self.y += self.velocity_y

        collided = False
        for wall in walls:
            if wall.colliderect(self):
                collided = True
                break

        self.x -= self.velocity_x
        self.y -= self.velocity_y
        if collided:
            self.direction = prev_direction
            self.update_velocity()

    def update_velocity(self):
        if self.direction == 'U':
           self.velocity_x = 0
           self.velocity_y = -TILE_SIZE/4

        elif self.direction == 'D':
            self.velocity_x = 0
            self.velocity_y = TILE_SIZE/4

        elif self.direction == 'L':
            self.velocity_x = -TILE_SIZE/4
            self.velocity_y = 0

        elif self.direction == 'R':
            self.velocity_x = TILE_SIZE/4
            self.velocity_y = 0

    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        self.scared = False
        self.image = self.start_image

def load_image(image_name, scale=None): #setting function to load and resize image in only one line. ex on #game sprites
    image = pygame.image.load(os.path.join("images", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image   

#game sprites
PACMAN_RIGHT_IMAGE0 = load_image("pacmanRight0.png", (TILE_SIZE, TILE_SIZE))
PACMAN_RIGHT_IMAGE1 = load_image("pacmanRight1.png", (TILE_SIZE, TILE_SIZE))
PACMAN_RIGHT_IMAGE2 = load_image("pacmanRight2.png", (TILE_SIZE, TILE_SIZE))
PACMAN_RIGHT_IMAGES = [PACMAN_RIGHT_IMAGE0, PACMAN_RIGHT_IMAGE1, PACMAN_RIGHT_IMAGE2]

PACMAN_LEFT_IMAGE0 = load_image("pacmanLeft0.png", (TILE_SIZE, TILE_SIZE))
PACMAN_LEFT_IMAGE1 = load_image("pacmanLeft1.png", (TILE_SIZE, TILE_SIZE))
PACMAN_LEFT_IMAGE2 = load_image("pacmanLeft2.png", (TILE_SIZE, TILE_SIZE))
PACMAN_LEFT_IMAGES = [PACMAN_LEFT_IMAGE0, PACMAN_LEFT_IMAGE1, PACMAN_LEFT_IMAGE2]

PACMAN_UP_IMAGE0 = load_image("pacmanUp0.png", (TILE_SIZE, TILE_SIZE))
PACMAN_UP_IMAGE1 = load_image("pacmanUp1.png", (TILE_SIZE, TILE_SIZE))
PACMAN_UP_IMAGE2 = load_image("pacmanUp2.png", (TILE_SIZE, TILE_SIZE))
PACMAN_UP_IMAGES = [PACMAN_UP_IMAGE0, PACMAN_UP_IMAGE1, PACMAN_UP_IMAGE2]

PACMAN_DOWN_IMAGE0 = load_image("pacmanDown0.png", (TILE_SIZE, TILE_SIZE))
PACMAN_DOWN_IMAGE1 = load_image("pacmanDown1.png", (TILE_SIZE, TILE_SIZE))
PACMAN_DOWN_IMAGE2 = load_image("pacmanDown2.png", (TILE_SIZE, TILE_SIZE))
PACMAN_DOWN_IMAGES = [PACMAN_DOWN_IMAGE0, PACMAN_DOWN_IMAGE1, PACMAN_DOWN_IMAGE2]

WALL_IMAGE = load_image("wall.png", (TILE_SIZE, TILE_SIZE))

BLUE_GHOST_IMAGE0 = load_image("blueGhost0.png", (TILE_SIZE, TILE_SIZE))
BLUE_GHOST_IMAGE1 = load_image("blueGhost1.png", (TILE_SIZE, TILE_SIZE))
BLUE_GHOST_IMAGES = [BLUE_GHOST_IMAGE0, BLUE_GHOST_IMAGE1]

ORANGE_GHOST_IMAGE0 = load_image("orangeGhost0.png", (TILE_SIZE, TILE_SIZE))
ORANGE_GHOST_IMAGE1 = load_image("orangeGhost1.png", (TILE_SIZE, TILE_SIZE))
ORANGE_GHOST_IMAGES = [ORANGE_GHOST_IMAGE0, ORANGE_GHOST_IMAGE1]

PINK_GHOST_IMAGE0 = load_image("pinkGhost0.png", (TILE_SIZE, TILE_SIZE))
PINK_GHOST_IMAGE1 = load_image("pinkGhost1.png", (TILE_SIZE, TILE_SIZE))
PINK_GHOST_IMAGES = [PINK_GHOST_IMAGE0, PINK_GHOST_IMAGE1]

RED_GHOST_IMAGE0 = load_image("redGhost0.png", (TILE_SIZE, TILE_SIZE))
RED_GHOST_IMAGE1 = load_image("redGhost1.png", (TILE_SIZE, TILE_SIZE))
RED_GHOST_IMAGES = [RED_GHOST_IMAGE0, RED_GHOST_IMAGE1]

SCARED_GHOST_IMAGE0 = load_image("scaredGhost0.png", (TILE_SIZE, TILE_SIZE))
SCARED_GHOST_IMAGE1 = load_image("scaredGhost1.png", (TILE_SIZE, TILE_SIZE))
SCARED_GHOST_IMAGES = [SCARED_GHOST_IMAGE0, SCARED_GHOST_IMAGE1]

POWER_FOOD_IMAGE= load_image("powerFood.png", (TILE_SIZE/2, TILE_SIZE/2))

pygame.init() #needed in every pygame project, starts the module
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT)) #setmode creates the window, we usually get the size from the monitor to calculate a preferrable window size
pygame.display.set_caption("Pacman") #names the game window
pygame.display.set_icon(PACMAN_RIGHT_IMAGE1) #sets the pacman right image as the window icon
clock = pygame.time.Clock() #variable of time/framerate assigned to clock


pacman = None #sets the variable for pacman, first two numbers are x and y starting points, last two are width and height
walls = []
foods = []
ghosts = []
power_foods = []
score = 0
lives = 3
game_over = False
scared_ghost_start_time = 0
scared_ghost_duration = 6000
animation_duration = 150

EAT_FOOD_SOUND = pygame.mixer.Sound("audio/eatFood.ogg")
EAT_GHOST_SOUND = pygame.mixer.Sound("audio/eatGhost.ogg")
PACMAN_LOSE_SOUND = pygame.mixer.Sound("audio/pacmanLose.ogg")

SIREN_BGM_PATH = "audio/siren.ogg"
SCARED_GHOST_BGM_PATH = "audio/scaredGhost.ogg"

current_music = SIREN_BGM_PATH
pygame.mixer.music.stop()
pygame.mixer.music.load(current_music)
pygame.mixer.music.play(-1, 0.0)

def load_map():
    global pacman

    walls.clear()
    foods.clear()
    power_foods.clear()
    ghosts.clear()

    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            row = TILE_MAP[r]
            tile_map_char = row[c]

            x = c*TILE_SIZE
            y = r*TILE_SIZE

            if tile_map_char == 'X': #walls
                wall = Block(x, y, TILE_SIZE, TILE_SIZE, WALL_IMAGE)
                walls.append(wall)

            elif tile_map_char == 'b': #ghosts
                ghost = Block(x, y, TILE_SIZE, TILE_SIZE, BLUE_GHOST_IMAGES)
                ghosts.append(ghost)

            elif tile_map_char == 'o': #ghosts
                ghost = Block(x, y, TILE_SIZE, TILE_SIZE, ORANGE_GHOST_IMAGES)
                ghosts.append(ghost)

            elif tile_map_char == 'p': #ghosts
                ghost = Block(x, y, TILE_SIZE, TILE_SIZE, PINK_GHOST_IMAGES)
                ghosts.append(ghost)

            elif tile_map_char == 'r': #ghosts
                ghost = Block(x, y, TILE_SIZE, TILE_SIZE, RED_GHOST_IMAGES)
                ghosts.append(ghost)

            elif tile_map_char == 'P': #Pacman :)
                pacman = Block(x, y, TILE_SIZE, TILE_SIZE, PACMAN_RIGHT_IMAGES) #this is a local variable, i made it global on the def loadmap line

            elif tile_map_char == '+':
                food = Block(x + 8, y + 8, TILE_SIZE/2, TILE_SIZE/2, POWER_FOOD_IMAGE)
                power_foods.append(food)

            elif tile_map_char == ' ':
                food = Block(x + 14, y + 14, 4, 4, None)
                foods.append(food)

    for ghost in ghosts:
        new_direction = random.choice(DIRECTIONS)
        ghost.update_direction(new_direction)
               
load_map()

def move():
    global score, lives, game_over, scared_ghost_start_time, current_music

    pacman.x += pacman.velocity_x
    pacman.y += pacman.velocity_y

    if pacman.right <= 0:
        pacman.x = GAME_WIDTH - pacman.width
    elif pacman.left >= GAME_WIDTH:
        pacman.x = 0

    for wall in walls:
        if wall.colliderect(pacman):
            pacman.x -= pacman.velocity_x
            pacman.y -= pacman.velocity_y
            break

    for ghost in ghosts:
        if pacman.colliderect(ghost): 
            if ghost.scared:
                score += 500
                EAT_GHOST_SOUND.play()
                ghost.reset_position()
            else:    
                lives -= 1
                PACMAN_LOSE_SOUND.play()
                if lives <= 0:
                    game_over = True
                    pygame.mixer.music.stop()
                    current_music = ""
                    return
                reset_positions()
            if current_music != SIREN_BGM_PATH:
                pygame.mixer.music.stop()
                current_music = SIREN_BGM_PATH
                pygame.mixer.music.load(current_music)
                pygame.mixer.music.play(-1, 0.0)


        if ghost.right <= 0:
            ghost.x = GAME_WIDTH - ghost.width

        elif ghost.left >= GAME_WIDTH:
            ghost.x = 0

        if ghost.y == TILE_SIZE*9 and ghost.direction != 'U' and ghost.direction != 'D':
            if random.random() < 0.5:
                ghost.update_direction('U')
            else:
                ghost.update_direction('D')

        elif ghost.x == pacman.x:
            if ghost.y < pacman.y:
                ghost.update_direction('U if ghost.scared else D')
            elif ghost.y > pacman.y:
                ghost.update_direction('D if ghost.scared else U')

        elif ghost.y == pacman.y:
            if ghost.x < pacman.x:
                ghost.update_direction('L if ghost.scared else R')
            elif ghost.x > pacman.x:
                ghost.update_direction('R if ghost.scared else L')

        ghost.x += ghost.velocity_x
        ghost.y += ghost.velocity_y

        for wall in walls:
            if wall.colliderect(ghost):
                ghost.x -= ghost.velocity_x
                ghost.y -= ghost.velocity_y
                new_direction = random.choice(DIRECTIONS)
                ghost.update_direction(new_direction)
                break

    for food in foods:
        if pacman.colliderect(food):
            foods.remove(food)
            score += 10
            if not pygame.mixer.get_busy():
                EAT_FOOD_SOUND.play()
            break

    if len(foods) ==0:
        load_map()
        reset_positions()
        lives = (lives + 1)

    for food in power_foods:
        if pacman.colliderect(food):
            for ghost in ghosts:
                ghost.scared = True  
                ghost.image = SCARED_GHOST_IMAGES 
            scared_ghost_start_time = pygame.time.get_ticks()
            power_foods.remove(food)

            if current_music != SCARED_GHOST_BGM_PATH:
                pygame.mixer.music.stop()
                current_music = SCARED_GHOST_BGM_PATH
                pygame.mixer.music.load(current_music)
                pygame.mixer.music.play(-1, 0.0)

            break

def draw(): #setting the function responsible for drawing the visuals // order matters so every layer will be put on the last layers surface
    window.fill("black")
    window.blit(pacman.image[pacman.animation_index], pacman)

    for wall in walls:
        window.blit(wall.image, wall)

    for food in foods:
        pygame.draw.rect(window, "white", food)

    for food in power_foods:
        window.blit(food.image, food)

    for ghost in ghosts:
        window.blit(ghost.image[ghost.animation_index], ghost)

    text_str = "x" + str(lives) + " SCORE: " + str(score)
    if game_over:
        text_str = "x" + str(lives) + " GAME OVER: " + str(score)

    text_font = pygame.font.SysFont("Comic Sans MS", TILE_SIZE//2)
    text_render = text_font.render(text_str, True, "white")
    window.blit(text_render, (5, 0))

def reset_positions():
    pacman.reset_position()
    pacman.velocity_x = 0
    pacman.velocity_y = 0
    for ghost in ghosts:
        ghost.reset_position()
        new_direction = random.choice(DIRECTIONS)
        ghost.update_direction(new_direction)

while True: #sets a loop to keep the window opened until the player manually closes it
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #makes the window closeable by clicking on the X button
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if game_over:
                game_over = False
                load_map()
                reset_positions()
                lives = 3
                score = 0
            if current_music != SIREN_BGM_PATH:
                pygame.mixer.music.stop()
                current_music = SIREN_BGM_PATH
                pygame.mixer.music.load(current_music)
                pygame.mixer.music.play(-1, 0.0)


            #if event.key == pygame.K_UP or event.key == pygame.K_w: long version of the same line below this one, noting just for learning purposes
            if event.key in (pygame.K_UP, pygame.K_w):
                pacman.update_direction('U')
            if event.key in (pygame.K_DOWN, pygame.K_s):
                pacman.update_direction('D')  
            if event.key in (pygame.K_LEFT, pygame.K_a):
                pacman.update_direction('L')
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                pacman.update_direction('R') 

            if pacman.direction == 'U':
                pacman.image = PACMAN_UP_IMAGES
            elif pacman.direction == 'D':
                pacman.image = PACMAN_DOWN_IMAGES
            elif pacman.direction == 'L':
                pacman.image = PACMAN_LEFT_IMAGES
            elif pacman.direction == 'R':
                pacman.image = PACMAN_RIGHT_IMAGES

    if not game_over:
        now = pygame.time.get_ticks()
        if now - scared_ghost_start_time >= scared_ghost_duration:
            for ghost in ghosts:
                ghost.scared = False
                ghost.image = ghost.start_image

            if current_music != SIREN_BGM_PATH:
                pygame.mixer.music.stop()
                current_music = SIREN_BGM_PATH
                pygame.mixer.music.load(current_music)
                pygame.mixer.music.play(-1, 0.0)

        if now - pacman.last_animation_time >= animation_duration:
            pacman.animation_index = (pacman.animation_index + 1) % len(pacman.image)
            pacman.last_animation_time = now

        for ghost in ghosts:
            if now - ghost.last_animation_time >= animation_duration:
                ghost.animation_index = (ghost.animation_index + 1) % len(ghost.image)
                ghost.last_animation_time = now
        
        move()
        draw() #keeps the visuals opened
        pygame.display.update() #keeps it open
        clock.tick(20) #runs at (x)fps