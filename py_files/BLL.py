print("gorillas module geactiveert")
import pygame, random, time, math
from py_files.presentation_layer import *
pygame.init() # om pygame te activeren

def make_file(file_name):
    text = ""   # dit is de text die ik wil toevoegen
    bestand = open(file_name, "w") # maakt een file aan
    bestand.write(text) # zet de text in het bestand
    bestand.close() # sluit het bestand terug


def search_for(zoek, file):     # kan dingen zoeken in een bestand
    bestand = open(file, "r")

    for line in bestand:     # zolang de inhoud niet leeg is
        temp = line.rstrip("\n")
        if temp == zoek:                  # als de inhoud is wat je zoekt
            antwoord = bestand.readline().rstrip("\n")  # pakt de info op de volgende lijn
            return antwoord

    return None

    bestand.close()  # sluit het bestand terug


class body:                     # lichamen in pygame zoals de gorillas
    def __init__(self, name):
        self.name = name

    def get_info_from(self, file):                  # haalt alle info uit de file
        bestand = open(file, "r")  # leest de file

        self.hoogte = int(search_for(self.name + "_hoogte", file))
        self.breedte = int(search_for(self.name + "_breedte", file))
        self.x_cor = search_for(self.name + "_x_cor", file)
        self.y_cor = search_for(self.name + "_y_cor", file)
        self.collor = search_for(self.name + "_collor", file)

        lives = search_for(self.name + "_lives", file)
        if lives != None:
            self.lives = int(lives)

        bestand.close()  # sluit het bestand terug

    def pygamer(self, asked):       # maakt een surface of een rect van je lichaam
        if asked == "surface":
            body_surface = pygame.Surface((int(self.breedte), int(self.hoogte)))
            body_surface.fill(self.collor)
            return body_surface
        elif asked == "rect":
            body_surface = pygame.Surface((int(self.breedte), int(self.hoogte)))
            body_rect = body_surface.get_rect(midbottom = (int(self.x_cor), int(self.y_cor)))
            return body_rect

    def get_random_x(self, screen, helft, file):
        apart = search_for("apart_from_eachother", file)    # hoever de gorillas van elkaar moeten staan
        a = int(apart) // 2
        b = int(screen.breedte) // 2

        if helft == 1:
            self.x_cor = random.randint(0, b - a)     # bepaalt een random x coördinaat in de eerste helft
        elif helft == 2:
            self.x_cor = random.randint(b, b*2)

    def latch(self, world):
        a = int(self.x_cor)

        for j in range(world.buildings.n_buildings):
            if a < (j * 100 + 92) and a > ((j - 1) * 100 + 92):
                latch_h = int(world.screen.hoogte) - world.buildings.pygamer("hoogte", j + 1)  # hoogte van het scherm - de hoogte van het gebouw

                self.y_cor = latch_h


    def image(self, image_file, file):
        ori_image = pygame.image.load(image_file).convert_alpha()
        size_factor = int(search_for(self.name + "_size_factor", file))*0.1
        
        act_image = pygame.transform.scale_by(ori_image, size_factor)
        rect_image = act_image.get_rect(center=(int(self.x_cor), int(self.y_cor)))

        self.hoogte = act_image.get_height()
        self.breedte = act_image.get_width()
        self.surf = act_image
        self.rect = rect_image

    def make_hitbox(self, file):
        hitbox_sizefactor = int(search_for(self.name + "_hitbox_size_factor", file))*0.01

        hoogte = 10
        breedte = 10

        surface = pygame.Surface((breedte, hoogte))
        self.hitbox_surf = pygame.transform.scale_by(surface, hitbox_sizefactor)
        self.hitbox_rect = self.hitbox_surf.get_rect(midbottom=(int(self.x_cor), int(self.y_cor)))



class city:
    def make_buildings(self, size, screen):
        self.n_buildings = int(int(screen.breedte) / size)
        self.surf_buildings = [0] * self.n_buildings
        self.rect_buildings = [0] * self.n_buildings
        self.h_buildings = [0] * self.n_buildings
        self.collor = search_for("building_collor", "settings_V2.txt")

        for i in range(self.n_buildings):
            hoogte_building = random.randint(15, int(search_for("building_max_h", "settings_V2.txt")))
            self.h_buildings[i] = hoogte_building

            building_ = pygame.Surface((size, hoogte_building)) # random hoogte
            building_.fill(self.collor)
            self.surf_buildings[i] = building_

            self.rect_buildings[i] = building_.get_rect(bottomleft=(i * size, int(screen.hoogte)))     # maakt een hitbox voor de buildings

        #return [self.surf_buildings, self.rect_buildings, self.h_buildings]

    def pygamer(self, asked, number):
        if asked == "surface":
            return self.surf_buildings[number - 1]
        elif asked == "rect":
            return self.rect_buildings[number - 1]
        elif asked == "hoogte":
            return self.h_buildings[number - 1]


