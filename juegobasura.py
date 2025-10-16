import os
import pygame
import random

# Inicialización de pygame: prepara los módulos internos (pantalla, fuentes, etc.)
pygame.init()

# --------------------------------------------------
# Carga de recursos (imágenes)
# - Se asume que existe una carpeta 'img' al mismo nivel que este script
# - Nombres esperados: player.png, garbage.png, background.jpg
# --------------------------------------------------
scriptDir = os.path.dirname(__file__)  # carpeta del script actual
rutaImagenes = os.path.join(scriptDir, 'img')
# cargar imágenes (lanza excepción si no están presentes)
jugador = pygame.image.load(os.path.join(rutaImagenes, 'player.png'))
basura = pygame.image.load(os.path.join(rutaImagenes, 'garbage.png'))
fondo = pygame.image.load(os.path.join(rutaImagenes, 'background.jpg'))

# --------------------------------------------------
# Configuración de pantalla y variables globales
# --------------------------------------------------
COLOR_NEGRO = (0, 0, 0)
# offset determina dónde dibujamos el fondo dentro de la ventana.
# Si quieres que el fondo ocupe toda la ventana, pon offset = (0,0).
offset = (0, 0)

# Calculamos el tamaño de la ventana a partir del tamaño del fondo
fw, fh = fondo.get_size()
tamano = (fw + offset[0], fh + offset[1])
pantalla = pygame.display.set_mode(tamano)

# Rectángulos auxiliares para colisión/posición
jugadorRect = jugador.get_rect()   # rect de la imagen del jugador
basuraRect = basura.get_rect()     # rect de la imagen de basura (tamaño)

# Estado del juego
puntos = 0                          # puntuación
basuraNivel = []                    # lista de rects con basura del nivel
tipografia = pygame.font.SysFont("monospace", 15)  # fuente para textos
tiempoRestante = 0                  # temporizador del nivel
contadorNivel = 0                   # número de niveles completados
realizado = False                   # flag de salida del bucle principal


# --------------------------------------------------
# Funciones del juego
# --------------------------------------------------

def moverJugadorHacia(coords):
    """
    Mueve (teletransporta) el jugador al centro de las coordenadas dadas.
    coords: tupla (x, y) normalmente tomada de pygame.mouse.get_pos().
    """
    jugadorRect.center = coords


def chequearColisiones():
    """
    Revisa colisiones entre el rect del jugador y cada rect de basura.
    Si hay colisión, incrementa puntos y elimina la basura golpeada.
    Nota: iteramos sobre una copia implícita de la lista original para
    evitar problemas al eliminar elementos mientras iteramos.
    """
    global puntos
    # iterar sobre una copia evita 'skip' al remover elementos
    for g in basuraNivel[:]:
        if jugadorRect.colliderect(g):
            puntos += 1
            basuraNivel.remove(g)


def dibujar():
    """
    Dibuja toda la escena en cada frame:
    - limpia la pantalla
    - dibuja el fondo en el offset definido
    - dibuja cada basura en su posición
    - dibuja el jugador
    - dibuja HUD: puntos y tiempo restante
    - actualiza la pantalla
    """
    pantalla.fill(COLOR_NEGRO)
    pantalla.blit(fondo, offset)

    # dibujar cada basura usando sus coordenadas (left, top)
    for g in basuraNivel:
        pantalla.blit(basura, (g.left, g.top))

    # dibujar jugador
    pantalla.blit(jugador, (jugadorRect.left, jugadorRect.top))

    # HUD: puntos
    label = tipografia.render("Puntos: " + str(puntos), 1, (255, 255, 255))
    pantalla.blit(label, (0, 30))

    # Mensaje de fin (se muestra cuando el contador de niveles es mayor a 2)
    label2 = tipografia.render("Fin del juego!", 1, (255, 255, 255))
    if contadorNivel > 2:
        pantalla.blit(label2, (0 + label.get_rect().width + 10, 0))

    # Mostrar tiempo restante al lado del HUD
    label3 = tipografia.render("Tiempo Restante: " + str(tiempoRestante), 1, (255, 255, 255))
    pantalla.blit(label3, (0 + label.get_rect().width + label2.get_rect().width + 20, 0))

    # Actualiza la pantalla completa (flip)
    pygame.display.flip()


