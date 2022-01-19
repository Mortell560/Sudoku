
############################################
#     Lycée Camille Claudel - Palaiseau
#
#                Spécialité
#     Numérique et Science informatique
#           Première et Terminale
#
#   Thomas RAVARY
#   version de janvier 2019
#
#   SOMMAIRE
#
#   1. Types, Variables, Constantes.....35
#   2. Affichage........................87
#   3. Dessin d'objets.................132
#   4. Gestion d'images................247
#   5. Ecriture de texte...............290
#   6. Gestion d'événements............312
#   7. Gestion du temps................417
#   8. Valeurs aléatoires..............471
#   9. Initialisation de tableaux......483
#   10. Divers.........................495
#
#   ANNEXE : Fonctions de tests........509
#            Main......................680
#
#############################################

import math
import pygame
from pygame.locals import *
import random
random.seed()

#################################
# 1. Types, Variables, Constantes
#################################

""" Type Point """
""" Toute fonction de la bibliothèque peut utiliser des points sous forme d'un tuple (x,y) ou d'un objet de type Point """

class Point:
    __slots__ =('x','y')
    def __init__(self,x = 0,y = 0):
        self.x,self.y = x,y

""" Constantes de couleur """
noir = pygame.Color('black')
blanc = pygame.Color('white')
bleu = pygame.Color('blue')
rouge = pygame.Color('red')
jaune = pygame.Color('yellow')
vert = pygame.Color('green')
rose = pygame.Color('pink')
orange = pygame.Color('orange')
violet = pygame.Color('purple')
cyan = pygame.Color('cyan')

""" Constantes booléennes """
TRUE = True
true = True
FALSE = False
false = False

""" Taille de l'affichage """
__L, __H = 0,0

""" Ecran d'affichage """
__screen = None

""" Si __AFFICHE_AUTO vaut 1, l'affichage est automatiquement fait pour chaque objet
    Sinon, il faut le faire à la main à l'aide de la fonction affiche_all()
"""
__AFFICHE_AUTO = 1

""" Lorsqu'une touche reste enfoncée, la touche va générer en continue des événements KEYDOWN.
    __REPEAT_DELAY est le nombre de milliseconds avant la première répétition
    __REPEAT_INTERVAL est le nombre de milliseconds entre deux répétitions """
__REPEAT_DELAY = 20
__REPEAT_INTERVAL = 20

""" A modifier selon le type de clavier "azerty" ou "qwerty" """
__CLAVIER = "azerty"

""" Police par défaut """
__POLICE_NAME = "monospace"
__POLICE_SIZE = 15

""" Si __MODE_CLASSE_POINT vaut True alors les points renvoyés sont des classes Point
    sinon les points renvoyés sont des tuples (x,y) """
__MODE_CLASSE_POINT = False

def __get_xy(point):
    if type(point)==Point:
        return (point.x,point.y)
    else:
        return point

def __return_point(point):
    x,y=__get_xy(point)
    if __MODE_CLASSE_POINT:
        return Point(x,y)
    return (x,y)

##################
# 2. Affichage
##################

""" 2.1 Initialisation de la fenêtre dans laquelle on dessine """
def init_fenetre(largeur,hauteur,titre = "Ma fenêtre"):
    """ Lance une fenetre de dimension largeur par hauteur. Le titre est optionnel """
    global __L, __H, __screen
    __L, __H = largeur, hauteur
    pygame.init()
    pygame.display.set_caption(titre)
    __screen = pygame.display.set_mode( (__L,__H) )
    pygame.key.set_repeat(__REPEAT_DELAY,__REPEAT_INTERVAL)

    remplir_fenetre(noir)
    affiche_tout()

def affiche_auto_on():
    global __AFFICHE_AUTO
    __AFFICHE_AUTO = 1

def affiche_auto_off():
    global __AFFICHE_AUTO
    __AFFICHE_AUTO = 0

def affiche_tout():
    pygame.display.flip()

def pas_echap():
    """ renvoie vrai si l'utilisateur n'a pas demandé de quitter l'application
        sinon quitte l'application
    """
    __update_event()
    return True

def attendre_echap():
    """ Attend l'ordre de quitter l'application
        instruction bloquante
    """
    while pas_echap():
        pass

######################
# 3. Dessin d'objets
######################



def __pyPoint( point ):
    x,y=__get_xy(point)
    return (x, __H-y)

def affiche_pixel(point, couleur):
    """ affiche un pixel """
    point = __pyPoint(point)
    __screen.set_at( point, couleur)
    if __AFFICHE_AUTO:
        affiche_tout()

