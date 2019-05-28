import player
import random
import pygame as pg
from pygame.locals import *
import math
import food
import player


class population:
	#instantiate variables
	def __init__(self,size,best):
		self.best_snake = best
		self.best_snake_clone = best
		self.best_snake_score = 0
		self.gen = 0
		self.samebest = 0
		self.best_fitness = 0
		self.fitness_sum = 0
		self.players = []
		self.goal = food.food()
		for i in range(0,size):
			self.players.append(player.player(self.goal.clone()))
	#move population 0.o
	def move_population(self):
		for snake in self.players:
			if(snake.alive):
				snake.move()
		if(self.best_snake_clone.alive):
			self.best_snake_clone.move()
	#check if any snake is still alive
	def end(self):
		for snake in self.players:
			if(snake.alive or self.best_snake_clone.alive):
				return False
		return True
	#calculate the fitness of each snake in population
	def calc_fitness(self):
		for snake in self.players:
			snake.calcFitness()
			#print(snake.fitness)
	#change the weights and biases of brain of snake
	def mutate(self):
		for snake in self.players:
			snake.brain.mutate()
	#snake with best fitness becomes best snake
	def setBestSnake(self):
		maxFitness = 0
		maxIndex = 0
		for i in range(0,len(self.players)):
			if(self.players[i].fitness>maxFitness):
				maxFitness = self.players[i].fitness
				maxIndex = i
		if(maxFitness>self.best_fitness):
			self.best_fitness = maxFitness
			self.best_snake = self.players[maxIndex].clone()
	#a helper function used to select snakes
	def calcFitnessSum(self):
		self.fitness_sum = 0
		for snake in self.players:
			self.fitness_sum+=snake.fitness
	#select some of the best snakes from the previous population but not the best (prob needs to be fixed)
	def pickSnake(self):
		rand = math.floor(random.randint(0,self.fitness_sum))
		runningSum = 0
		for snake in self.players:
			runningSum+=snake.fitness
			if(runningSum>rand):
				return snake
		return self.players[0]
	#breed new snakes by setting the best snake from the last population and good snakes from the population
	
	def pickSnake2(self):
		maxLength = 0
		maxTime = 0
		maxIndexL = 0
		maxIndexT = 0
		for i in range(0,len(self.players)):
			if(maxLength>self.players[i].tail):
				maxIndexL = i
				maxLength = self.players[i].tail
			if(maxTime>self.players[i].lifeLeft):
				maxTime = self.players[i].lifeLeft
				maxIndexT = i
		return self.players[maxIndexL],self.players[maxIndexT]
	
	def naturalSelection(self):
		newPlayers = []
		self.setBestSnake()
		self.calcFitnessSum()
		self.best_snake_clone = self.best_snake.clone()
		self.best_snake_clone.redo()
		newPlayers.append(self.best_snake.clone())
		newPlayers[0].redo()
		for i in range(1,len(self.players)):
			#newPlayers.append(self.pickSnake().crossover(self.pickSnake()))
			newPlayers.append(self.pickSnake().crossover(self.pickSnake()))
			newPlayers[i].brain.mutate()
			newPlayers[i].redo()
			#i+=1
			#newPlayers.append(player.player())
		self.players.clear()
		self.players = newPlayers