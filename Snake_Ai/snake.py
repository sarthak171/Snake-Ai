import pygame as pg
from pygame.locals import *
import random as rand
import math
import food
import player
import population


#just python and pygame things


pg.init()
gameDisplay = pg.display.set_mode((500,500),pg.RESIZABLE)
gameDisplay.fill((0,0,0))
clock = pg.time.Clock()
end = False

#instantiate an initial "best snake" a list of populations and some other stuff
species = []
snake = player.player(food.food())

cnt = 0
i = 0
pop = population.population(500,snake) #create a population size 500
species.append(pop)
best = species[i].best_snake
while not end:
	for event in pg.event.get(): #pygame code to end program when x button pressed
	    if event.type == pg.QUIT:
	        end = True
	keys = pg.key.get_pressed()
	if(species[i].end()): #if all members of population ded
		species[i].calc_fitness() #calc fitness of all members of population
		species[i].naturalSelection() #update population with new snakes
		if(best == species[i].best_snake):
			cnt+=1
			print(cnt)
		else:
			best = species[i].best_snake
			cnt = 0
			print("K")
		if(cnt>=5):
			species[i].best_fitness = 0
			#species[i].goal = food.food()
	#if not snake.alive or keys[K_r]:
	#	snake.redo()
	gameDisplay.fill((0,0,0))
	#snake.foodCol()
	#snake.updateOld()
	species[i].move_population() #move population
	#for x in range(0,10):
	#	species[i].players[x].draw(gameDisplay)
	#	species[i].players[x].drawG(gameDisplay)

	for snakes in species[i].players: #draw all members of population
		snakes.draw(gameDisplay)
		#snakes.drawG(gameDisplay)
	species[i].best_snake_clone.drawF(gameDisplay) #draw best member of population
	pg.display.update()
	clock.tick(20)
pg.quit()
quit()


#code that does runs a single snake no population for debug purposes
'''



import pygame as pg
from pygame.locals import *
import random as rand
import math
import food
import player
import population



species = []

pg.init()
gameDisplay = pg.display.set_mode((500,500),pg.RESIZABLE)
gameDisplay.fill((0,0,0))
clock = pg.time.Clock()
end = False
snake = player.player()
cnt = 0
i = 0
#pop = population.population(1,snake)
#species.append(pop)
while not end:
	for event in pg.event.get():
	    if event.type == pg.QUIT:
	        end = True
	keys = pg.key.get_pressed()
	#if(species[i].end()):
	#	species[i].calc_fitness()
	#	species[i].naturalSelection()
	if not snake.alive or keys[K_r]:
		snake = player.player()
	gameDisplay.fill((0,0,0))
	snake.move()
	snake.draw(gameDisplay)
	#snake.foodCol()
	#snake.updateOld()
	#species[i].move_population()
	#for snakes in species[i].players:
	#	snakes.draw(gameDisplay)
	#species[i].players[0].drawF(gameDisplay)
	pg.display.update()
	clock.tick(20)
pg.quit()
quit()


'''