def affiche_ligne(point_depart, point_arrivee, couleur,epaisseur = 1):
    """ affiche un segment
        la largeur en pixel vaut 1 par défaut et est optionnelle
    """
    point_depart,point_arrivee =__pyPoint(point_depart),__pyPoint(point_arrivee)
    pygame.draw.line(__screen, couleur, point_depart, point_arrivee, epaisseur)
    if __AFFICHE_AUTO:
        affiche_tout()

def affiche_rectangle(point1,point2,couleur,epaisseur = 1):
    """ affiche un rectangle non rempli dont point1 et point2 sont des sommets non adjacents """
    x1,y1=__get_xy(point1)
    x2,y2=__get_xy(point2)
    point_left_top = (min(x1,x2), max(y1,y2))
    largeur = max(x1,x2) - min(x1,x2)
    hauteur = max(y1,y2) - min(y1,y2)
    point_left_top = __pyPoint(point_left_top)

    rectangle = pygame.Rect( point_left_top, (largeur,hauteur))
    pygame.draw.rect(__screen,couleur,rectangle,epaisseur)
    if __AFFICHE_AUTO:
        affiche_tout()

def affiche_rectangle_plein(point1,point2,couleur):
    """ affiche un rectangle plein dont point1 et point2 sont des sommets non adjacents """
    x1,y1=__get_xy(point1)
    x2,y2=__get_xy(point2)
    point_left_top = (min(x1,x2), max(y1,y2))
    largeur = max(x1,x2) - min(x1,x2)
    hauteur = max(y1,y2) - min(y1,y2)
    point_left_top = __pyPoint(point_left_top)
    rectangle = pygame.Rect( point_left_top, (largeur,hauteur))
    pygame.draw.rect(__screen,couleur,rectangle,0)
    if __AFFICHE_AUTO:
        affiche_tout()

def affiche_cercle(centre, rayon, couleur,epaisseur = 1):
    """ dessine un cercle non rempli """
    centre = __pyPoint(centre)
    pygame.draw.circle(__screen,couleur,centre,rayon,epaisseur)
    if __AFFICHE_AUTO:
        affiche_tout()

def affiche_cercle_plein(centre, rayon, couleur):
    """ dessine un cercle plein """
    centre = __pyPoint(centre)
    pygame.draw.circle(__screen,couleur,centre,rayon,0)
    if __AFFICHE_AUTO:
        affiche_tout()

def affiche_triangle(point1,point2,point3,couleur,epaisseur=1):
    """ affiche un triangle non rempli """
    point1,point2,point3 = __pyPoint(point1),__pyPoint(point2),__pyPoint(point3)
    pygame.draw.polygon(__screen,couleur,[point1,point2,point3],epaisseur)
    if __AFFICHE_AUTO:
        affiche_tout()

def affiche_triangle_plein(point1,point2,point3,couleur):
    """ affiche un triangle rempli """
    point1,point2,point3 = __pyPoint(point1),__pyPoint(point2),__pyPoint(point3)
    pygame.draw.polygon(__screen,couleur,[point1,point2,point3],0)
    if __AFFICHE_AUTO:
        affiche_tout()

def affiche_arc_cercle(centre,rayon,angle_debut,angle_fin,couleur,epaisseur=1):
    """ affiche un arc de cercle
        les angles sont en degrés de -360 à +360
    """
    x,y=__get_xy(centre)
    point_left_top = (x-rayon,y+rayon)
    point_left_top = __pyPoint(point_left_top)
    rectangle = pygame.Rect(point_left_top,(2*rayon,2*rayon))
    angle_debut = angle_debut* math.pi / 180
    angle_fin = angle_fin* math.pi / 180

    pygame.draw.arc(__screen,couleur,rectangle,angle_debut,angle_fin,epaisseur)
    if __AFFICHE_AUTO:
        affiche_tout()

def affiche_ellipse(point1,point2,couleur,epaisseur = 1):
    """ affiche une ellipse non remplie dont point1 et point2 sont des sommets non adjacents du rectangle circonscrit à l'ellipse """
    x1,y1=__get_xy(point1)
    x2,y2=__get_xy(point2)
    point_left_top = (min(x1,x2), max(y1,y2))
    point_left_top = __pyPoint(point_left_top)
    largeur = max(x1,x2) - min(x1,x2)
    hauteur = max(y1,y2) - min(y1,y2)
    rectangle = pygame.Rect( point_left_top, (largeur,hauteur))
    pygame.draw.ellipse(__screen,couleur,rectangle,epaisseur)
    if __AFFICHE_AUTO:
        affiche_tout()

