import pygame
import sys
from pygame.locals import QUIT, Rect, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN, KEYUP
from math import ceil
from random import randint

Display_width = 1200
Display_height = 800

Surface_width = 1200
Surface_height = 800

display_ratio_x = Display_width / Surface_width
display_ratio_y = Display_height / Surface_height

FPS = 40

pygame.init()
DISPLAY = pygame.display.set_mode((Display_width, Display_height))
SURFACE = pygame.Surface((Surface_width, Surface_height))
FPSCLOCK = pygame.time.Clock()

game_display_rect = Rect(100, 100, 1000, 500)
GAME_DISPLAY = pygame.Surface(game_display_rect.size)

dinosaur_width = 80
dinosaur_height = 60

dinosaur_image = pygame.transform.scale(pygame.image.load("resources/dinosaur.png"), (dinosaur_width, dinosaur_height * 3))

dinosaur_position = 100

ground = 400
ground_piece_width = 240
ground_piece_height = 100
ground_image = pygame.transform.scale(pygame.image.load("resources/ground.png"), (ground_piece_width, ground_piece_height))

ground_piece_count = ceil(game_display_rect.width / ground_piece_width) + 1

start_button_rect = Rect(480, 610, 240, 80)
start_button_image = pygame.transform.scale(pygame.image.load("resources/start_button.png"),
                                            (start_button_rect.width, start_button_rect.height * 2))

retry_button_rect = Rect(480, 400, 240, 80)
retry_button_image = pygame.transform.scale(pygame.image.load("resources/retry_button.png"),
                                            (retry_button_rect.width, retry_button_rect.height * 2))

speed = 300

step_delay = 200

jump_power = 1100
gravity = 4000
boost_power = 1600

cactus_types = ((20, 80), (20, 60))
cactus_counts = ((1, 4), (1, 4))

cactus_images = []
for index, size in enumerate(cactus_types):
    cactus_images.append(pygame.transform.scale(pygame.image.load("resources/cactus{}.png".format(index)), size))

cactus_create_distance_min = 270
cactus_create_distance_max = 600

gameover_message_rect = Rect(200, 250, 800, 80)
gameover_message_image = pygame.transform.scale(pygame.image.load("resources/gameover_message.png"),
                                                gameover_message_rect.size)

score_text_height = 40
score_text_topleft = (100, 30)
score_text_prefix_width = 192

score_text_prefix_image = pygame.transform.scale(pygame.image.load("resources/score.png"),
                                                 (score_text_prefix_width, score_text_height))

score_number_width = 32

score_number_image = pygame.transform.scale(pygame.image.load("resources/numbers.png"),
                                                  (score_number_width * 10, score_text_height))


class Cactus:
    def __init__(self):
        self.type = randint(0, len(cactus_types) - 1)
        self.count = randint(cactus_counts[self.type][0], cactus_counts[self.type][1])

        self.position = game_display_rect.width

    def draw(self):
        for repeat in range(self.count):
            GAME_DISPLAY.blit(cactus_images[self.type], (self.position + repeat * cactus_types[self.type][0],
                                                         ground - cactus_types[self.type][1]))

    def test(self, jumping_height):
        if jumping_height < cactus_types[self.type][1]:
            if dinosaur_position < self.position < dinosaur_width + dinosaur_position:
                print(1)
                return True
            if dinosaur_position < self.position + cactus_types[self.type][0] * self.count < dinosaur_width + dinosaur_position:
                print(2)
                return True
            if self.position < dinosaur_position < self.position + cactus_types[self.type][0] * self.count:
                print(3)
                return True
            if self.position < dinosaur_position + dinosaur_width < self.position + cactus_types[self.type][0] * self.count:
                print(4)

                return True

            else:
                return False


