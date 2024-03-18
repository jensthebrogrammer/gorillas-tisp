import pygame, time

pygame.init()

def render_all(world, players, settings):
    world.screen_pygame.fill(search_for("screen_collor", "settings_V2.txt"))
    text(players, world.screen_pygame, world.screen.breedte)  # zet de namen van de spelers op het scherm
    render_buildings(world.buildings, world.screen_pygame)  # zet alle buildings op het scherm
    world.screen_pygame.blit(world.gorilla1.surf, world.gorilla1.pygamer("rect")) # gorilla 1
    world.screen_pygame.blit(world.gorilla2.surf, world.gorilla2.pygamer("rect"))
    world.screen_pygame.blit(world.clouds.surf, world.clouds.rect)
    display_grav(world)
    display_lives(world, 1, world.gorilla1.lives)
    display_lives(world, 2, world.gorilla2.lives)


def render_buildings(buildings, screen):
    for i in range(buildings.n_buildings):
        screen.blit(buildings.pygamer("surface", i + 1), buildings.pygamer("rect", i + 1))


def winner(world, hit):
    location = (world.screen.breedte//2, world.screen.hoogte//2)
    clock = pygame.time.Clock()     # om de framerate in te stellen

    if hit == "p2":
        text = "speler1 is gewonnen!!!"
    elif hit == "p1":
        text = "speler2 is gewonnen!!!"
    for i in range(10):
        if i%2 == 0:
            for j in range(100):
                world.screen_pygame.fill('Black')
                blit_text(world, text, location, "White")

                pygame.display.update()  # om je scherm te updaten
                clock.tick(60)  # fps
        else:
            for j in range(40):
                world.screen_pygame.fill('Black')
                pygame.display.update()  # om je scherm te updaten
                clock.tick(60)  # fps


def players(world):      # vraagt gwn de spelers
    clock = pygame.time.Clock()     # om de framerate in te stellen
    location_text1 = (world.screen.breedte//2, world.screen.hoogte//2)
    location_text2 = (world.screen.breedte//2, world.screen.hoogte//2)
    location_names = (world.screen.breedte//2 + 100, world.screen.hoogte//2)
    contin = False
    contin2 = False
    while contin2 == False:
        for event in pygame.event.get():    # om je spel stop te kunnen zetten
            if event.type == pygame.QUIT:
                pygame.quit()   # om pygame te deactiveren
                quit()      # om je programma stop te zetten
        
        world.screen_pygame.fill('Black')

        if contin == False:
            blit_text(world, "player1? : ", location_text1, "White")
            info = get_letters(location_names, world.screen_pygame)
            contin, name1 = info[0], info[1]
        elif contin == True:
            blit_text(world, "player2? : ", location_text2, "White")
            info = get_letters(location_names, world.screen_pygame)
            contin2, name2 = info[0], info[1]
        

        pygame.display.update()  # om je scherm te updaten
        clock.tick(60)  # fps
    
    return [name1, name2]


def blit_text(world, text, location, collor):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text_ = font.render(text, True, collor)
    textrect = text_.get_rect(center=location)

    world.screen_pygame.blit(text_, textrect)


def text(players, screen, breedte):     # zet de namen van de spelers op het scherm
    font1 = pygame.font.Font('freesansbold.ttf', 20)
    text1 = font1.render(players[0], True, "Red")
    textrect1 = text1.get_rect(topleft=(10, 10))

    font2 = pygame.font.Font('freesansbold.ttf', 20)
    text2 = font2.render(players[1], True, "Red")
    textrect2 = text2.get_rect(topright=(breedte-30, 10))

    screen.blit(text1, textrect1)
    screen.blit(text2, textrect2)


def search_for(zoek, file):     # kan dingen zoeken in een bestand
    bestand = open(file, "r")

    for line in bestand:     # zolang de inhoud niet leeg is
        temp = line.rstrip("\n")
        if temp == zoek:                  # als de inhoud is wat je zoekt
            antwoord = bestand.readline().rstrip("\n")  # pakt de info op de volgende lijn
            return antwoord

    return None

    bestand.close()  # sluit het bestand terug



stringer = ""   # voor de get_letters functie
def get_letters(location, screen):
    global stringer
    contin = False
    new = ""
    for i in range(20): # om langer te blijven zoeken naar keyboard inputs
        time.sleep(0.01)    # om er voor te zorgen dat we niet te snel gaan (dit zorgt wel dat je de window niet kan sluiten)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in range(63, 91) or event.key in range(95, 123):
                    letter = chr(event.key)
                    stringer += letter

                elif event.key in range(48, 58):
                    letter = chr(event.key)
                    stringer += letter
                
                elif event.key == pygame.K_SPACE:
                    contin = True
                    new = stringer
                    stringer = ""

                elif event.key == pygame.K_DELETE:
                    stringer = ""


    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render(stringer, True, "Red")
    textrect1 = text.get_rect(center=location)       # maten kloppen nog niet
    screen.blit(text, textrect1)

    return [contin, new]


def PL_ask_speed(world, player):
    if player == 1:
        location = (60, 40)
    else:
        location = (world.screen.breedte-90, 45)

    blit_text(world, "give speed: ", location, "red")


def blit_projectile(world, surf, rect, cords):
    render_all(world, ["", ""], world.gravity)
    world.screen_pygame.blit(surf, rect)        # blit de banaan


def PL_ask_angle(world, player):
    if player == 1:
        location = (60, 40)
    else:
        location = (world.screen.breedte-90, 45)

    blit_text(world, "give angle: ", location, "red")


def display_grav(world):
    g_message = "g : " + str(world.gravity)
    location = (world.screen.breedte//2, 15)
    blit_text(world, g_message, location, "Red")


def display_lives(world, gorilla, lives):
    if gorilla == 1:
        location = (140, 20)
    else:
        location = (world.screen.breedte - 150, 20)

    message_lives = "L : " + str(lives)
    blit_text(world, message_lives, location, "Red")