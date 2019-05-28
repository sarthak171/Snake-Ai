import pygame as pg
from pygame.locals import *
import random as rand
import math
import player
from copy import deepcopy

class food:
	x = 0
	y = 0
	xarr = []
	yarr = []
	cnt = 0
	def __init__(self):
		self.x = int(rand.random()*500)
		self.y = int(rand.random()*500)
		self.cnt = 0
		self.xarr.append(self.x)
		self.yarr.append(self.y)
		for i in range(0,100):
			self.xarr.append(int(rand.random()*500))
			self.yarr.append(int(rand.random()*500))
		#self.x = 400
		#self.y = 250
	def draw(self,surface):
		pg.draw.circle(surface,(0,255,0),(self.x,self.y),10)
	def drawF(self,surface):
		pg.draw.circle(surface,(0,0,255),(self.x,self.y),10)
	def next(self):
		self.cnt+=1
		self.x = self.xarr[self.cnt]
		self.y = self.yarr[self.cnt]
	def reset(self):
		self.cnt = 0
		self.x = self.xarr[self.cnt]
		self.y = self.yarr[self.cnt]
	def clone(self):
		#self.goal = food.food()
		return deepcopy(self)
