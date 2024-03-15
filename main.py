from BLL import *
import pygame, math
pygame.init()  # om pygame te activeren


def main():
    settings_file = "settings_V2.txt"   # van dit bestand haal ik al mijn info
    banaan_image_file = "banaan_transparant.png"        # (488, 250)
    gorilla_image_file = "donkey_kong_transparant.png"  # (488, 327)
    clouds_image_file = "wolken_transparant.png"

    # setup
    turn = 1
    gravity = 9.81
    a_angle, a_speed, trow = True, False, False

    # alle lichamen maken
    screen = body("screen")
    screen.get_info_from(settings_file)
    screen_pygame = pygame.display.set_mode((screen.breedte, screen.hoogte))    # de grote van je window(breedte, hoogte)
    screen_pygame.fill(screen.collor)       # geeft het scherm een kleur

    banana = body("banana")
    banana.get_info_from(settings_file)
    banana.image(banaan_image_file, settings_file)

    gorilla2 = body("gorilla2")
    gorilla2.get_info_from(settings_file)
    gorilla2.image(gorilla_image_file, settings_file)

    gorilla1 = body("gorilla1")
    gorilla1.get_info_from(settings_file)
    gorilla1.image(gorilla_image_file, settings_file)

    clouds = body("clouds")
    clouds.x_cor, clouds.y_cor = screen.breedte//2, screen.hoogte//2
    clouds.image(clouds_image_file, settings_file)

    buildings = city()
    size = int(search_for("building_size", settings_file))  # berekent hoeveel gebouwen er gemaakt moeten worden
    buildings.make_buildings(size, screen)

    # de lichamen opslagen in een classe
    world = map(gorilla1, gorilla2, banana, screen, screen_pygame
                , buildings, clouds, gravity)

    gorilla1.get_random_x(screen, 1, settings_file)     # bepaalt en random x waarde
    gorilla2.get_random_x(screen, 2, settings_file)
    gorilla1.latch(world)   # berekent de hoogte van de gorilla op het gebouw
    gorilla2.latch(world)  # berekent de hoogte van de gorilla op het gebouw

    gorilla1.make_hitbox(settings_file)
    gorilla2.make_hitbox(settings_file)
    banana.make_hitbox(settings_file)

    pygame.display.set_caption('gorillas')  # de naam van je game
    clock = pygame.time.Clock()     # om de framerate in te stellen

    players_ = players(world)

    while True:     # game loop
        for event in pygame.event.get():    # om je spel stop te kunnen zetten
            if event.type == pygame.QUIT:
                pygame.quit()   # om pygame te deactiveren
                quit()      # om je programma stop te zetten

        screen_pygame.fill(search_for("screen_collor", settings_file))  # om het scherm te updaten
        render_all(world, players_, settings_file)     # zet alles op het scherm

        if a_angle == True:     # ik gebruik booleans om te weten wat wanneer moet gebeuren
            info = ask_angle(world, turn)   # neemt keyboard inputs
            a_speed, angle = info[0], info[1]       # info[0] is een string

            # input validatie
            if a_speed == True and int(angle) < 15:
                a_speed, angle = False, 0

        if a_speed == True:
            info = ask_speed(world, turn)
            trow, speed = info[0], info[1]
            a_angle = False
            

        if trow == True:
            trow_(world, turn, int(speed), int(angle))
            a_angle, a_speed, trow = True, False, False     # reset
            turn = turn % 2 + 1  # reset

        pygame.display.update()  # om je scherm te updaten
        clock.tick(60)  # fps


main()
