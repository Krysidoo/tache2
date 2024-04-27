#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, GyroSensor, Port
from pybricks.parameters import Color
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from mindsensorsPYB import DIST_ToF

# Ici on associe la brique au nom ev3
ev3 = EV3Brick()
# Ici on va ajouter le gyroscope
gyro = GyroSensor(Port.S3)
corr= 2 # Correction à appliquer aux mesures du capteur de distance
# ici il s'agit des corrections qu'il y avait dans le fichier
# qui avait été donner au debut

# Maintenant on definie les moteur a leurs ports respectif
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# ici on definie les fonction avance et recule que l'on utilisera plus tard
def avance():
     left_motor.run(200)
     right_motor.run(200)

def recule():
     left_motor.run(-1000)
     right_motor.run(-1000)


# Ici on definie la fonction pour arrêter les moteurs
def stop():
    left_motor.stop()
    right_motor.stop()

#  Rotation dans le sens des aiguilles d'une montre
def aspin():
     left_motor.run(20)
     right_motor.run(-20)

# Rotation dans le sens inverse des aiguilles d'une montre
def aaspin():
     left_motor.run(-20)
     right_motor.run(20)
     
# ici on definie le systeme de scan, le robot analyse la zone
# si on ne vois rien ou que l'objet est trop proche on tourne !
# qu'on on trouve la cible on s'arrete.
def loop1():
     while True:
           #Ici on initialise le capteur pour voir la distance
           ToF = DIST_ToF(Port.S1,0x02)
           d= (DIST_ToF(Port.S1,0x02).readToFmm() - corr)
           print(d)
           #lorsqu'on ne vois rien on tourne
           if d>7000:
                aspin()
           #Si un objet est trop proche on tourne aussi
           elif d<=400:
                aspin()
           #Lorsqu'on vois l'objet on s'imobilise
           elif 400<d<=7000:
                break
# Ici on definie le systeme de detection de couleur, le robot analyse la couleur
# si la couleur est rouge on doit reculer
# si la couleur est verte on avance et on éloigne l'objet
def loop2():
     while True:
           # couleur est détectée par le capteur
           color = color_sensor.color()
           # Le robot avance vers l'objet qui est détecté
           avance()
           # On vérifie si la couleur détectée est du rouge
           if color == Color.RED:
            # Si c'est du rouge, le robot recule et recommence
                recule()
                wait(700)
                break
     
           # On Vérifie si la couleur détectée est du vert
           elif color == Color.GREEN:
                # Si c'est du vert, il ajuste sa position, amène l'objet très loin
                aspin()
                wait(1000)
                avance()
                wait(2000)
                aspin()
                wait(3000)
                avance()
                wait(30000)
          

# Caractéristique des roues (diametre et distance entre les deux)
diam=54.9 #diametre des roues
largeur=105 #distance entre les roues

# On définit les cararctéristiques du robot
robot = DriveBase(left_motor, right_motor, diam, largeur)

# On définit, dans l'ordre, la vitesse en mm/s, l'accélération en mm/s/s,
# la vitesse de rotation sur lui-même en deg/s, l'accélération de rotation en deg/s/s.
robot.settings(500, 50, 100, 20)

# Capteur de distance
ToF = DIST_ToF(Port.S1,0x02)
d= (DIST_ToF(Port.S1,0x02).readToFmm() - corr)
print(d)

# Le robot fait le loop pour s'orienter vers l'objet deux fois afin de minimiser les erreurs de capteurs
loop1()
stop()
wait(200)
avance()
wait(1000)
aspin()
wait(500)
loop1()

# defini le capteur de couleur sur le port 2
color_sensor = ColorSensor(Port.S2)

#Le robot fait le loop2 vu qu'il est orienté vers un objet.
loop2()

print("phase2")
#Le robot tourne afin de détecter deux fois le même objet
aaspin()
wait(2000)

#Il refait les deux loops pour arriver devant l'objet vert.
loop1()
stop()
wait(200)
loop2()