def affiche_ellipse_plein(point1,point2,couleur):
    """ affiche une ellipse remplie dont point1 et point2 sont des sommets non adjacents du rectangle circonscrit à l'ellipse """
    x1,y1=__get_xy(point1)
    x2,y2=__get_xy(point2)
    point_left_top = (min(x1,x2), max(y1,y2))
    point_left_top = __pyPoint(point_left_top)
    largeur = max(x1,x2) - min(x1,x2)
    hauteur = max(y1,y2) - min(y1,y2)
    rectangle = pygame.Rect( point_left_top, (largeur,hauteur))
    pygame.draw.ellipse(__screen,couleur,rectangle,0)
    if __AFFICHE_AUTO:
        affiche_tout()

def remplir_fenetre(couleur):
    """ remplissage de toute la fenetre """
    __screen.fill(couleur)
    if __AFFICHE_AUTO:
        affiche_tout()

###########################################
# 4. Gestion d'images
###########################################

__images_original = dict()
__images = dict()
def charge_image(nom_image):
    global __images_original,__images
    """ charge une image en mémoire """
    __images_original[nom_image] = pygame.image.load(nom_image).convert()
    __images[nom_image] = __images_original[nom_image]

def affiche_image(nom_image,dest_bas_gauche, source_bas_gauche = None, source_haut_droit = None):
    """
        affiche une image.
        nom_image est le nom du fichier image (appartenant au même dossier que le code source executé).
        dest_bas_gauche correspond au point bas gauche dans la fenetre où on veut afficher l'image
        source_bas_gauche et source_haut_droit correspondent aux coins du rectangle dans l'image
        à afficher(pour afficher un morceau seulement).
        Ces deux derniers paramètres sont optionnels, par défaut toute l'image est affichée
    """
    if not(nom_image in __images):
        charge_image(nom_image)
    image = __images[nom_image]
    hauteur = image.get_height()

    area = None
    if source_bas_gauche and source_haut_droit:
        xbg,ybg=__get_xy(source_bas_gauche)
        xhd,yhd=__get_xy(source_haut_droit)
        source_haut_gauche = (xbg,image.get_height()-yhd)
        hauteur = yhd-ybg
        area = pygame.Rect(source_haut_gauche,(xhd-xbg,hauteur))
    xbg_d,ybg_d=__get_xy(dest_bas_gauche)
    dest_haut_gauche = __pyPoint((xbg_d,ybg_d+hauteur))

    __screen.blit(image,dest_haut_gauche,area)
    if __AFFICHE_AUTO:
        affiche_tout()

def modifie_taille_image(nom_image,nouvelle_largeur,nouvelle_hauteur):
    """ change la taille d'une image (avant de l'afficher)"""
    if not(nom_image in __images):
        charge_image(nom_image)
    __images[nom_image] = pygame.transform.scale(__images_original[nom_image],(nouvelle_largeur,nouvelle_hauteur))

########################################
# 6. Ecriture de texte
########################################

def largeur_texte(texte,taille_police = 15,police = "mono"):
    """ renvoie la largeur du texte à afficher en pixel """
    myfont = pygame.font.SysFont(police, taille_police)
    return myfont.size(texte)[0]

def hauteur_texte(texte,taille_police = 15,police = "mono"):
    """ renvoie la hauteur du texte à afficher en pixel """
    myfont = pygame.font.SysFont(police, taille_police)
    return myfont.size(texte)[1]

def affiche_texte(texte,position,couleur,taille_police = __POLICE_SIZE,police = __POLICE_NAME):
    """ affiche un texte, position correspond au point bas gauche du plus petit rectangle dans lequel le texte est inclus """
    myfont = pygame.font.SysFont(police, taille_police)
    label = myfont.render(texte, 1, couleur)
    x,y=__get_xy(position)
    position = (x,y+myfont.size(texte)[1])
    position = __pyPoint(position)
    __screen.blit(label, position)

##########################################
# 6. Gestion d'événements
#########################################

__MOUSE_LEFT = 1
__MOUSE_MIDDLE = 2
__MOUSE_RIGHT = 3
def wait_clic():
    """ Attend que l'utilisateur clique avec le bouton gauche de la souris
        et renvoie les coordonnées du point cliqué sous la forme d'un Point
        fonction bloquante
    """
    global __is_clic
    __is_clic=False
    while 1:
        __update_event()
        clic=last_clic()
        if clic:
            return clic

