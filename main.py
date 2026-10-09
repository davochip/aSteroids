import sys

import pygame

from asteroid_class import Asteroid
from asteroidfield import AsteroidField
from character import Player
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, drawable, updatable)

    field = AsteroidField()
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 0)

    while True:
        log_state()

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        updatable.update(dt)

        for object in asteroids:
            if player.collides_with(object):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

            for blast in shots:
                if blast.collides_with(object):
                    log_event("asteroid_shot")
                    blast.kill()
                    object.split()

        for drawing in drawable:
            drawing.draw(screen)

        pygame.display.flip()



if __name__ == "__main__":
    main()
