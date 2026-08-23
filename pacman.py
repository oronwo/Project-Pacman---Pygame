import pygame #import pygame module, the main module the game will run
from sys import exit #basically imports the exit option on the pygame window
import os

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

class Block(pygame.Rect): #inheritance, i am creating a new class (block) that takes functionalities of the rect obj and i can create more of them without altering the original rect obj
    def __init__(self, x, y, width, height, image):
        pygame.Rect.__init__(self, x, y, width, height)
        self.image = image
        self.direction = 'R'

    def update_direction(self, direction):
        self.direction = direction

def load_image(image_name, scale=None): #setting function to load and resize image in only one line. ex on #game sprites
    image = pygame.image.load(os.path.join("images", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

#game sprites
PACMAN_RIGHT_IMAGE = load_image("pacmanRight.png", (TILE_SIZE, TILE_SIZE))
PACMAN_LEFT_IMAGE = load_image("pacmanLeft.png", (TILE_SIZE, TILE_SIZE))
PACMAN_UP_IMAGE = load_image("pacmanUp.png", (TILE_SIZE, TILE_SIZE))
PACMAN_DOWN_IMAGE = load_image("pacmanDown.png", (TILE_SIZE, TILE_SIZE))
WALL_IMAGE = load_image("wall.png", (TILE_SIZE, TILE_SIZE))
BLUE_GHOST_IMAGE= load_image("blueGhost.png", (TILE_SIZE, TILE_SIZE))
ORANGE_GHOST_IMAGE= load_image("orangeGhost.png", (TILE_SIZE, TILE_SIZE))
PINK_GHOST_IMAGE= load_image("pinkGhost.png", (TILE_SIZE, TILE_SIZE))
RED_GHOST_IMAGE= load_image("redGhost.png", (TILE_SIZE, TILE_SIZE))
POWER_FOOD_IAMGE= load_image("powerFood.png", (TILE_SIZE/2, TILE_SIZE/2))

pygame.init() #needed in every pygame project, starts the module
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT)) #setmode creates the window, we usually get the size from the monitor to calculate a preferrable window size
pygame.display.set_caption("Pacman") #names the game window
pygame.display.set_icon(PACMAN_RIGHT_IMAGE) #sets the pacman right image as the window icon
clock = pygame.time.Clock() #variable of time/framerate assigned to clock


pacman = None #sets the variable for pacman, first two numbers are x and y starting points, last two are width and height
walls = []
foods = []
ghosts = []
power_foods = []

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
                ghost = Block(x, y, TILE_SIZE, TILE_SIZE, BLUE_GHOST_IMAGE)
                ghosts.append(ghost)

            elif tile_map_char == 'o': #ghosts
                ghost = Block(x, y, TILE_SIZE, TILE_SIZE, ORANGE_GHOST_IMAGE)
                ghosts.append(ghost)

            elif tile_map_char == 'p': #ghosts
                ghost = Block(x, y, TILE_SIZE, TILE_SIZE, PINK_GHOST_IMAGE)
                ghosts.append(ghost)

            elif tile_map_char == 'r': #ghosts
                ghost = Block(x, y, TILE_SIZE, TILE_SIZE, RED_GHOST_IMAGE)
                ghosts.append(ghost)

            elif tile_map_char == 'P': #Pacman :)
                pacman = Block(x, y, TILE_SIZE, TILE_SIZE, PACMAN_RIGHT_IMAGE) #this is a local variable, i made it global on the def loadmap line

            elif tile_map_char == '+':
                food = Block(x + 8, y + 8, TILE_SIZE/2, TILE_SIZE/2, POWER_FOOD_IAMGE)
                power_foods.append(food)

            elif tile_map_char == ' ':
                food = Block(x + 14, y + 14, 4, 4, None)
                foods.append(food)
               
load_map()

def draw(): #setting the function responsible for drawing the visuals // order matters so every layer will be put on the last layers surface
    window.fill("black")
    window.blit(pacman.image, pacman)

    for wall in walls:
        window.blit(wall.image, wall)

    for food in foods:
        pygame.draw.rect(window, "white", food)

    for food in power_foods:
        window.blit(food.image, food)

    for ghost in ghosts:
        window.blit(ghost.image, ghost)

while True: #sets a loop to keep the window opened until the player manually closes it
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #makes the window closeable by clicking on the X button
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
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
                pacman.image = PACMAN_UP_IMAGE
            elif pacman.direction == 'D':
                pacman.image = PACMAN_DOWN_IMAGE
            elif pacman.direction == 'L':
                pacman.image = PACMAN_LEFT_IMAGE
            elif pacman.direction == 'R':
                pacman.image = PACMAN_RIGHT_IMAGE

    draw() #keeps the visuals opened
    pygame.display.update() #keeps it open
    clock.tick(60) #runs at 60fps