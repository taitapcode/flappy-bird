# Import
import pygame, sys, random, os

# Initialization
pygame.init()

WIDTH, HEIGHT = 600, 800
DIR_PATH = os.path.dirname(__file__)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
main_font = pygame.font.Font(f'{DIR_PATH}/assets/04B_19.TTF', 45)
colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}


# Load Images
bg_img = pygame.image.load(f'{DIR_PATH}/assets/images/bg-day.png').convert()
base_img = pygame.image.load(f'{DIR_PATH}/assets/images/base.png').convert()
menu_img = pygame.image.load(f'{DIR_PATH}/assets/images/menu.png')

bird_downflap_img = pygame.image.load(f'{DIR_PATH}/assets/images/bird-downflap.png').convert_alpha()
bird_midflap_img = pygame.image.load(f'{DIR_PATH}/assets/images/bird-midflap.png').convert_alpha()
bird_upflap_img = pygame.image.load(f'{DIR_PATH}/assets/images/bird-upflap.png').convert_alpha()

pipe_img = pygame.image.load(f'{DIR_PATH}/assets/images/pipe.png').convert()


# Load Sound
score_sound = pygame.mixer.Sound(f'{DIR_PATH}/assets/sounds/point.wav')
lost_sound = pygame.mixer.Sound(f'{DIR_PATH}/assets/sounds/die.wav')
score_sound.set_volume(0.15)
lost_sound.set_volume(0.35)


class Bird:
    def __init__(self: any):
        self.down_flap_img = pygame.transform.scale(bird_downflap_img, (50, 35))
        self.mid_flap_img = pygame.transform.scale(bird_midflap_img, (50, 35))
        self.up_flap_img = pygame.transform.scale(bird_upflap_img, (50, 35))
        self.GRAVITY = 0.1
        self.movement = 0
        self.x = 100
        self.y = 200
        self.list_animations = [self.down_flap_img, self.mid_flap_img, self.up_flap_img, self.mid_flap_img]
        self.animation_index = 0
        self.img = self.list_animations[self.animation_index]
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.BIRD_FLAP = pygame.USEREVENT + 1

        pygame.time.set_timer(self.BIRD_FLAP, 200)

    def rotate_bird(self: any, bird: pygame.image.load):
        return pygame.transform.rotozoom(bird, -self.movement * 3, 1)

    def animations(self: any):
        new_bird = self.list_animations[self.animation_index]
        new_rect = new_bird.get_rect(center=(self.x, self.rect.centery))
        return new_bird, new_rect

    def draw(self: any):
        self.movement += self.GRAVITY
        rotate_bird = self.rotate_bird(self.img)
        self.rect.centery += self.movement
        screen.blit(rotate_bird, self.rect)


class Pipes:
    def __init__(self: any):
        self.img = pygame.transform.scale(pipe_img, (80, 450))
        self.pipe_list = []
        self.x = WIDTH + self.img.get_rect().width / 2
        self.y = random.randint(375, 625)
        self.TIME_SPAWN = pygame.USEREVENT

        pygame.time.set_timer(self.TIME_SPAWN, 900)

    def create(self: any):
        self.y = random.randint(350, 575)
        bottom_pipe = self.img.get_rect(midtop=(self.x, self.y))
        top_pipe = self.img.get_rect(midbottom=(self.x, self.y - 150))

        return bottom_pipe, top_pipe

    def move(self: any):
        for pipe in self.pipe_list:
            pipe.centerx -= 4
        new_pipes = [pipe for pipe in self.pipe_list if pipe.right > -80]

        return new_pipes

    def draw(self: any):
        for pipe in self.pipe_list:
            if pipe.bottom >= HEIGHT:
                screen.blit(self.img, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.img, False, True)
                screen.blit(flip_pipe, pipe)


class Game:
    def __init__(self: any):
        self.bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        self.base_img = pygame.transform.scale(base_img, (WIDTH, 150))
        self.menu_img = pygame.transform.scale(menu_img, (350, 490))
        self.base_x = 0
        self.base_y = 675
        self.is_start = False
        self.score = 0
        self.high_score = 0
        self.bird = Bird()
        self.pipes = Pipes()

    def draw_base(self: any):
        screen.blit(self.base_img, (self.base_x, self.base_y))
        screen.blit(self.base_img, (self.base_x + WIDTH, self.base_y))

    def draw_menu(self: any):
        menu_rect = self.menu_img.get_rect(midtop=(WIDTH / 2, 110))
        screen.blit(self.menu_img, menu_rect)

    def is_collision(self: any, pipes: Pipes, bird: Bird):
        for pipe in pipes.pipe_list:
            if bird.rect.colliderect(pipe):
                lost_sound.play()
                return False

        if bird.rect.top <= -35 or bird.rect.bottom >= self.base_y:
            lost_sound.play()
            return False

        return True

    def check_score(self: any, pipes: Pipes):
        for pipe in pipes.pipe_list[::2]:
            if pipe.centerx == 100:
                self.score += 1
                score_sound.play()

    def score_display(self: any):
        if self.is_start:
            score_text = main_font.render(str(self.score), True, colors['white'])
            score_rect = score_text.get_rect(midtop=(WIDTH / 2, 50))
            screen.blit(score_text, score_rect)
        else:
            score_text = main_font.render(f'Score: {self.score}', True, colors['white'])
            score_rect = score_text.get_rect(midtop=(WIDTH / 2, 20))
            screen.blit(score_text, score_rect)

            high_score_text = main_font.render(f'High Score: {self.high_score}', True, colors['white'])
            high_score_rect = high_score_text.get_rect(midtop=(WIDTH / 2, 620))
            screen.blit(high_score_text, high_score_rect)

    def update_high_score(self: any):
        if self.high_score < self.score:
            self.high_score = self.score

    def update_game(self: any):
        screen.fill(colors['black'])
        screen.blit(self.bg_img, (0, 0))
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.is_start:
                    self.bird.movement = -4
                elif event.key == pygame.K_SPACE and self.is_start == False:
                    self.bird.movement = -2
                    self.pipes.pipe_list.clear()
                    self.is_start = True
                    self.bird.rect.center = (self.bird.x, self.bird.y)
                    self.score = 0
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == self.pipes.TIME_SPAWN:
                self.pipes.pipe_list.extend(self.pipes.create())
            elif event.type == self.bird.BIRD_FLAP:
                if self.bird.animation_index < 3:
                    self.bird.animation_index += 1
                else:
                    self.bird.animation_index = 0

                self.bird.img, self.bird.rect = self.bird.animations()

        if self.is_start:
            # Bird
            self.bird.draw()

            # Pipes
            self.pipes.pipe_list = self.pipes.move()
            self.pipes.draw()

            self.check_score(self.pipes)
            self.is_start = self.is_collision(self.pipes, self.bird)
        else:
            self.draw_menu()
            self.update_high_score()

        # Other
        self.draw_base()
        self.base_x -= 4
        if self.base_x == -WIDTH:
            self.base_x = 0
        self.score_display()

    def run(self: any):
        while True:
            self.update_game()
            pygame.display.update()

# Run
if __name__ == "__main__":
    Game().run()