def main():
    FLAG = 0
    dinosaur_situation = 2
    dinosaur_situation_delay = 0

    start_button_clicked = 0
    retry_button_clicked = 0

    distance = 0

    jumping = False
    jumping_height = 0
    force = 0

    cactus_create_distance = randint(cactus_create_distance_min, cactus_create_distance_max)

    boosting = False

    CACTI = []

    while True:
        pygame_events = pygame.event.get()
        for pygame_event in pygame_events:
            if pygame_event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif pygame_event.type == MOUSEBUTTONUP:
                event_pos = (pygame_event.pos[0] / display_ratio_x, pygame_event.pos[1] / display_ratio_y)

                if FLAG == 0:
                    if start_button_rect.collidepoint(event_pos) and start_button_clicked:
                        FLAG = 1
                        dinosaur_situation = 0
                    start_button_clicked = 0

                elif FLAG == 2:
                    if retry_button_rect.collidepoint(event_pos) and retry_button_clicked:
                        FLAG = 0
                        dinosaur_situation = 2
                        dinosaur_situation_delay = 0

                        distance = 0
                        jumping = False
                        jumping_height = 0
                        force = 0
                        cactus_create_distance = randint(cactus_create_distance_min, cactus_create_distance_max)
                        boosting = False
                        CACTI = []

                    retry_button_clicked = 0


            elif pygame_event.type == MOUSEBUTTONDOWN:
                event_pos = (pygame_event.pos[0] / display_ratio_x, pygame_event.pos[1] / display_ratio_y)

                if FLAG == 0:
                    if start_button_rect.collidepoint(event_pos):
                        start_button_clicked = 1

                elif FLAG == 2:
                    if retry_button_rect.collidepoint(event_pos):
                        retry_button_clicked = 1

            elif pygame_event.type == KEYDOWN:
                if FLAG == 1:
                    if pygame_event.key == pygame.K_SPACE:
                        jumping = True
                        force = jump_power
                        boosting = True

            elif pygame_event.type == KEYUP:
                if pygame_event.key == pygame.K_SPACE:
                    boosting = False

        if FLAG == 1:
            distance += speed / FPS
            if distance >= cactus_create_distance:
                cactus_create_distance += randint(cactus_create_distance_min, cactus_create_distance_max)
                CACTI.append(Cactus())

            for index in range(len(CACTI)):
                CACTI[index].position -= speed / FPS
                if CACTI[index].position + (CACTI[index].count - 1) * cactus_types[CACTI[index].type][0] < 0:
                    CACTI[index] = 0
            for repeat in range(CACTI.count(0)):
                CACTI.remove(0)

            if jumping:
                force -= gravity / FPS
                if boosting:
                    force += boost_power / FPS
                jumping_height += force / FPS

                if jumping_height <= 0:
                    jumping = False
                    jumping_height = 0

                dinosaur_situation = 2
                dinosaur_situation_delay = 0

            else:
                dinosaur_situation_delay += 1000 / FPS

                if dinosaur_situation_delay >= step_delay:
                    dinosaur_situation += dinosaur_situation_delay // step_delay
                    dinosaur_situation %= 2
                    dinosaur_situation_delay %= step_delay

            for index in range(len(CACTI)):
                if CACTI[index].test(jumping_height):
                    FLAG = 2

        SURFACE.fill((255, 255, 255))
        GAME_DISPLAY.fill((255, 255, 255))

        for index in range(len(CACTI)):
            CACTI[index].draw()

        GAME_DISPLAY.blit(dinosaur_image, (dinosaur_position, ground - dinosaur_height - jumping_height),
                          (0, dinosaur_situation * dinosaur_height, dinosaur_width, dinosaur_height))
        for repeat in range(ground_piece_count):
            GAME_DISPLAY.blit(ground_image, (repeat * ground_piece_width - distance % ground_piece_width, ground))

        SURFACE.blit(GAME_DISPLAY, game_display_rect.topleft)

        pygame.draw.rect(SURFACE, (63, 63, 63), game_display_rect, 5)

        if FLAG == 0:
            SURFACE.blit(start_button_image, start_button_rect.topleft,
                         ((0, start_button_rect.height * start_button_clicked), start_button_rect.size))

        if FLAG == 2:
            SURFACE.blit(gameover_message_image, gameover_message_rect.topleft)
            SURFACE.blit(retry_button_image, retry_button_rect.topleft,
                         (0, retry_button_rect.height * retry_button_clicked,
                          retry_button_rect.width, retry_button_rect.height))

        SURFACE.blit(score_text_prefix_image, score_text_topleft)
        for index, number in enumerate(list(str(int(distance / 100)))):
            SURFACE.blit(score_number_image, (score_text_topleft[0] + score_text_prefix_width + index *
                                              score_number_width, score_text_topleft[1]),
                         (int(number) * score_number_width, 0, score_number_width, score_text_height))

        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
