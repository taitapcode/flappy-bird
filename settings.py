import pygame, os

# Initialization
pygame.init()
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
WIDTH, HEIGHT = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
DIR_PATH = os.path.dirname(__file__)
MAIN_FONT = pygame.font.Font(f'{DIR_PATH}/assets/04B_19.TTF', 45)
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}

# Images
BG_IMAGE = pygame.image.load(f'{DIR_PATH}/assets/images/day.png').convert()
BASE_IMAGE = pygame.image.load(f'{DIR_PATH}/assets/images/base.png').convert()
MENU_IMAGE = pygame.image.load(f'{DIR_PATH}/assets/images/menu.png')

BIRD_DOWNFLAP_IMAGE = pygame.image.load(f'{DIR_PATH}/assets/images/downflap.png').convert_alpha()
BIRD_MIDFLAP_IMAGE = pygame.image.load(f'{DIR_PATH}/assets/images/midflap.png').convert_alpha()
BIRD_UPFLAP_IMAGE = pygame.image.load(f'{DIR_PATH}/assets/images/upflap.png').convert_alpha()

PIPE_IMAGE = pygame.image.load(f'{DIR_PATH}/assets/images/pipe.png').convert()

# Sounds
SCORE_SOUND = pygame.mixer.Sound(f'{DIR_PATH}/assets/sounds/point.wav')
SCORE_SOUND.set_volume(0.15)

LOST_SOUND = pygame.mixer.Sound(f'{DIR_PATH}/assets/sounds/die.wav')
LOST_SOUND.set_volume(0.35)