def last_clic():
    """ si le bouton gauche de la souris a été relaché depuis le dernier appel à last_clic(),
        renvoie un point contenant la position de la souris au moment où le bouton gauche à été enfoncé pour la dernière fois
        sinon renvoie None
        instruction non bloquante
        A utiliser avec précaution :
            - le dernier clic effectué peut être "vieux", il peut être judicieux de faire un appel préventif à
                last_clic pour vider les anciens clics
            - ne pas utiliser en même temps que pas_echap ou get_fleches
    """
    global __is_clic,__last_clic
    __update_event()
    if __is_clic:
        __is_clic=False
        return __return_point((__last_clic.x,__H - __last_clic.y))
    else:
        return None

__arrow=Point(0,0)
__is_clic=False
__last_clic=Point(0,0)
def __update_event():
    global __arrow,__is_clic,__last_clic
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            exit()
        if event.type == KEYDOWN and event.key == K_LEFT:
            __arrow.x -= 1
        if event.type == KEYDOWN and event.key == K_RIGHT:
            __arrow.x += 1
        if event.type == KEYDOWN and event.key == K_DOWN:
            __arrow.y -=1
        if event.type == KEYDOWN and event.key == K_UP:
            __arrow.y += 1
        if event.type == MOUSEBUTTONDOWN and event.button == __MOUSE_LEFT:
           __last_clic.x,__last_clic.y = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONUP and event.button == __MOUSE_LEFT:
            __is_clic = True
            __last_clic.x,__last_clic.y = pygame.mouse.get_pos()

def get_fleches():
    """
        renvoie un Point p contenant
            en abscisse le nombre d'appui sur les fleches gauche et droite (-1 par appui sur la fleche gauche, +1 sur la
                            fleche droite)
            en ordonnée le nombre d'appui sur les fleches bas et haut (-1 par appui sur la fleche bas, +1 sur la fleche haut)
        fonction non bloquante
    """
    global __arrow
    __update_event()
    arrow=Point(__arrow.x,__arrow.y)
    __arrow=Point(0,0)
    return __return_point(arrow)

__table_touche = dict()
def __init_table_touche():
    #recuperation de la table qwerty
    for val in dir(pygame):
        if val[0:2] == 'K_':
            __table_touche[val] = getattr(pygame,val)

    #modification de la table dans le cas d'un clavier azerty
    if __CLAVIER == "azerty":
        __table_touche['K_a'] = pygame.K_q
        __table_touche['K_z'] = pygame.K_w
        __table_touche['K_q'] = pygame.K_a
        __table_touche['K_m'] = pygame.K_SEMICOLON
        __table_touche['K_w'] = pygame.K_z
        __table_touche['K_COMMA'] = pygame.K_m
        __table_touche['K_SEMICOLON'] = pygame.K_COMMA
__init_table_touche()

def touche_enfoncee(touche):
    """
        renvoie True si la touche est enfoncée, False sinon
        touche est une chaine de caractère :
            les lettres ou chiffres : 'K_a', 'K_b', etc et 'K_1','K_2', etc
            les fleches : 'K_LEFT', 'K_RIGHT', 'K_DOWN', 'K_UP'
            la touche espace : 'K_SPACE'
            les touches control : 'K_LCTRL' (gauche) et 'K_RCTRL' (droit)
            les touches maj : 'K_LSHIFT' et 'K_RSHIFT'
            les touches alt : 'K_LALT' et 'K_RALT'
            la touche entrée : 'K_RETURN'
            la touche Retour arrière : 'K_BACKSPACE'
            le pavé numérique 'K_KP0', 'K_KP1', etc et 'K_KP_ENTER' (entree), 'K_KP_PLUS',
            'K_KP_MINUS', 'K_KP_MULTIPLY', 'K_KP_DIVIDE' (opérations) et 'K_KP_PERIOD' (point)
    """
    return pygame.key.get_pressed()[__table_touche[touche]]

#########################################
# 7. Gestion du temps
#########################################

__CHRONOS = dict()
class Chrono:
    def __init__(self):
        self.debut = pygame.time.get_ticks()
        self.temps = 0
        self.en_cours = True

    def init(self):
        Chrono.__init__(self)

    def lancer(self):
        self.debut = pygame.time.get_ticks()
        self.en_cours = True

    def stop(self):
        self.temps += (pygame.time.get_ticks()-self.debut)
        self.en_cours = False

    def lire(self):
        if self.en_cours:
            return self.temps + (pygame.time.get_ticks()-self.debut)
        else:
            return self.temps