class map:      # een classe om al je lichamen bij te houden
    def __init__(self, gorilla1, gorilla2, banana, screen, 
                 screen_pygame, buildings, clouds, gravity):
        self.gorilla1 = gorilla1
        self.gorilla2 = gorilla2
        self.banana = banana
        self.screen = screen
        self.screen_pygame = screen_pygame
        self.buildings = buildings
        self.clouds = clouds
        self.gravity = gravity


def ask_angle(world, player):
    PL_ask_angle(world, player)
    
    if player == 1:     # zet een tekstje op het scherm om de snelheid te vragen
        info = get_letters((150, 43), world)
        contin, letters = info[0], info[1]

    elif player == 2:
        info = get_letters((world.screen.breedte - 17, 43), world)
        contin, letters = info[0], info[1]

    return [contin, letters]


def ask_speed(world, player):
    PL_ask_speed(world, player)

    if player == 1:
        info = get_letters((150, 43), world)
        contin, letters = info[0], info[1]

    elif player == 2:
        info = get_letters((world.screen.breedte - 17, 43), world)
        contin, letters = info[0], info[1]

    return [contin, letters]


stringer = ""   # voor de get_letters functie
def get_letters(location, world):
    global stringer
    contin = False
    new = ""
    for i in range(10): # om langer te blijven zoeken naar keyboard inputs
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

    blit_text(world, stringer, location, "red")

    return [contin, new]
    

def trow_(world, turn, speed, alpha):
    t = 0       # t is de tijd

    if turn == 1:       # variabelen aan de hand van wie er aan de beurd is
        expected_colision = "p2"        # wie verwacht ik dat er geraakt word
        x_gor = world.gorilla1.x_cor
        y_gor = world.gorilla1.y_cor
        alpha = alpha * (math.pi / 180)     # zet alpha om naar radialen
    elif turn == 2:
        alpha = 180 - alpha     # gooit de andere richting uit
        alpha = alpha * (math.pi / 180)
        expected_colision = "p1"
        x_gor = world.gorilla2.x_cor
        y_gor = world.gorilla2.y_cor

    y = (speed * math.sin(alpha) * t - 1 / 2 * world.gravity * t ** 2)       # berekent y één keer voor de while loop te starten

    while y >= -50:     # -50 omdat dat de max hoogte van de gebouwen is
        time.sleep(0)
        x = x_gor + (speed * math.cos(alpha) * t)
        y = (speed * math.sin(alpha) * t - 1 / 2 * world.gravity * t ** 2)
        x = round(x)
        y = round(y)
        t += 0.1        # de tijd gaat vooruit

        hoogte = world.screen.hoogte        # hoogte van het scherm
        y_ = hoogte - y - (hoogte - y_gor)      # omgevormde y voor het coördinaten systeem
        surface = world.banana.surf
        cords = (x, y_)
        rectangle = surface.get_rect(center=cords)    # hitbox van de banaan

        temp_surf = world.banana.hitbox_surf
        world.banana.hitbox_rect = world.banana.hitbox_surf.get_rect(center=cords)
        temp_rect = world.banana.hitbox_rect

        blit_projectile(world, surface, rectangle, cords)

        pygame.display.update()  # om je scherm te updaten
        clock = pygame.time.Clock()  # om de framerate in te stellen
        clock.tick(60)  # fps

        if world.banana.hitbox_rect.colliderect(world.gorilla1.hitbox_rect) == 1:
            colision = "p1"

        elif world.banana.hitbox_rect.colliderect(world.gorilla2.hitbox_rect) == 1:
            colision = "p2"
        else:
            colision = ""       # als er niks is

        if expected_colision == colision:       # dit word gedaan omdat je anders jezelf kan raken
            if colision == "p2":
                world.gorilla2.lives -= 1
            elif colision == "p1":
                world.gorilla1.lives -= 1
            
            y = -51 # om de while loop te stoppen
            world.gravity = random.randint(2, 20)

            if ((world.gorilla1.lives == 0) or
                (world.gorilla2.lives == 0)):
                winner(world, colision)
                pygame.quit()  # om pygame te deactiveren
                quit()  # om je programma stop te zetten                 
