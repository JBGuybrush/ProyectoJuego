#en este archivo vamos a generar las clases con los objetos que necesitamos en el juego
# necesitamos que tenga como atributos:
# tag, posición en X (pos_X), posición en Y (pos_y), imagen

# creamos también un metodo para devolver la imagen de un objeto (get_image)
# creamos un metodo para devolver el rectángulo de la imagen (get_rect)

import pygame
from enum import Enum

class GameObject:
    #constructor
    def __init__(self, tag, screen, pos_x=0, pos_y=0, image="Pink_Monster.png"):
# queda por defecto definida posición x=0 e y=0 e imagen de monstruo rosa si no se concreta otra ahora a continuación en el código
        print(f"Creando el objeto: {tag}") #así nos aparece un mensaje en consola con el nombre que le hallamos dado en tag.

        #vamos a crear los ATRIBUTOS DE LA INSTANCIA:
        self.tag = tag
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = image

        #ATRIBUTOS PRIVADOS para la carga de imágenes sin tener que escribir en el código del juego cada una
        self.__img = pygame.image.load(self.image)
            #la doble __ la hace privada
        self.__img.convert()
        self.__rect = self.__img.get_rect()
        self.__screen = screen
        self.__rect.center = (self.pos_x, self.pos_y) #para que tome la posición que le pidamos en el código y muestre ahí la imagen


# Mover hacia arriba el GameObject
    def move_up(self,y=5): #Así si no especifica moverá 5 en y cada vez que se presione la tecla.
        #print(self.__rect.y) #para que aparezca en consola la posición en que se encuentra tras moverse
        if (self.__rect.top-y) > 0: #para que deje de moverse cuando llegue arriba de la pantalla.
            self.__rect.move_ip(0,-y)
# Mover a la derecha el GameObject
    def move_right(self, x=5):
        if self.__rect.right+x < self.__screen.get_width(): #para que no se mueva más allá del 800 en este caso que es el ancho del screen
            self.__rect.move_ip(x, 0)

    def move_left(self, x=5):
       if (self.__rect.left-x) > 0:
            self.__rect.move_ip(-x, 0)

    def move_down(self, y=5):
        if (self.__rect.bottom+y) < self.__screen.get_height():
            self.__rect.move_ip(0, y)

    #Función que devuelve la imagen del GameObject porque si no no puede alcanzar al img el archivo del juego
    def get_image(self):
        return self.__img

    #Función (metodo) que actualiza la orientación del GameObject
    def set_image(self, image):
        self.__img = image

    #Función que devuelve el rectángulo de la imagen para llamarla y no poner esta línea tampoco en el código del juego
    def get_rect(self):
        return self.__rect

# Class Character
# Atributo nuevo:
# - vida

class Character(GameObject): # sería la clase Child que hereda de la parent (GameObject)
    # Constructor
    def __init__(self, tag, screen, pos_x=0, pos_y=0, image="Pink_Monster.png", vida=3):
        super().__init__(tag, screen, pos_x, pos_y, image) # el super() añadirá el nuevo atributo vida a los del Parent

        # establezco el nuevo atributo como privado con __
        self.__vida = vida

    def perder_vida (self, damage = 1):
        self.__vida -= damage #para restar el valor

# Función para la comprobación de colisión entre objetos. Toma como referencia al character para comprobar, no al mapa.
    def __comprobar_colision(self,game_objects_list):
        # Debo excluir de la comprobación al jugador que está en posición 0
        # OJO con el tema de la posición 0
        for i in range (1, len(game_objects_list)):
            # si colisiona no puedo moverlo
            if game_objects_list[i].get_rect().colliderect(game_objects_list[0].get_rect()):
                return True
        return False

    def move_character_right(self, game_objects_list, x=5):
        super().move_right(x)
        if self.__comprobar_colision(game_objects_list) == True:
            super().move_left(x)

    def move_character_left(self, game_objects_list, x=5):
        super().move_left(x)
        if self.__comprobar_colision(game_objects_list) == True:
            super().move_right(x)

    def move_character_up(self, game_objects_list, y=5):
        super().move_up(y)
        if self.__comprobar_colision(game_objects_list) == True:
            super().move_down(y)

    def move_character_down(self, game_objects_list, y=5):
        super().move_down(y)
        if self.__comprobar_colision(game_objects_list) == True:
            super().move_up(y)

# Class Obstacle
# Atributo:
# - damage (daño)
class TypeObstacle(Enum):
    FURNITURE = 1
    TRAP = 2

class Obstacle(GameObject):
    def __init__(self, tag, screen, pos_x=0, pos_y=0, image="Pink_Monster.png", type_obstacle = TypeObstacle.FURNITURE, damage=0):
        super().__init__(tag,screen,pos_x,pos_y,image)
        #self.__damage = 0 if type_obstacle == TypeObstacle.FURNITURE else 1 ## ES OTRA FORMA DE PONER LO SIGUIENTE:
        if type_obstacle == TypeObstacle.TRAP:
            self.__damage = 1
        else:
            self.__damage = 0

# Class Item
# Atributo nuevo:
# - vida