def crearUnaBasura():
    """
    Crea un nuevo rect para una basura posicionada aleatoriamente dentro
    del área ocupada por el fondo. Devuelve una copia del rect con left/top
    asignados.
    """
    temp = basuraRect.copy()
    # generar posiciones dentro del área del fondo (no fuera de la pantalla)
    fw, fh = fondo.get_size()
    min_x = offset[0]
    min_y = offset[1]
    # Si la imagen de basura es más grande que el fondo, el cálculo
    # fw - temp.width será negativo y producirá un rango vacío.
    # Para evitar ValueError, clamp (limitar) max_x/max_y a al menos min_x/min_y.
    max_x = offset[0] + max(0, fw - temp.width)
    max_y = offset[1] + max(0, fh - temp.height)
    # Asegurar que los límites son válidos (por si offset o tamaños son extraños)
    if max_x < min_x:
        max_x = min_x
    if max_y < min_y:
        max_y = min_y
    # randint incluye ambos extremos; si max_x==min_x se colocará en min_x
    temp.left = random.randint(min_x, max_x)
    temp.top = random.randint(min_y, max_y)
    return temp


def crearNivel(amount):
    """
    Inicializa la lista de basura del nivel actual con 'amount' elementos
    colocados aleatoriamente dentro del fondo, y reinicia el temporizador.
    """
    global tiempoRestante
    tiempoRestante = 10
    basuraNivel.clear()
    for x in range(amount):
        basuraNivel.append(crearUnaBasura())


# Inicializar primer nivel al inicio del juego: crea 5 basuras
crearNivel(5)


def avanzarNivel():
    """
    Si no queda basura en el nivel actual, incrementa contadorNivel y
    crea un nuevo nivel cuando proceda. Esta función puede ampliarse para
    ajustar dificultad (más basura, menos tiempo, etc.).
    """
    global contadorNivel
    global tiempoRestante
    if len(basuraNivel) == 0:
        contadorNivel += 1
        tiempoRestante = 0
        # ejemplo: a partir de cierto nivel, generar más basura
        if (contadorNivel > 3):
            crearNivel(7 + 3 * contadorNivel)


# Configurar un evento de pygame que se dispare cada 1000 ms (1 segundo)
pygame.time.set_timer(pygame.USEREVENT, 1000)


def decrementarTiempo():
    """
    Llamada cada segundo por el USEREVENT. Resta tiempo restante y,
    cuando llega a cero, decide si avanzar de nivel (si no queda basura)
    o reiniciar el temporizador para el mismo nivel (si aún hay basura).
    """
    global tiempoRestante
    global contadorNivel
    # decrementar el tiempo cada segundo y pasar de nivel cuando llegue a 0
    if tiempoRestante > 0:
        tiempoRestante -= 1
    if tiempoRestante <= 0:
        # si se acaba el tiempo y no hay basura, avanzar de nivel
        if len(basuraNivel) == 0:
            contadorNivel += 1
            crearNivel(5 + 3 * contadorNivel)
        else:
            # si queda basura pero se acaba el tiempo, reiniciar tiempo para ese nivel
            tiempoRestante = 10
    return False


# --------------------------------------------------
# Bucle principal del juego
# - procesa eventos
# - actualiza estado (mover jugador, colisiones, avanzar nivel)
# - dibuja la escena
# --------------------------------------------------
while not realizado:
    # --- Bucle de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.USEREVENT:
            # temporizador: decrementar tiempo cada segundo
            decrementarTiempo()
        if evento.type == pygame.QUIT:
            # cerrar la ventana y terminar el bucle
            realizado = True
            break

    # Lógica del juego: solo procesar niveles si no hemos alcanzado el tope
    if contadorNivel < 3:
        avanzarNivel()
        # Mover jugador para que siga el cursor del ratón
        moverJugadorHacia(pygame.mouse.get_pos())
        # Comprobar y resolver colisiones jugador-basura
        chequearColisiones()

    # Dibujar todo en pantalla cada iteración
    dibujar()

# Salir limpiamente de pygame
pygame.quit()




