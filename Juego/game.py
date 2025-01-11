#importamos la librería para usar su lenguaje en nuestro código.
import pygame
import random # Vamos a usar random.randint de esta librería para generar aleatoriamente posición de rocas en el código
import time
from pygame.constants import K_ESCAPE

from Juego.gameclass import Character, Obstacle, TypeObstacle, Door, TypeDoor, Key

#Pygame setup
#Pygame inicialización
pygame.init() #esto marca el punto de arranque de la librería Pygame
#Creo una ventana
width = 800
height = 600
screen = pygame.display.set_mode((width, height)) #Alternativa ocupar pantalla: screen = pygame.FULLSCREEN
clock = pygame.time.Clock()

# Cargamos una imagen para el fondo
background = pygame.image.load("tile.png")
background = pygame.transform.scale(background, (width, height))

#Comenzaría a crear los GameObjects
game_objects_list = [] #en esta lista se incorporarán los elementos

# Cargar el personaje/s del juego
player = Character("player", screen,70, 100) #marco esa posición en (x,y) para que aparezca delante de la puerta
game_objects_list.append(player)


# Añadir una valla de entrada y una de salida al mapa
entrance_door = Door("entrada", screen, 130, 100, "dooropen.png", TypeDoor.ENTRANCE, is_open=True)
exit_door = Door("salida", screen, width - 80, height - 180, "doorshut.png", TypeDoor.EXIT, is_open=False)
game_objects_list.append(entrance_door)
game_objects_list.append(exit_door)

# Añadir una llave al mapa
key = Key("palanca", screen, random.randint(50, width - 50), random.randint(50, height - 50), "lever.png", used=False)
game_objects_list.append(key)

# Variables para controlar si la llave ha sido recogida y si hemos pasado la salida
key_collected = False
puerta_alcanzada = False

# Por último, añadimos un número de rocas al mapa, para que haga al comprobación de si colisiona con el resto de rectángulos antes de aparecer.
num_rocks = 5
for id_rock in range(num_rocks):
    rock = Obstacle(f"rock{id_rock}", screen, random.randint(20, width -20), random.randint(20, height -20), "rock.png", TypeObstacle.TRAP)
    # Comprobar si el nuevo GameObject "rock" colisiona con todos los anteriores
    for id in range(len(game_objects_list)):
        #Comprobamos la colisión para rock y el id
        if (game_objects_list[id].get_rect().colliderect(rock.get_rect())):
            rock = Obstacle(f"rock{id_rock}", screen, random.randint(20, width -20), random.randint(20, height -20),
                            "rock.png")
            id_rock = 0
    # El nuevo objeto no colisiona y se añade a la lista
    game_objects_list.append(rock)

# Control del movimiento con tecla apretada:
player_move = False
key_press = "" #¿Qué tecla he apretado?
# Control del movimiento para el cambio de orientación de la imagen
player_moving_left = False
player_moving_right = False

# ¿Cómo hacerlo escribiendo a fuego en el código? si no lo cargo con POO de otro archivo como clase es así:
    #img = pygame.image.load('Pink_monster.png')
    #img.convert()
    #imgrect = img.get_rect()
    #imgrect.center = (width/2, height/2) #esto coloca al personaje en el centro de la pantalla con los tamaños que hemos definido.

# Arranca el bucle del juego
running = True

while running:

    keys = pygame.key.get_pressed() # Metodo de Pygame que devuelve el estado de las teclas para generar movimiento continuo.
    # comienzas a llamar a eventos que van a ocurrir mientras funciona
    # .get le pide que tome todos los eventos que van ocurriendo dentro del bucle infinito
    for event in pygame.event.get(): #condicionas el comportamiento con los eventos que marcas a continuación

    #según la letra pulsada generaremos un movimiento en nuestro character
        if keys[pygame.K_w]:  # Si la tecla "w" es presionada
            player.move_character_up(game_objects_list, 10) #si no pusiera un número en el paréntesis moverá -5 en y por defecto, elijo 10 para que vaya más fluido.

        if keys[pygame.K_d]:  # Si la tecla "d" es presionada
            player.move_character_right(game_objects_list, 10)  # Le pasamos el game_objects_list para la comprobación de colisiones entre objetos
        # Control de la orientación de la imagen en el movimiento dependiendo de su movimiento previo
            if player_moving_left:
                imgFlip = pygame.transform.flip(player.get_image(), True, False)
                player.set_image(imgFlip)
                player_moving_right = True
                player_moving_left = False

        if keys[pygame.K_a]:  # Si la tecla "a" es presionada
            player.move_character_left(game_objects_list, 10)
        # Control de la orientación de la imagen en el movimiento dependiendo de su movimiento previo
            if not player_moving_left:
                imgFlip = pygame.transform.flip(player.get_image(), True, False)
                player_moving_left = True
                player_moving_right = False
                player.set_image(imgFlip)

        if keys[pygame.K_s]:  # Si la tecla "s" es presionada, movemos hacia abajo.
            player.move_character_down(game_objects_list, 10)

        #if event.type == pygame.KEYUP: Usado para verificar si está registrando correctamente cuandos e levanta la tecla.
            #print("Tecla levantada")

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # salir pulsando X de cierre o ESC.
            running = False #en caso de este evento sale del bucle con False

    # Comprobar si el personaje colisiona con la llave
    if not key_collected and player.get_rect().colliderect(key.get_rect()):
        print("¡Palanca accionada!")
        key_collected = True
        key.use()  # Marca la llave como usada
        exit_door.open_door()  # Abre la puerta de salida
        print("¡Valla de salida abierta!")
        exit_door.update_image()

    if player.get_rect().colliderect(exit_door.get_rect()):
        if not puerta_alcanzada:
            print("Puerta de salida alcanzada")
            print("FINISH HIM! PRESS ESC")
            puerta_alcanzada = True

    # Color elegido para la ventana mientras se mantenga en el bucle de funcionamiento.
    screen.fill((46, 125, 50)) # He obtenido de "material colours" el código hexadecimal #2E7D32 y lo he pasado a RGB para que aparezca verde bosque el fondo.

    #Pintamos el fondo
    screen.blit(background, (0, 0))
    # Pintamos los objetos
    for game_object in game_objects_list:
        screen.blit(game_object.get_image(), game_object.get_rect())

    ##screen.blit(player2.get_image(), player2.get_rect()) para representar al segundo jugador

    # flip() para mostrar el trabajo completo en pantalla
    pygame.display.flip() #sin esto no mostraría lo que hemos configurado para el screen
    clock.tick(60) # Para que se refresque el juego a 60fps
pygame.quit()