import pygame as pg
from pygame.locals import *
import random as rand
import math
import food
import SnakeNet
import population
from copy import deepcopy

class player:
	def __init__(self,food):
		self.x = [250,240,230,220]
		self.y = [250,250,250,250]
		self.lifeLeft = 200
		self.lifetime = 0
		self.tail = 4
		self.speed = 15
		self.ang = 0
		self.direction = 100
		self.inputs = []
		self.outputs = []
		self.fitness = 0
		self.growCount = 0
		self.alive = True
		self.goal_cnt = 0
		self.goal = food
		#self.goal = food.food()
		self.brain = SnakeNet.SnakeNet(24,18,18,4)
	def redo(self):
		#self.brain.mutate()
		self.goal.reset()
		self.x = [250,240,230,220]
		self.y = [250,250,250,250]
		self.lifeLeft = 200
		self.lifetime = 0
		self.tail = 4
		self.speed = 15
		#self.direction = 2
		self.inputs = []
		self.outputs = []
		self.fitness = 0
		self.growCount = 0
		self.alive = True
		self.goal_cnt = 0
		#self.goal = food.food()
	def mutate(self):
		self.brain.mutate()
	def checkBorderCol(self):
		check = False
		if(self.x[0]<=0):	    
		    check = True
		elif(self.x[0]+10>=505):    
		    check = True
		elif(self.y[0]<=0):
		    check = True
		elif(self.y[0]+10>=505):
		    check = True
		return check
	def foodCol(self):
		if(math.sqrt((self.goal.y-self.y[0])**2+(self.goal.x-self.x[0])**2)<=20):
			self.x.append(self.x[self.tail-1])
			self.y.append(self.y[self.tail-1])
			self.tail +=1
			self.goal_cnt +=1
			self.goal.next()
			self.lifeLeft +=100
			return self.goal
		return False
	def checkSelfCol(self,position,x_thing):
		for t in range(x_thing,self.tail):
			if(math.sqrt((self.y[t]-position[1])**2+(self.x[t]-position[0])**2)<=10):
				return True
		return False
	def moveRight(self):
		self.x[0] = self.x[0] -self.speed
		self.ang=0
		self.direction = 1
	def moveLeft(self):
		self.x[0] = self.x[0] + self.speed
		self.ang=180
		self.direction = 2
	def moveUp(self):
		self.y[0] = self.y[0] - self.speed
		self.ang=90
		self.direction = 3
	def moveDown(self):
		self.y[0] = self.y[0] +self.speed
		self.ang=270
		self.direction = 0
	def updateOld(self):
		i = self.tail-1
		while i > 0:
			self.x[i] = self.x[i-1]
			self.y[i] = self.y[i-1]
			i-=1
	def crossover(self,partner):
		child = player(self.goal)
		child.brain = self.brain.crossover(partner.brain)
		return child
	def Brain_Decision(self):
		self.outputs = self.brain.feed_forward(self.inputs)
		max_output = 0
		max_index = 0
		for i in range(0,self.outputs.shape[0]):
			if(max_output<self.outputs[i]):
				max_output=self.outputs[i]
				max_index = i
		#print(max_index)
		if(max_index==1):
			if self.direction == 2:
				#self.alive = False
				self.moveLeft()
			else:
				self.moveRight()
		elif(max_index==2):
			if self.direction ==1:
				#self.alive = False
				self.moveRight()
			else:
				self.moveLeft()
		elif(max_index==3):
			if self.direction==0:
				#self.alive = False
				self.moveDown()
			else:
				self.moveUp()
		elif(max_index==0):
			if(self.direction==3):
				#self.alive = False
				self.moveUp()
			else:
				self.moveDown()
	def move(self):
		self.lifetime+=1
		self.lifeLeft-=1
		if(self.lifeLeft<0):
			self.alive = False
		if(self.checkBorderCol() or self.checkSelfCol((self.x[0],self.y[0]),3)):
			self.alive = False
		self.foodCol()
		self.updateOld()
		self.update_inputs()
		self.Brain_Decision()
		#self.calcFitness()
		#print(self.fitness)
	def calcFitness(self):
		if(self.tail <10):
			self.fitness = math.floor(self.lifetime*self.lifetime*math.pow(2,(math.floor(self.tail))))
		else:
			self.fitness = self.lifetime*self.lifetime
			self.fitness *= pow(2,10)
			self.fitness *= (self.tail-9)
	def draw(self,surface):
		#self.goal.draw(surface)
		for i in range(self.tail):
			pg.draw.circle(surface,(255,0,0),(self.x[i],self.y[i]),10)
	def drawG(self,surface):
		self.goal.draw(surface)
	def drawF(self,surface):
		self.goal.drawF(surface)
		for i in range(self.tail):
			pg.draw.circle(surface,(0,0,255),(self.x[i],self.y[i]),10)
	def clone(self):
		#self.goal = food.food()
		return deepcopy(self)
	def look_direction(self,ang):
		food_found = False
		tail_found = False
		distance = 1
		vision = [0,0,0]
		position = []
		position.append(self.x[0])
		position.append(self.y[0])
		while(not ((position[0]<=10) or (position[0]+10>=500) or (position[1]<=10) or (position[1]+10>=500))):
			if(not food_found and math.sqrt((self.goal.y-position[1])**2+(self.goal.x-position[0])**2)<=20):
				#if(self.ang<ang-90 or self.ang>ang+90):
				#	vision[0] = -1
				#else:
				vision[0] = 1
				food_found = True
				#print("FOUND FOOD",ang)
			if(not tail_found and self.checkSelfCol(position,3)):
				vision[1] = 1
				tail_found = True
				#print("FOUND TAIL",ang)
			distance+=15
			position[0] = 15*math.cos(math.radians(ang))+position[0]
			position[1] = 15*math.sin(math.radians(ang))+position[1]
		vision[2] = 1/(distance)
		#print("found_wal",ang)
		return vision
	def update_inputs(self):
		self.inputs.clear()
		temp = self.look_direction(self.ang)
		self.inputs.append(temp[0])
		self.inputs.append(temp[1])
		self.inputs.append(temp[2])

		temp = self.look_direction((self.ang+45)%360)
		self.inputs.append(temp[0])
		self.inputs.append(temp[1])
		self.inputs.append(temp[2])

		temp = self.look_direction((self.ang+90)%360)
		self.inputs.append(temp[0])
		self.inputs.append(temp[1])
		self.inputs.append(temp[2])

		temp = self.look_direction((self.ang+135)%360)
		self.inputs.append(temp[0])
		self.inputs.append(temp[1])
		self.inputs.append(temp[2])

		temp = self.look_direction((self.ang+180)%360)
		self.inputs.append(temp[0])
		self.inputs.append(temp[1])
		self.inputs.append(temp[2])

		temp = self.look_direction((self.ang+225)%360)
		self.inputs.append(temp[0])
		self.inputs.append(temp[1])
		self.inputs.append(temp[2])

		temp = self.look_direction((self.ang+270)%360)
		self.inputs.append(temp[0])
		self.inputs.append(temp[1])
		self.inputs.append(temp[2])

		temp = self.look_direction((self.ang+315)%360)
		self.inputs.append(temp[0])
		self.inputs.append(temp[1])
		self.inputs.append(temp[2])

