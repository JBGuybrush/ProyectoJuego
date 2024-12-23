#importamos la librería para usar su lenguaje en nuestro código.
import pygame
from Juego.gameclass import GameObject, Character

#Pygame setup
#Pygame inicialización
pygame.init() #esto marca el punto de arranque de la librería Pygame
#Creo una ventana
width = 800
height = 600
screen = pygame.display.set_mode((width, height)) #Alternativa ocupar pantalla: screen = pygame.FULLSCREEN
clock = pygame.time.Clock()

# Cargar el personaje/s del juego
player = Character("player", screen, width/2, height/2)
##player2 = GameObject("player2", screen, width/2 - 30, height/2, "Owlet_Monster.png") segundo jugador
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
    # comienzas a llamar a eventos que van a ocurrir mientras funciona
    # .get le pide que tome todos los eventos que van ocurriendo dentro del bucle infinito
    for event in pygame.event.get(): #condicionas el comportamiento con los eventos que marcas a continuación
        if event.type == pygame.KEYDOWN: #tomar y registrar al momento la letra pulsada por el usuario
            #print("Tecla apretada")
            if event.unicode == "w":
                player.move_up() #si no pongo un número en el paréntesis moverá -5 en y por defecto.
                key_press = "w"
                player_move = True
            elif event.unicode == "d":
                # Control de la orientación de la imagen en el movimiento
                player_moving_right = True
                if player_moving_left:
                    imgFlip = pygame.transform.flip(player.get_image(),True,False)
                    player_moving_left = False
                    player.set_image(imgFlip)
                player.move_right()
                key_press = "d"
                player_move = True
            elif event.unicode == "a":
                ## Control de la orientación de la imagen en el movimiento
                player_moving_left = True
                if player_moving_right:
                    imgFlip = pygame.transform.flip(player.get_image(),True,False)
                    player_moving_right = False
                    player.set_image(imgFlip)
                ##
                player.move_left()
                key_press = "a"
                player_move = True
            elif event.unicode == "s":
                player.move_down()
                key_press = "s"
                player_move = True

# Vamos a obligar al código a pasar por aquí en bucle para que el movimiento sea más fluido por la pantalla.
        if player_move:
            if key_press == "w":
                player.move_up(4)
            if key_press == "d":
                player.move_right(4)
            if key_press == "a":
                player.move_left(4)
            if key_press == "s":
                player.move_down(4)

        if event.type == pygame.KEYUP:
            player_move = False  #para que salga del bucle del movimiento al levantar la tecla

        if event.type == pygame.QUIT: # si ocurre este evento se refiere a que sea pulsada la X de cierre de ventana
            running = False #en caso de este evento sale del bucle con False

    # Color elegido para la ventana mientras se mantenga en el bucle de funcionamiento
    screen.fill([188,170,164]) # códigos numéricos de color preestablecidos. Buscar referencia del color en "material colours" en google.

    # Pintamos al héroe en la pantalla
    screen.blit(player.get_image(), player.get_rect())

    ##screen.blit(player2.get_image(), player2.get_rect()) para representar al segundo jugador


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip() #sin esto no mostraría lo que hemos configurado para el screen
    clock.tick(60) # Para que se refresque el juego a 60fps
pygame.quit()