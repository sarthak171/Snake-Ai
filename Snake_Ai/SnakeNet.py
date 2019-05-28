import numpy as np
import random

def sigmoid(x):
	return 1.0/(1.+np.exp(-x))
def apply_bias(array,bias):
	for x in range(0,len(bias)):
		array[x]-=bias[x][0]
	return array
def mutate(array,mutate_rate):
	shape = array.shape
	for x in range(0,shape[0]):
		for y in range(0,shape[1]):
			if(abs(np.random.rand(1,1))>mutate_rate):
				array[x][y]=random.gauss(array[x][y],1)
				if(array[x][y]>=1): array[x][y] = 1
				elif(array[x][y]<=-1): array[x][y] = -1
	return array
	
class SnakeNet:
	def __init__(self,inputN,hiddenN1,hiddenN2,outputN):
		self.inputN = inputN
		self.hiddenN1 = hiddenN1
		self.hiddenN2 = hiddenN2
		self.outputN = outputN
		self.weights1 = np.random.rand(inputN,hiddenN1)
		self.weights2 = np.random.rand(hiddenN1,hiddenN2)
		self.weights3 = np.random.rand(hiddenN2,outputN)
		self.bias1  = np.ones((inputN,1))
		self.bias2 = np.ones((hiddenN1,1))
	def feed_forward(self,input_arr):
		self.hidden_nodes1 = sigmoid(np.dot(apply_bias(input_arr,self.bias1),self.weights1))
		#print(self.hidden_nodes1.shape)
		self.hidden_nodes2 = sigmoid(np.dot(apply_bias(self.hidden_nodes1,self.bias2),self.weights2))
		self.output = sigmoid(np.dot(self.hidden_nodes2,self.weights3))
		#print(self.output)
		return self.output
	def mutate(self):
		self.weights1 = mutate(self.weights1,.1)
		self.weights2 = mutate(self.weights2,.1)
		self.weights3 = mutate(self.weights3,.1)
		#self.bias1 = mutate(self.bias1,.5)
		#self.bias2 = mutate(self.bias2,.5)
	def crossover(self,partner):
		child = SnakeNet(self.inputN,self.hiddenN1,self.hiddenN2,self.outputN)
		randC = random.randint(0,partner.weights1.shape[0])
		randR = random.randint(0,partner.weights1.shape[1])
		for i in range (0,partner.weights1.shape[0]):
			for j in range(0,partner.weights1.shape[1]):
				if(i<randR or (i == randR and j <= randC)):
					child.weights1[i][j]=self.weights1[i][j]
				else:
					child.weights1[i][j]=partner.weights1[i][j]
		randC = random.randint(0,partner.weights2.shape[0])
		randR = random.randint(0,partner.weights2.shape[1])
		for i in range (0,partner.weights2.shape[0]):
			for j in range(0,partner.weights2.shape[1]):
				if(i<randR or (i == randR and j <= randC)):
					child.weights2[i][j]=self.weights2[i][j]
				else:
					child.weights2[i][j]=partner.weights2[i][j]
		randC = random.randint(0,partner.weights3.shape[0])
		randR = random.randint(0,partner.weights3.shape[1])
		for i in range (0,partner.weights3.shape[0]):
			for j in range(0,partner.weights3.shape[1]):
				if(i<randR or (i == randR and j <= randC)):
					child.weights3[i][j]=self.weights3[i][j]
				else:
					child.weights3[i][j]=partner.weights3[i][j]
		return child




















