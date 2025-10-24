import pygame
import sys
import os

pygame.init()

# ---------------------------- CONFIGURACIÓN DE RECURSOS Y CONSTANTES ----------------------------
RUTA_ARCHIVO_FONDO = "ciudad.jpg"
RUTA_JUGADOR = "UAIBOT.png"
RUTA_AUTO = "auto.png"
ENERGIA = 60
fuente = pygame.font.SysFont('Arial', 30)
FONDO_VEL_INICIAL = 3          # Velocidad base del fondo
FONDO_VEL_MAX = 15             # Límite máximo de velocidad
FONDO_AUMENTO_RATE =0.00000001     # Cuánto aumenta la velocidad por frame

AUTO_VEL_INICIAL = 7
AUTO_AUMENTO_RATE = 0.002      # La velocidad del auto aumenta también

COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_VERDE = (0, 200, 0)
COLOR_ROJO = (200, 0, 0)
COLOR_INSTRUCCION_FONDO = (50, 50, 50)

PANTALLA_ANCHO = 1280
PANTALLA_ALTO = 720
PISO_POS_Y = 650
FPS = 60

# Distancia inicial
kilometros_restantes = 1  # El tope inicial es 1 km

# Variables para mostrar mensaje de entrega
mostrar_mensaje = False
tiempo_mensaje = 0
duracion_mensaje = 2000  # milisegundos

# Tasa de decremento (0.03 km por segundo)
tasa_decremento = 0.03

# Variable para rastrear el tiempo de la última actualización
# Se usará para calcular el tiempo transcurrido
tiempo_anterior = pygame.time.get_ticks() / 1000.0



pantalla = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
pygame.display.set_caption("OFIRCA 2025 - Ronda 1 - Fondo animado")

font_TxtInstrucciones = pygame.font.SysFont(None, 36)
font_TxtGameOver = pygame.font.SysFont(None, 100)
font_Energia = pygame.font.SysFont(None, 30)  # 🔹 fuente para el porcentaje
clock = pygame.time.Clock()

# ---------------------------- CARGA DE IMÁGENES ----------------------------
try:
    img_fondo = pygame.image.load(RUTA_ARCHIVO_FONDO)
    img_fondo = pygame.transform.scale(img_fondo, (PANTALLA_ANCHO, PANTALLA_ALTO))
except:
    img_fondo = None
    print("Error al cargar el fondo")

try:
    jugador = pygame.image.load(RUTA_JUGADOR)
    jugador = pygame.transform.scale(jugador, (70, 70))
except:
    jugador = None
    print("Error al cargar el jugador")

try:
    auto = pygame.image.load(RUTA_AUTO)
    auto = pygame.transform.scale(auto, (100, 50))
except:
    auto = None
    print("Error al cargar el auto")

# ---------------------------- VARIABLES DE JUEGO ----------------------------
fondo_x = 0
fondo_vel = FONDO_VEL_INICIAL
auto_vel_x = AUTO_VEL_INICIAL
PAQUETES = 0

robot_x = 100
robot_y = PISO_POS_Y - 70

auto_x = PANTALLA_ANCHO
auto_y = PISO_POS_Y - 50

# Variables para el auto enemigo
auto_enemigo_color = (255, 0, 0)  # Rojo
auto_enemigo_x = PANTALLA_ANCHO + 300  # Empieza un poco después del auto normal
auto_enemigo_y = PISO_POS_Y - 50
auto_enemigo_vel = auto_vel_x  # misma velocidad que el auto
energia_reducida = 1  # cantidad de energía que resta al tocarlo

en_el_aire = False
velocidad_vertical = 0
fuerza_salto = -20
gravedad = 1

game_over = False
juegoEnEjecucion = True

# 🔹 Guardamos el tiempo de inicio

inicio_tiempo = pygame.time.get_ticks()
energia_actual = ENERGIA  # energía dinámica que puede aumentar con los paquetes

