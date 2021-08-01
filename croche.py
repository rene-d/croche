#!/usr/bin/env python3
# rene-d 2021
# Licence: CC BY-SA 3.0


import turtle
import math

pixel = 1
precision = 2
scale = 3.9721798560812203


#              q4
#                    q3
#
#  q1
#       q2
q1, q2, q3, q4 = None, None, None, None
bezier_curves = []


def turtle_bezier(turtle, p0, p1, p2, p3):
    """ Trace la courbe de Bézier définie par les quatre points. """
    global q1, q2, q3, q4

    # print(f"bezier({p0},{p1},{p2},{p3})")
    bezier_curves.append((p0, p1, p2, p3))

    turtle.penup()
    turtle.goto(p0)
    turtle.pendown()

    # turtle.dot(5, "blue")

    t = 0
    while t < 1:
        t += 0.01

        x = p0[0] * (1 - t) ** 3 + 3 * p1[0] * t * (1 - t) ** 2 + 3 * p2[0] * (t ** 2) * (1 - t) + p3[0] * (t ** 3)
        y = p0[1] * (1 - t) ** 3 + 3 * p1[1] * t * (1 - t) ** 2 + 3 * p2[1] * (t ** 2) * (1 - t) + p3[1] * (t ** 3)

        if q1 is None:
            q1, q2, q3, q4 = (x, y), (x, y), (x, y), (x, y)
        else:
            if q1[0] > x:
                q1 = (x, y)
            if q2[1] > y:
                q2 = (x, y)
            if q3[0] < x:
                q3 = (x, y)
            if q4[1] < y:
                q4 = (x, y)

        if turtle.distance(x, y) >= pixel * precision:
            turtle.goto(x, y)

    turtle.goto(p3)

    # turtle.penup()
    # turtle.color("red")
    # turtle.goto(p0)
    # turtle.pendown()
    # turtle.goto(p1)
    # turtle.goto(p2)
    # turtle.goto(p3)
    # turtle.color("black")


def rotation(x, y, xc, yc, a):
    """ Rotation plane autour du point (xc,yc). """
    x = x - xc
    y = y - yc
    a = math.radians(a)
    x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
    return x + xc, y + yc


def head_bezier():
    """ Recherche l'angle de la tête en maximisant la verticalité de (q2,q4) et l'horizontalité de (q1,q3) (points extrêmes). """

    def box(angle):

        q1, q2, q3, q4 = None, None, None, None
        for p0, p1, p2, p3 in bezier_curves:

            t = 0
            while t < 1:
                t += 0.01

                x = p0[0] * (1 - t) ** 3 + 3 * p1[0] * t * (1 - t) ** 2 + 3 * p2[0] * (t ** 2) * (1 - t) + p3[0] * (t ** 3)
                y = p0[1] * (1 - t) ** 3 + 3 * p1[1] * t * (1 - t) ** 2 + 3 * p2[1] * (t ** 2) * (1 - t) + p3[1] * (t ** 3)

                x, y = rotation(x, y, 0, 0, angle)

                if q1 is None:
                    q1, q2, q3, q4 = (x, y), (x, y), (x, y), (x, y)
                else:
                    if q1[0] > x:
                        q1 = (x, y)
                    if q2[1] > y:
                        q2 = (x, y)
                    if q3[0] < x:
                        q3 = (x, y)
                    if q4[1] < y:
                        q4 = (x, y)

        w = q3[0] - q1[0]
        l = q4[1] - q2[1]

        e = (q1[1] - q3[1]) ** 2 + abs(q2[0] - q4[0]) ** 2

        return e, w, l

    e_min = 1
    a_min = 0
    for a in range(250, 350):
        e, w, l = box(-a / 10)
        if e_min > e:
            e_min = e
            a_min = -a / 10

    angle = a_min
    e, w, l = box(angle)

    print(f"tête angle:     {angle}°")
    print(f"tête grand axe: {w*scale:7.3f}")
    print(f"tête petit axe: {l*scale:7.3f}")


def curveto(a, b, c):
    """ Similaire à \curveto de PSTricks. """
    p0 = turtle.pos()
    turtle_bezier(turtle, p0, a, b, c)


def moveto(x, y):
    """ Similaire à \moveto de PSTricks. """
    turtle.penup()
    turtle.goto(x, y)


def lineto(x, y):
    """ Similaire à \lineto de PSTricks. """

    turtle.pendown()
    turtle.goto(x, y)


def roundedrect(a, b, d):
    """ Trace un rectangle aux coins arrondis. """

    # turtle.color("red")
    # turtle.penup()
    # turtle.goto(a[0],a[1])
    # turtle.pendown()
    # turtle.goto(b[0],a[1])
    # turtle.goto(b[0],b[1])
    # turtle.goto(a[0],b[1])
    # turtle.goto(a[0],a[1])
    # turtle.color("black")

    turtle.penup()
    turtle.goto(a[0], a[1] - d)
    turtle.pendown()
    turtle.goto(b[0], a[1] - d)
    turtle.setheading(0)
    turtle.circle(d, 90, steps=10)
    turtle.goto(b[0] + d, b[1])
    turtle.setheading(90)
    turtle.circle(d, 90, steps=10)

    turtle.goto(a[0], b[1] + d)
    turtle.setheading(180)
    turtle.circle(d, 90, steps=10)

    turtle.goto(a[0] - d, a[1])
    turtle.setheading(270)
    turtle.circle(d, 90, steps=10)


