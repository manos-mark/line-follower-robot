import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

def init():
    pygame.init()
    screen = pygame.display.set_mode((1,1))

def get_keyboard_input(key_name):
    for _ in pygame.event.get():
        pass

    key_input = pygame.key.get_pressed()
    my_key = getattr(pygame, 'K_{}'.format(key_name))

    if key_input[my_key] is not None:
        pygame.display.update()
        return key_input[my_key]


def main():
    if get_keyboard_input('LEFT'):
        print('Left Key was pressed')
    if get_keyboard_input('RIGHT'):
        print('Right Key was pressed')
    if get_keyboard_input('UP'):
        print('Up Key was pressed')
    if get_keyboard_input('DOWN'):
        print('Down Key was pressed')


if __name__ == '__main__':
    init()

    while True:
        main()