# Texto de instrucciones y game over
txtInstrucciones = font_TxtInstrucciones.render("Usa la barra espaciadora para saltar", True, COLOR_BLANCO)
txtInstrucciones_rect = txtInstrucciones.get_rect(topleft=(10, 10))
txtGameOver = font_TxtGameOver.render("JUEGO TERMINADO", True, COLOR_ROJO)
txtGameOver_rect = txtGameOver.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 - 200))

# ---------------------------- BUCLE PRINCIPAL ----------------------------
while juegoEnEjecucion:
    clock.tick(FPS)

    # 1. Obtener el tiempo actual en segundos
    tiempo_actual = pygame.time.get_ticks() / 1000.0

    # 2. Calcular el tiempo transcurrido desde la última actualización
    tiempo_delta = tiempo_actual - tiempo_anterior

    # 3. Calcular la cantidad de kilómetros a restar
    # (Tasa por segundo) * (Tiempo transcurrido en segundos)
    decremento = tasa_decremento * tiempo_delta

    # 4. Actualizar los kilómetros restantes
    kilometros_restantes -= decremento

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juegoEnEjecucion = False

        if not game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not en_el_aire:
                en_el_aire = True
                velocidad_vertical = fuerza_salto
        else:
            if event.type == pygame.KEYDOWN:
                juegoEnEjecucion = False
    # ---------------------------- CONTADOR DE KM ----------------------------
    # 5. Asegurarse de que el contador no baje de cero
    if kilometros_restantes < 0:
        kilometros_restantes = 0
    
    if kilometros_restantes <= 0:
        PAQUETES += 1
        kilometros_restantes = 1.0
        fondo_vel += 1.05
        auto_vel_x += 1.05
        mostrar_mensaje = True
        energia_actual *= 1.4  # aumenta la energía un 40% al entregar un paquete
        if PAQUETES >= 2:
            kilometros_restantes *= 0.2  # reducir la distancia para el siguiente paquete
            fondo_vel += 1.05
            auto_vel_x += 1.05

    tiempo_mensaje = pygame.time.get_ticks()

    # 6. Actualizar el tiempo anterior para el próximo ciclo
    tiempo_anterior = tiempo_actual


    # ---------------------------- FONDO EN MOVIMIENTO ----------------------------
    if img_fondo:
        # Desplaza el fondo hacia la izquierda
        fondo_x -= fondo_vel
        # Dibuja dos fondos seguidos para efecto de scroll infinito
        pantalla.blit(img_fondo, (fondo_x, 0))
        pantalla.blit(img_fondo, (fondo_x + PANTALLA_ANCHO, 0))
        # Reinicia la posición cuando el primer fondo sale de pantalla
        if fondo_x <= -PANTALLA_ANCHO:
            fondo_x = 0
    else:
        pantalla.fill(COLOR_BLANCO)

    # ---------------------------- PISO ----------------------------
    piso_altura = PANTALLA_ALTO - PISO_POS_Y
    pygame.draw.rect(pantalla, COLOR_VERDE, (0, PISO_POS_Y, PANTALLA_ANCHO, piso_altura))
    pygame.draw.line(pantalla, COLOR_NEGRO, (0, PISO_POS_Y), (PANTALLA_ANCHO, PISO_POS_Y), 3)

    # ---------------------------- MOVIMIENTO DEL ROBOT ----------------------------
    if not game_over:
        velocidad_vertical += gravedad
        robot_y += velocidad_vertical

        if robot_y >= PISO_POS_Y - jugador.get_height():
            robot_y = PISO_POS_Y - jugador.get_height()
            en_el_aire = False
            velocidad_vertical = 0

        # ---------------------------- MOVIMIENTO DEL AUTO ----------------------------
        auto_x -= auto_vel_x
        if auto_x < -auto.get_width():
            auto_x = PANTALLA_ANCHO

        # Movimiento del auto enemigo solo después de 2 km
        if PAQUETES >= 2 or kilometros_restantes <= 0.0:
            auto_enemigo_x -= auto_enemigo_vel
            if auto_enemigo_x < -100:  # reinicia cuando sale de pantalla
                auto_enemigo_x = PANTALLA_ANCHO + 200
                auto_enemigo_vel *= 1.05  # aumenta la velocidad del auto enemigo un 5% cada vez que reaparece


        # ---------------------------- AUMENTO DE VELOCIDAD CON EL TIEMPO ----------------------------
        if fondo_vel < FONDO_VEL_MAX:
            fondo_vel += FONDO_AUMENTO_RATE
            auto_vel_x += AUTO_AUMENTO_RATE

        # ---------------------------- DIBUJO DE ENTIDADES ----------------------------
        robot_rect = pantalla.blit(jugador, (robot_x, robot_y))
        auto_rect = pantalla.blit(auto, (auto_x, auto_y))
        auto_enemigo_rect = pygame.draw.rect(pantalla, auto_enemigo_color,
                                     (auto_enemigo_x, auto_enemigo_y, 100, 50))


        # ---------------------------- COLISIÓN ----------------------------
        if robot_rect.colliderect(auto_rect):
            game_over = True
        if robot_rect.colliderect(auto_enemigo_rect):
            energia_actual -= energia_reducida
            if energia_actual < 0:
                energia_actual = 0

        if not game_over:
            tiempo_transcurrido = (pygame.time.get_ticks() - inicio_tiempo) / 1000
            tiempo_restante = max(0, energia_actual - tiempo_transcurrido)
            porcentaje = tiempo_restante / energia_actual if energia_actual > 0 else 0

            # Si se acaba el tiempo → fin del juego
            if tiempo_restante <= 0:
                game_over = True

            # Dimensiones y posición de la barra
            barra_ancho = 300
            barra_alto = 30
            barra_x = 20
            barra_y = 60

            # Fondo gris oscuro
            pygame.draw.rect(pantalla, (80, 80, 80), (barra_x, barra_y, barra_ancho, barra_alto))
            # Parte verde proporcional al tiempo restante
            pygame.draw.rect(pantalla, COLOR_VERDE, (barra_x, barra_y, barra_ancho * porcentaje, barra_alto))

            # Texto del porcentaje
            texto_energia = font_Energia.render(f"{int(porcentaje * 60)}%", True, COLOR_BLANCO)
            texto_rect = texto_energia.get_rect(center=(barra_x + barra_ancho / 2, barra_y + barra_alto / 2))
            pantalla.blit(texto_energia, texto_rect)



    # ---------------------------- INTERFAZ ----------------------------
    puntos_text = font_TxtInstrucciones.render(f"Paquetes: {PAQUETES}", True, COLOR_BLANCO)
    pantalla.blit(puntos_text, (PANTALLA_ANCHO - 180, 10))


   
    
    # Formatear el texto para mostrar solo 2 decimales
    texto_contador = "Distancia restante: {:.2f} km".format(kilometros_restantes)
    superficie_texto = fuente.render(texto_contador, True, (255, 255, 255)) # Color blanco
    texto_rect = superficie_texto.get_rect(center=(PANTALLA_ANCHO // 2, 50))  # Centrado horizontal, 50 px desde arriba
    pantalla.blit(superficie_texto, texto_rect)

    # Mostrar mensaje de entrega si corresponde
    if mostrar_mensaje:
        tiempo_actual_ms = pygame.time.get_ticks()
        if tiempo_actual_ms - tiempo_mensaje < duracion_mensaje:
            texto_entrega = font_Energia.render("¡Paquete entregado!", True, COLOR_VERDE)
            rect_entrega = texto_entrega.get_rect(center=(PANTALLA_ANCHO // 2, PANTALLA_ALTO // 2 - 100))
            pantalla.blit(texto_entrega, rect_entrega)
        else:
            mostrar_mensaje = False
    # (Eliminado el mensaje de paquete entregado anterior)



    if not game_over:
        pygame.draw.rect(pantalla, COLOR_INSTRUCCION_FONDO,
                         (txtInstrucciones_rect.left - 10, txtInstrucciones_rect.top - 10,
                          txtInstrucciones_rect.width + 20, txtInstrucciones_rect.height + 20))
        pantalla.blit(txtInstrucciones, txtInstrucciones_rect)
    else:
        pantalla.blit(txtGameOver, txtGameOver_rect)

    pygame.display.flip()


pygame.quit()
sys.exit()