def mire(x, y, r):
    """ Cercle et rayons perpendiculaires. """
    turtle.color("red")
    moveto(x, y)
    turtle.pendown()
    turtle.circle(r, steps=50)
    moveto(x - r, y + r)
    lineto(x + r, y + r)
    moveto(x, y)
    lineto(x, y + r * 2)
    turtle.color("black")


# initialisation Turtle
r = turtle.window_width() / turtle.window_height()
e = (50 - 0) - (45 - 15)
turtle.setworldcoordinates((15 - e / 2) * r, 0, (45 + e / 2) * r, 50)
turtle.speed("fastest")
turtle.hideturtle()
px = turtle.window_height() / (45 - 15 + e)
py = turtle.window_height() / (50 - 0)
pixel = 1 / px

if True:
    # tête ovale / note head
    moveto(27.75965107, 14.62279269)
    curveto((26.03666357, 14.62279269), (24.34675743, 13.99322896), (22.82268221, 13.09861144))
    curveto((20.83461971, 11.90577394), (18.48202607, 9.85154872), (18.48202607, 6.80297416))
    curveto((18.48202607, 4.18530552), (20.73516357, 2.95938666), (23.08775721, 2.95938666))
    curveto((24.81074471, 2.95938666), (26.50065085, 3.58895039), (28.02472607, 4.48356791))
    curveto((30.01278857, 5.67640541), (32.36538221, 7.73063063), (32.36538221, 10.77920519))
    curveto((32.36538221, 13.39687383), (30.14532607, 14.62279269), (27.75965107, 14.62279269))

if True:
    # vérification tête ovale
    head_bezier()
    turtle.color("green")
    # moveto(*q1); turtle.dot(5, "green"); lineto(*q3)
    # moveto(*q2); turtle.dot(5, "green"); lineto(*q4)
    # moveto(*q3); turtle.dot(5, "green")
    # moveto(*q4); turtle.dot(5, "green")
    # roundedrect((q1[0], q2[1]), (q3[0], q4[1]), 0)
    hc = (q1[0] + q3[0]) / 2, (q2[1] + q4[1]) / 2
    # print(hc)
    moveto(*hc)
    # turtle.dot(5, "green")
    # inclinaison ~ 31.1°
    turtle.color("red")
    for a in range(0, 360, 90):
        moveto(*hc)
        turtle.setheading(31.1 + a)
        turtle.pendown()
        turtle.forward(8)
    turtle.color("black")

    print(f"tête largeur:   {(q3[0]-q1[0])*scale:7.3f}")
    print(f"tête hauteur:   {(q4[1]-q2[1])*scale:7.3f}")

if True:
    # hampe / stem
    d = 32.38478628 - 31.96966
    # moveto(31.4478-d, 11.1999985-d)
    # lineto(31.96966+d, 11.1999985-d)
    # lineto(31.96966+d, 45.3449985+d)
    # lineto(31.4478-d, 45.3449985+d)
    # lineto(31.4478-d, 11.1999985-d)
    roundedrect((31.4478, 11.1999985), (31.96968, 45.3449985), d)

    print(f"hampe largeur:  {(d+31.96968-31.4478+d)*scale:7.3f}")
    print(f"hampe hauteur:  {(d+45.3449985-11.1999985+d)*scale:7.3f}")

if True:
    # crochet / flag
    moveto(32.38474387, 45.34187722)
    lineto(31.72205637, 45.34187722)
    lineto(31.72205637, 34.77195858)
    lineto(32.38474387, 34.77195858)
    curveto((35.43310637, 31.62413994), (39.44231273, 27.21732108), (39.44231273, 22.81050222))
    curveto((39.44231273, 20.02721472), (38.77962523, 17.27700858), (37.65305648, 14.72571472))
    curveto((37.55365336, 14.02990345), (38.08379275, 13.566001), (38.64708773, 13.566001))
    curveto((38.9452865, 13.566001), (39.24350648, 13.73168347), (39.44231273, 14.096151))
    curveto((40.5357365, 16.8794385), (41.198424, 19.82834486), (41.198424, 22.81054464))
    curveto((41.198424, 31.1934885), (32.38478628, 36.99205714), (32.38478628, 45.34191964))

if True:
    # box englobante
    turtle.color("green")
    q4 = q4[0], q4[1] + d
    moveto(*q1)
    turtle.dot(5, "green")
    moveto(*q2)
    turtle.dot(5, "green")
    moveto(*q3)
    turtle.dot(5, "green")
    moveto(*q4)
    turtle.dot(5, "green")
    roundedrect((q1[0], q2[1]), (q3[0], q4[1]), 0)

    print(f"largeur:        {(q3[0]-q1[0])*scale:7.3f}")
    print(f"hauteur:        {(q4[1]-q2[1])*scale:7.3f}")

# mire de vérification repère orthogonal
mire(q1[0] + 5, q4[1] - 10, 5)

# sauvegarde de l'image
ts = turtle.getscreen()
ts.getcanvas().postscript(file="croche.eps", height=297 / 210 * 600, width=600)

# clic de fermeture
screen = turtle.Screen()
screen.exitonclick()
