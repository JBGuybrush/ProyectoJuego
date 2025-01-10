#importamos la librería para usar su lenguaje en nuestro código.
import pygame
import random # Vamos a usar random.randint de esta librería para generar aleatoriamente posición de rocas en el código

from pygame.constants import K_ESCAPE

from Juego.gameclass import Character, Obstacle

#Pygame setup
#Pygame inicialización
pygame.init() #esto marca el punto de arranque de la librería Pygame
#Creo una ventana
width = 800
height = 600
screen = pygame.display.set_mode((width, height)) #Alternativa ocupar pantalla: screen = pygame.FULLSCREEN
clock = pygame.time.Clock()

#Comenzaría a crear los GameObjects
game_objects_list = [] #en esta lista se incorporarán los elementos

# Cargar el personaje/s del juego
player = Character("player", screen, width/2, height/2)
game_objects_list.append(player)

# Añadir un número de rocas
num_rocks = 4
for id_rock in range(num_rocks):
    rock = Obstacle(f"rock{id_rock}", screen, random.randint(50, width -15), random.randint(50, height -15), "rock.png")
    # Comprobar si el nuevo GameObject colisiona con todos los anteriores
    for id in range(len(game_objects_list)):
        #Comprobamos la colisión para rock y el id
        if (game_objects_list[id].get_rect().colliderect(rock.get_rect())):
            rock = Obstacle(f"rock{id_rock}", screen, random.randint(50, width -15), random.randint(50, height -15),
                            "rock.png")
            id_rock = 0
    # El nuevo objeto no colisiona
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

        if event.type == pygame.KEYUP:
            print("Tecla levantada")

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # salir pulsando X de cierre o ESC.
            running = False #en caso de este evento sale del bucle con False



    # Color elegido para la ventana mientras se mantenga en el bucle de funcionamiento
    screen.fill([188,170,164]) # códigos numéricos de color preestablecidos. Buscar referencia del color en "material colours" en google.

    # Pintamos los objetos
    for game_object in game_objects_list:
        screen.blit(game_object.get_image(), game_object.get_rect())

    ##screen.blit(player2.get_image(), player2.get_rect()) para representar al segundo jugador


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip() #sin esto no mostraría lo que hemos configurado para el screen
    clock.tick(60) # Para que se refresque el juego a 60fps
pygame.quit()