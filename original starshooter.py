import math
from turtle import *
from random import *

#Set up play area
screen = Screen()
screen.setup(600,600)
screen.tracer(0,0)#disables autoupdate of the screen


#Draw random stars on the background
screen.bgcolor("black")
starTurtle = Turtle()
starTurtle.color("white")
starTurtle.penup()
for i in range(500):
  starTurtle.goto(randint(-600,600),randint(-600,600))
  starTurtle.pendown()
  starTurtle.dot()
  starTurtle.penup()
starTurtle.hideturtle()

#Add shapes
screen.register_shape("player",((0,0),(5,-10),(15,-10),(0,20),(-15,-10),(-5,-10)))
screen.register_shape("bullet",((-5,-5),(-5,5),(5,5),(5,-5)))
screen.register_shape("rocket",((0,20),(-10,0),(0,-10),(10,0)))

#Declare Objects
class Player(Turtle):
  def __init__(self,x,y):
    Turtle.__init__(self)
    self.x = x
    self.y = y
    self.penup()
    self.shape("player")
    self.color("blue")
    self.goto(x,y)
    self.direction = 0.0
    self.radius = 20
    self.isMoving = False
    self.speed = 0
    self.dead = False
    
  def enemyShip(self):
    self.shape("rocket")
    
  def antiClock(self):
    temp = self.direction
    self.direction = temp - 10
    self.setheading(self.direction)
    
  def move(self):
    self.isMoving = True
    self.speed = 0.75
    
  def kill(self):
    self.dead = True
    self.color("#da190b")
    self.speed = 0
    self.clear()
    
  def isDead(self):
    return self.dead
    

class Bullet(Turtle):
  def __init__(self,x,y):
    Turtle.__init__(self)
    self.x = x
    self.y = y
    self.penup()
    self.color("yellow")
    self.shape("bullet")
    self.goto(x,y)
    self.speed = 0 
    self.fired = False
    self.radius = 5
    
    
  def moveForward(self):
    self.speed = 10
    self.fired = True
  
  def isFired(self):
    return self.fired

#Create Player
mainPlayer = Player(-10,0)

#Create Ammo
magazine = []
round = 0
for i in range(0,10):
  bullet = Bullet(-10,0)
  magazine.append(bullet)


#Create Enemies

enemies = []

for i in range (1,30):
  enemy = Player(0,0)
  enemy.enemyShip()
  enemy.color("purple")
  randomplace = randint(1,360)
  enemy.setheading(randomplace)
  enemy.back(300 * i)
  enemy.move()
  enemies.append(enemy)

#Set Controls

def clockwise():
  mainPlayer.setheading(mainPlayer.heading()-10)
  for item in magazine:
    if(item.isFired()==False):
      item.setheading(item.heading()-10)

def anticlockwise():
  mainPlayer.setheading(mainPlayer.heading()+10)
  for item in magazine:
    if(item.isFired()==False):
      item.setheading(item.heading()+10)
      
def forward():
  mainPlayer.forward(5)
  for item in magazine:
    item.forward(5)

#Selects bullet to fire
def fire_bullet():
  global round
  
  if round < len(magazine):
    currentBullet = magazine[round]
    currentBullet.moveForward()
    round += 1 #moves pointer to next bullet ready to fire
    


  


#moves a bullet forward if fired
def update_bullet():
  for item in magazine:
    if(item.isFired()==True):
      item.forward(item.speed)

def update_enemy():
  for item in enemies:
    if(item.isMoving==True):
      destination_x = mainPlayer.xcor()
      origin_x = item.xcor()
      destination_y = mainPlayer.ycor()
      origin_y = item.ycor()
      deltaX = destination_x - origin_x
      deltaY = destination_y - origin_y
      degrees_temp = math.atan2(deltaX, deltaY)/math.pi*180
      degrees_final = 0
      
      if degrees_temp < 0:
        degrees_final = 360 + degrees_temp
      else:
        degrees_final = degrees_temp
        
      item.setheading(item.towards( destination_x,destination_y))  
      item.forward(item.speed)

#Assign keys to functions

screen.onkey(clockwise, "right")
screen.onkey(anticlockwise, "left")
screen.onkey(fire_bullet,"space")
screen.onkey(forward,"up")
screen.listen()


#Create game checks

def collision(item1,item2):
  x_distance = abs(item1.xcor() - item2.xcor())
  y_distance = abs(item1.ycor() - item2.ycor())
  overlap_horizontally = (item1.radius + 5 >= x_distance)  # either True or False
  overlap_vertically   = (item1.radius + 5 >= y_distance)  # either True or False
  return overlap_horizontally and overlap_vertically 

def destroy_ship(ship):
  for item in magazine:
    if collision(ship,item) and item.isFired() and ship.isDead() == False:
      ship.kill()
      item.color("white")
      item.goto(-50000,0)
      item.speed = 0
      

def destroyed_ships():
  for ship in enemies:
    if ship.isDead():
      ship.color = "white"
      ship.goto(-50000,0)

def ship_collision():
  for ship in enemies:
    if collision(mainPlayer, ship):
      mainPlayer.kill()
      explosion = Turtle()
      explosion.penup()
      explosion.goto(mainPlayer)
      explosion.color("Orange")
      explosion.dot(50)


def game_over():
  return mainPlayer.isDead()
    
#Set step by step functions to run

def frame () :
    
    if game_over() == False:
      destroyed_ships()
      update_enemy()
      for e in enemies:
        destroy_ship(e)
      update_bullet()
      ship_collision()
      screen.update()  # show the new frame
      screen.ontimer(frame, framerate_ms)
    else:
      sorry = Turtle()
      sorry.hideturtle()
      sorry.penup()
      sorry.color("White")
      sorry.goto(0,100)
      sorry.write("Game Over", align="center", font = ("Arial", 32, "bold", "white"))
      screen.update()
    
    
    

#Set how often the game updates

framerate_ms = 0  # Every how many milliseconds must screen call frame function?
frame()
