import pygame

import Application

def main():
    pygame.init()

    apka = Application.App(900,600)
    apka.run()

if __name__ == '__main__':
    main()