import pygame, sys, random
from settings import *

class Bird:
    def __init__(self, x: int, y: int, jump_high: int):
        self.down_flap_img = pygame.transform.scale(BIRD_DOWNFLAP_IMAGE, (50, 35))
        self.mid_flap_img = pygame.transform.scale(BIRD_MIDFLAP_IMAGE, (50, 35))
        self.up_flap_img = pygame.transform.scale(BIRD_UPFLAP_IMAGE, (50, 35))
        self.GRAVITY = 0.1
        self.movement = 0
        self.x = x
        self.y = y
        self.jump_high = jump_high
        self.list_animations = [
            self.down_flap_img,
            self.mid_flap_img,
            self.up_flap_img,
            self.mid_flap_img
        ]
        self.animation_index = 0
        self.img = self.list_animations[self.animation_index]
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.BIRD_FLAP = pygame.USEREVENT + 1

        pygame.time.set_timer(self.BIRD_FLAP, 200)

    def rotate_bird(self, bird: pygame.image.load):
        return pygame.transform.rotozoom(bird, -self.movement * 3, 1)

    def animations(self):
        new_bird = self.list_animations[self.animation_index]
        new_rect = new_bird.get_rect(center=(self.x, self.rect.centery))
        return new_bird, new_rect

    def handle_event(self, event: pygame.event.Event, is_start: bool):
        if event.type == self.BIRD_FLAP:
            if self.animation_index < 3:
                self.animation_index += 1
            else:
                self.animation_index = 0

            self.img, self.rect = self.animations()
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or not is_start:
                self.movement = -self.jump_high


    def draw(self):
        self.movement += self.GRAVITY
        rotate_bird = self.rotate_bird(self.img)
        self.rect.centery += self.movement
        SCREEN.blit(rotate_bird, self.rect)


class Pipes:
    def __init__(self):
        self.img = pygame.transform.scale(PIPE_IMAGE, (80, 450))
        self.pipe_list: list[pygame.Rect] = []
        self.x = WIDTH + self.img.get_rect().width / 2
        self.y = random.randint(375, 625)
        self.TIME_SPAWN = pygame.USEREVENT

        pygame.time.set_timer(self.TIME_SPAWN, 900)

    def create(self):
        self.y = random.randint(350, 575)
        bottom_pipe = self.img.get_rect(midtop=(self.x, self.y))
        top_pipe = self.img.get_rect(midbottom=(self.x, self.y - 150))

        return bottom_pipe, top_pipe

    def handle_event(self, event: pygame.event.Event):
        if event.type != self.TIME_SPAWN:
            return

        self.pipe_list.extend(self.create())

    def move(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 4
        new_pipes = [pipe for pipe in self.pipe_list if pipe.right > -80]

        return new_pipes

    def draw(self):
        for pipe in self.pipe_list:
            if pipe.bottom >= HEIGHT:
                SCREEN.blit(self.img, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.img, False, True)
                SCREEN.blit(flip_pipe, pipe)


class Game:
    def __init__(self):
        self.bg_img = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))
        self.base_img = pygame.transform.scale(BASE_IMAGE, (WIDTH, 150))
        self.menu_img = pygame.transform.scale(MENU_IMAGE, (350, 490))
        self.base_x = 0
        self.base_y = 675
        self.is_start = False
        self.score = 0
        self.high_score = 0
        self.bird = Bird(100, 200, 4)
        self.pipes = Pipes()

    def is_collision(self, pipes: Pipes, bird: Bird):
        for pipe in pipes.pipe_list:
            if bird.rect.colliderect(pipe):
                LOST_SOUND.play()
                return False

        if bird.rect.top <= -35 or bird.rect.bottom >= self.base_y:
            LOST_SOUND.play()
            return False

        return True

    def check_score(self, pipes: Pipes):
        for pipe in pipes.pipe_list[::2]:
            if pipe.centerx == 100:
                self.score += 1
                SCORE_SOUND.play()

    def base_movement(self):
        self.base_x -= 4
        if self.base_x == -WIDTH:
            self.base_x = 0

    def update_high_score(self):
        if self.high_score < self.score:
            self.high_score = self.score

    def handle_game_event(self):
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Restart game
                if event.key == pygame.K_SPACE and not self.is_start:
                    self.bird.movement = -2
                    self.pipes.pipe_list.clear()
                    self.is_start = True
                    self.bird.rect.center = (self.bird.x, self.bird.y)
                    self.score = 0
                # Quit
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            self.bird.handle_event(event, self.is_start)
            self.pipes.handle_event(event)

    def draw_base(self):
        SCREEN.blit(self.base_img, (self.base_x, self.base_y))
        SCREEN.blit(self.base_img, (self.base_x + WIDTH, self.base_y))

    def draw_menu(self):
        menu_rect = self.menu_img.get_rect(midtop=(WIDTH / 2, 110))
        SCREEN.blit(self.menu_img, menu_rect)

    def draw_score(self):
        if self.is_start:
            score_text = MAIN_FONT.render(str(self.score), True, COLORS['white'])
            score_rect = score_text.get_rect(midtop=(WIDTH / 2, 50))
            SCREEN.blit(score_text, score_rect)
        else:
            score_text = MAIN_FONT.render(f'Score: {self.score}', True, COLORS['white'])
            score_rect = score_text.get_rect(midtop=(WIDTH / 2, 20))
            SCREEN.blit(score_text, score_rect)

            high_score_text = MAIN_FONT.render(f'High Score: {self.high_score}', True, COLORS['white'])
            high_score_rect = high_score_text.get_rect(midtop=(WIDTH / 2, 620))
            SCREEN.blit(high_score_text, high_score_rect)

    def draw(self):
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
        self.draw_score()
        self.draw_base()

    def update_game(self):
        SCREEN.blit(self.bg_img, (0, 0))
        clock.tick(120) # Lock FPS
        self.handle_game_event()
        self.draw()
        self.base_movement()

    def run(self):
        while True:
            self.update_game()
            pygame.display.update()

# Main
if __name__ == "__main__":
    game = Game()
    game.run()