def init_chrono(chrono = "default"):
    """ remet le chronometre à 0 et le lance """
    if not(chrono in __CHRONOS):
        __CHRONOS[chrono] = Chrono()
    __CHRONOS[chrono].init()

def lance_chrono(chrono = "default"):
    """ lance le chronometre (sans le remettre a 0) """
    if not(chrono in __CHRONOS):
        __CHRONOS[chrono] = Chrono()
    __CHRONOS[chrono].lancer()

def stop_chrono(chrono = "default"):
    if not(chrono in __CHRONOS):
        __CHRONOS[chrono] = Chrono()
    __CHRONOS[chrono].stop()

def lire_chrono(chrono = "default"):
    if not(chrono in __CHRONOS):
        __CHRONOS[chrono] = Chrono()
    return __CHRONOS[chrono].lire()

def attendre(temps):
    """ attendre temps milliseconds """
    pygame.time.wait(temps)

#########################################
# 8. Valeurs aleatoires
#########################################

def alea_int(a,b):
    """ renvoie un entier aleatoire entre a et b inclus """
    return random.randint(a,b)

def alea_float():
    """ renvoie un float aleatoire compris entre 0 (inclus) et 1 (exclus) """
    return random.random()

#########################################
# 9. Initialisation de tableaux (listes)
#########################################

def init_tableau(nb_cases,valeur):
    """ renvoie un tableau (une liste) d'indices de 0 à nb_cases - 1 rempli avec valeur (non mutable) """
    if not(type(valeur) in (type(None),str,int,float,complex,bool,tuple,bytes,frozenset,range)):
        print("Warning : init_tableau : valeur de type {type(valeur)}, valeur doit être de type non mutable")
    return [valeur for i in range(nb_cases)]

def init_tableau_2D(nb_cases_x, nb_cases_y,valeur):
    """ renvoie un tableau (une liste) à deux dimensions de nb_cases_x * nb_cases_y cases rempli avec valeur (non mutable) """
    if not(type(valeur) in (type(None),str,int,float,complex,bool,tuple,bytes,frozenset,range)):
        print("Warning : init_tableau : valeur de type {type(valeur)}, valeur doit être de type non mutable")
    return [ [valeur] * nb_cases_y for i in range(nb_cases_x)]

#########################################
# 10. Divers
#########################################

def couleur(r,g,b,a = 255):
    """ renvoie une couleur à partir de ses cactéristiques RGB, a étant la transparence
        pour obtenir les caractéristiques RGB d'une couleur, voir : https://htmlcolorcodes.com/fr/
    """
    return pygame.Color(r,g,b,a)

def distance(p1,p2):
    """ renvoie la distance entre les points p1 et p2 """
    x1,y1=__get_xy(p1)
    x2,y2=__get_xy(p2)
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )

###################################################
# Annexe : Fonctions de tests de la bibliothèque
###################################################
def test_dessin():
    init_fenetre(800,600,"Test dessin")
    remplir_fenetre(blanc)
    A = Point(10,50)
    B = Point(70,20)
    affiche_ligne(A,B,rouge)
    affiche_cercle(A,30,bleu)
    C = Point(200,300)
    D = Point(500,400)
    affiche_rectangle_plein(C,D,vert)
    affiche_rectangle(C,D,bleu)
    E = Point(600,550)
    F = Point(600,500)
    affiche_triangle(D,E,F,cyan,14)
    G = Point(350,350)
    affiche_pixel(G,rouge)
    H = Point(400,50)
    affiche_cercle_plein(H,40,rouge)
    I = Point(320,40)
    J = Point(320,60)
    affiche_triangle_plein(I,J,H,vert)
    affiche_arc_cercle(C,70,-160,120,noir,10)
    K = Point(100,400)
    L = Point(600,600)
    affiche_ellipse(K,L,orange,10)

    M = Point(150,450)
    N = Point(550,550)
    affiche_ellipse_plein(M,N,violet)

    attendre_echap()

