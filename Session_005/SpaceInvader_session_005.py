# Editeur de Sprite :: https://www.piskelapp.com/

import pygame
import random

noir = ((0,0,0))
blanc = (255,255,255)
vert = (0 , 255, 0)
rouge = (255,0,0)


# configuration de Base pour le moteur pyGame
pygame.init()
fenetre = pygame.display.set_mode((750,750))
pygame.display.set_caption('Sp@c3 1nv@d3r5')

imageFond = pygame.image.load('Fond.png')



# Sprite du Joueur

class Vaisseau(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([50,25])
        self.image = pygame.image.load('Vaisseau.png')
        #self.image.fill(vert)
        self.rect = self.image.get_rect()  #rectangle de colision
        self.vie = 5 # nombre de vie

    def draw(self):

        fenetre.blit(self.image, (self.rect.x, self.rect.y))


# Sprite des Aliens

class Alien(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([25,25])
        self.image = pygame.image.load('Alien.png')
        #self.image.fill(blanc)
        self.rect = self.image.get_rect()  #rectangle de colision
        self.group_rect = pygame.Rect(130,75,500,250)
        self.direction = 5

    def update(self):
        self.rect.x += self.direction
        self.group_rect.x += self.direction
        if self.group_rect.x + 500 >= 752:
            self.direction = -self.direction
        if self.group_rect.x <= 25:
            self.direction = -self.direction
            self.rect.y += 5 #descend



# Sprite des Bukers

class Bunker(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([8,8])
        self.image =  pygame.image.load('Bunker.png')
        #self.image.fill(vert)
        self.rect = self.image.get_rect()  #rectangle de colision


# Sprite des missiles

class Missile(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([5,10])
        self.image =  pygame.image.load('Missile.png')
        #self.image.fill(vert)
        self.rect = self.image.get_rect()  #rectangle de colision

    def update(self):
        self.rect.y += -10

# Sprite des bombes

class Bombe(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([5,10])
        self.image =  pygame.image.load('Bombe.png')
        #self.image.fill(rouge)
        self.rect = self.image.get_rect()  #rectangle de colision

    def update(self):
        self.rect.y += 10



# Création des Sprite

mon_vaisseau = Vaisseau()
mon_vaisseau.rect.x = 375
mon_vaisseau.rect.y = 650


liste_aliens = pygame.sprite.Group();

# Création du tableau d'aliens
for ligne in range(1,6):
    for colonne in range (1,11):
        un_alien = Alien()
        un_alien.rect.x = 80 + (50 * colonne)
        un_alien.rect.y = 25 + (50 * ligne)
        liste_aliens.add(un_alien)


# Création du tableau des bunkers

liste_bunker = pygame.sprite.Group();

for n in range (3):
    for ligne in range (5):
        for colonne in range(10):
            un_bunker =  Bunker()
            un_bunker.rect.x = ( 50 + (275* n)) + (10 * colonne)
            un_bunker.rect.y = ( 500 + (10 * ligne))
            liste_bunker.add(un_bunker)


# Création des listes pour les missiles et bombe
liste_missiles = pygame.sprite.Group();
liste_bombes = pygame.sprite.Group();





def redessine():

    fenetre.blit(imageFond, (0,0))
    #fenetre.fill(noir)


    bas = pygame.draw.rect(fenetre, vert, (50,700,650,15))

    for i in range(mon_vaisseau.vie):
        pygame.draw.rect(fenetre, rouge, (50 + (i * 130), 715,130,15))

    font = pygame.font.SysFont('Courrier',30);
    text = font.render('Py 1nv@d3r5', False, blanc)
    textRect = text.get_rect()
    textRect.center = (750//2, 25)
    fenetre.blit(text, textRect)

    mon_vaisseau.draw()

    liste_aliens.update()
    liste_aliens.draw(fenetre)


    liste_bunker.draw(fenetre)

    # mise à jour de la postion des missiles dans la liste
    liste_missiles.update()

    # dessine les missiles
    liste_missiles.draw(fenetre)

    # mise à jour de la postion des bombes dans la liste
    liste_bombes.update()

    # dessine les bombe
    liste_bombes.draw(fenetre)


    pygame.display.update();



run = True

while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
        mon_vaisseau.rect.x  += -10
    if key[pygame.K_RIGHT]:
        mon_vaisseau.rect.x  += 10
    if key[pygame.K_SPACE]:
        if len(liste_missiles) < 10:
            un_missile = Missile()
            un_missile.rect.x = mon_vaisseau.rect.x + 25  # C'est le milieu du vaisseau
            un_missile.rect.y = mon_vaisseau.rect.y
            liste_missiles.add(un_missile)



    # Calcul des chances de lancer une bombe
    shoot_chance =  random.randint(1,100)

    if shoot_chance < 25:
        if len(liste_aliens) > 0:
            un_alien_au_pif = random.choice(liste_aliens.sprites())
            une_bombe = Bombe()
            une_bombe.rect.x = un_alien_au_pif.rect.x +12 # milieu
            une_bombe.rect.y = un_alien_au_pif.rect.y +25 # bas de l'alien

            liste_bombes.add(une_bombe)


    # Vérification les missiles touchent quelque chose
    for un_missile in liste_missiles:

        if un_missile.rect.y < -10:
            liste_missiles.remove(un_missile)

        # Vérification des aliens touché
        for un_alien in liste_aliens:
            if un_missile.rect.colliderect(un_alien.rect):
                liste_missiles.remove(un_missile)
                liste_aliens.remove(un_alien)

        # Vérification si des bunkers sont touchés
        for un_bunker in liste_bunker:
            if un_missile.rect.colliderect(un_bunker.rect):
                liste_missiles.remove(un_missile)
                liste_bunker.remove(un_bunker)

    # Vérification si les bombes touchent quelque chose
    for une_bombe in liste_bombes:

        # Vérification si le vaisseau a été touché
        if une_bombe.rect.colliderect(mon_vaisseau.rect):
            liste_bombes.remove(une_bombe)
            mon_vaisseau.vie -= 1


        # Vérification si des bunkers sont touchés
        for un_bunker in liste_bunker:
            if une_bombe.rect.colliderect(un_bunker.rect):
                liste_bombes.remove(une_bombe)
                liste_bunker.remove(un_bunker)

    # Si je n'ai plus de vie alors fin de la partie
    if mon_vaisseau.vie < 0 or len (liste_aliens) == 0:
        run = False

    redessine()

pygame.quit()