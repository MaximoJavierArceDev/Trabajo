# Librerías
from turtle import Screen, Turtle
from random import randint, choice

# Seteos iniciales
limite = 25
screen = Screen()
screen.colormode(255)
screen.setup(400, 400)
formas = ['arrow', 'turtle', 'circle', 'square', 'triangle', 'classic']


# Funciones
def cualquierColor(turtle_obj=None):
    """Establece y devuelve un color RGB aleatorio. Si se pasa un Turtle, lo aplica."""
    rojo = randint(0, 255)
    verde = randint(0, 255)
    azul = randint(0, 255)
    if turtle_obj is not None:
        turtle_obj.color((rojo, verde, azul))
    return (rojo, verde, azul)


def cualquierLugar(turtle_obj):
    """Mueve el turtle a una posición aleatoria sin dibujar."""
    x = randint(-180, 180)
    y = randint(-180, 180)
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.pendown()


def dibujarRectangulo(turtle_obj, length=None, height=None):
    """Dibuja un solo rectángulo usando el turtle proporcionado."""
    turtle_obj.right(randint(0, 360))
    cualquierColor(turtle_obj)
    cualquierLugar(turtle_obj)
    turtle_obj.hideturtle()
    length = length or randint(10, 100)
    height = height or randint(10, 100)
    turtle_obj.begin_fill()
    turtle_obj.forward(length)
    turtle_obj.right(90)
    turtle_obj.forward(height)
    turtle_obj.right(90)
    turtle_obj.forward(length)
    turtle_obj.right(90)
    turtle_obj.forward(height)
    turtle_obj.right(90)
    turtle_obj.end_fill()


def main():
    # Turtle principal para rectángulos
    t = Turtle()
    t.speed(0)

    # Dibujar varios rectángulos
    for _ in range(randint(5, limite)):
        dibujarRectangulo(t)

    # Stamps con distintas formas
    stamper = Turtle()
    stamper.hideturtle()
    stamper.penup()
    for _ in range(randint(5, limite)):
        forma = choice(formas)
        stamper.shape(forma)
        cualquierColor(stamper)
        cualquierLugar(stamper)
        stamper.stamp()

    # Puntos aleatorios
    dotter = Turtle()
    dotter.hideturtle()
    dotter.penup()
    for _ in range(randint(10, limite * 2)):
        cualquierColor(dotter)
        cualquierLugar(dotter)
        dotter.dot(randint(5, 50))

    # Mantener la ventana abierta
    screen.mainloop()


if __name__ == '__main__':
    main()