def test_image():
    L = 1000
    H = 800
    init_fenetre(L,H,"Test dessin")
    affiche_auto_off()
    charge_image("elsa.bmp")
    modifie_taille_image("elsa.bmp",L,H)

    p1 = Point(200,100)
    p2 = Point(500,320)
    v = Point(3,2)
    clock = pygame.time.Clock()
    affiche_image("elsa.bmp",p1,p1,p2)

    while pas_echap():
        clock.tick(200)

        if(p2.x+v.x>__L or p1.x+v.x<0):
            v.x = -v.x
        if(p2.y+v.y>__H or p1.y+v.y<0):
            v.y = -v.y
        p1.x,p1.y = p1.x+v.x,p1.y+v.y
        p2.x,p2.y = p2.x+v.x,p2.y+v.y
        remplir_fenetre(noir)
        affiche_image("elsa.bmp",p1,p1,p2)
        affiche_tout()

def test_wait_clic():
    L = 1000
    H = 800
    init_fenetre(L,H,"Test wait_clic")
    while 1:
        clic = wait_clic()
        affiche_cercle_plein(clic,10,rouge)

def test_last_clic():
    L = 1000
    H = 800
    centre = Point(400,200)
    vitesse = Point(5,-2)
    rayon = 50
    couleur = rouge
    init_fenetre(L,H,"Test last_clic")
    affiche_auto_off()
    affiche_cercle_plein(centre,rayon,couleur)
    affiche_tout()
    while pas_echap():
        attendre(10)
        clic = last_clic()

        if clic:
            if not(__MODE_CLASSE_POINT):
                clic=Point(*clic)
            print("Clic en ({0},{1})".format(clic.x,clic.y))
        if clic and distance(centre,clic) <= rayon:
            break
        centre.x,centre.y = centre.x+vitesse.x,centre.y+vitesse.y
        if not( 0<=centre.x<L):
            vitesse.x = -vitesse.x
            centre.x += 2*vitesse.x
        if not( 0<=centre.y<H):
            vitesse.y = -vitesse.y
            centre.y += 2*vitesse.y

        remplir_fenetre(noir)
        affiche_cercle_plein(centre,rayon,couleur)
        affiche_tout()
    attendre_echap()

def test_get_fleches():
    L = 500
    H = 300
    init_fenetre(L,H,"Test get_fleches")
    charge_image("elsa.bmp")
    taille_img = Point(200,120)
    modifie_taille_image("elsa.bmp",taille_img.x,taille_img.y)
    affiche_auto_off()
    pos_img = Point(0,0)
    dep = 10
    remplir_fenetre(blanc)
    affiche_image("elsa.bmp",pos_img)
    affiche_tout()
    while 1:
        fleches = get_fleches()
        if not(__MODE_CLASSE_POINT):
            fleches=Point(*fleches)
        if (fleches.x != 0 or fleches.y != 0):
            pos_img.x += fleches.x*dep
            pos_img.y += fleches.y*dep
            pos_img.x = min(max(pos_img.x,0),L-taille_img.x)
            pos_img.y = min(max(pos_img.y,0),H-taille_img.y)
            remplir_fenetre(blanc)
            affiche_image("elsa.bmp",pos_img)
            affiche_tout()

def test_touche_enfoncee():
    L = 500
    H = 300
    init_fenetre(L,H,"Test touche_enfoncee")
    charge_image("elsa.bmp")
    taille_img = Point(200,120)
    modifie_taille_image("elsa.bmp",taille_img.x,taille_img.y)
    affiche_auto_off()
    pos_img = Point(0,0)
    dep = 10
    remplir_fenetre(blanc)
    affiche_image("elsa.bmp",pos_img)
    affiche_tout()
    while pas_echap():
        attendre(20)
        if touche_enfoncee('K_LEFT'):
            pos_img.x -= dep
        if touche_enfoncee('K_RIGHT'):
            pos_img.x += dep
        if touche_enfoncee('K_DOWN'):
            pos_img.y -= dep
        if touche_enfoncee('K_UP'):
            pos_img.y += dep

        pos_img.x = min(max(pos_img.x,0),L-taille_img.x)
        pos_img.y = min(max(pos_img.y,0),H-taille_img.y)
        remplir_fenetre(blanc)
        affiche_image("elsa.bmp",pos_img)
        affiche_tout()

def test_key_code():
    global __REPEAT_DELAY
    __REPEAT_DELAY = 0
    init_fenetre(300,100)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == KEYDOWN :
                for val in dir(pygame):
                    if val[0:2] == 'K_' and getattr(pygame,val) == event.key:
                        print(val)

#########################################
# Annexe : Main
#########################################

if __name__ == "__main__":
    #test_dessin()
    test_image()
    #test_wait_clic()
    #test_last_clic()
    #test_get_fleches()
    #test_touche_enfoncee()
    #test_key_code()

