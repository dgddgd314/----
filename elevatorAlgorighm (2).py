import numpy as np
import copy
import random
import pandas as pd

class Person:
	def __init__(self, disk_size):
		self.dest = self.start_distribution()
		self.mode = 0
		self.disk_size = disk_size

	def __sub__(self, other):
		if isinstance(other, Person):
			return self.dest - other.dest
		elif isinstance(other, int):
			return self.dest - other
		else:
			raise TypeError("Unsupported operand type")

	def __gt__(self, other):
		if isinstance(other, Person):
			return self.dest > other.dest
		elif isinstance(other, int):
			return self.dest > other
		else:
			raise TypeError("Unsupported operand type")

	def __lt__(self, other):
		if isinstance(other, Person):
			return self.dest < other.dest
		elif isinstance(other, int):
			return self.dest < other
		else:
			raise TypeError("Unsupported operand type")

	def __eq__(self, other):
		if isinstance(other, Person):
			return self.dest == other.dest
		elif isinstance(other, int):
			return self.dest == other
		else:
			raise TypeError("Unsupported operand type")

	def __str__(self):
		return f"Dest({self.dest}), Mode({self.mode})/"

	def start_distribution(self):
		#return np.random.randint(1, self.disk_size, size=1)[0] #random, 출근길
		return 1 # 퇴근길

	def end_distribution(self):
		return np.random.randint(1, self.disk_size, size=1)[0] #random, 퇴근길
		#return 1 #출근길

	def changeMode(self):
		start = self.dest
		self.dest = self.end_distribution()
		self.mode = 1
		return abs(start-self.dest)


	def isItEnd(self):
		return self.mode

def sort_key(person):
	return person.dest

def addPerson(arr, distance, disk_size, personperRTT):
	maxperson = 100  # 한 번에 최대로 탈 수 있는 인원
	personperRTT = 15   # RTT (한 번 엘레베이터가 회전하는 데 걸리는 시간) 동안 타는 평균 사람 수. 한가할 때 낮고, 바쁠 때는 매우 높다.
	probability = personperRTT*(distance/200)/maxperson   # 0.3 :
	for _ in range(maxperson): #한꺼번에 최대
		if random.random()<probability:
			arr.append(Person(disk_size))
		
def SCAN(disk_size = 40, personperRTT = 15):
	arr = [Person(disk_size=disk_size)]
	head = 1
	total_people = 0
	total_move = 0
	total_people_waiting_move = 0
	total_people_move = 0
	direction = "left"
	distance = 15
	cycle = 10000
	average = 1
 
	for i in range(1, cycle):  # 10000 사이클 회전
		left = []
		right = []
		now = []
  
		addPerson(arr, distance, disk_size, personperRTT=personperRTT)
  
		print(head, "start\n")

		for j in range(len(arr)):
			if arr[j] < head:
				left.append(arr[j])
			if arr[j] > head:
				right.append(arr[j])
			if arr[j] == head:
				now.append(arr[j])
	
		waitingpeople = len(left) + len(right) + len(now)

		left.sort(key=sort_key)
		right.sort(key=sort_key, reverse=True)

		for person in left: print(person)
		print("/")
		for person in now : print(person)
		print("/")
		for person in right : print(person)

		if len(left) == 0:
			direction = "right"

		if len(right) == 0:
			direction = "left"
   
		if waitingpeople == 0:
			print("pass due to no calling/", i, "turn\n")
			distance = 2
			goto = average
			total_move += abs(goto - average)
			continue


		if len(now) != 0:
			cur_people = now[-1]
			distance = 2
			if cur_people.isItEnd():
				total_people += 1
				now.pop()
				goto = copy.copy(cur_people)
			else:
				goto = copy.copy(cur_people)
				total_people_move += cur_people.changeMode()
	
		elif direction == "left":
			cur_people = left[-1] # 수정
			distance = abs(cur_people - head)
			total_people_waiting_move += distance * waitingpeople
			if cur_people.isItEnd():
				total_people += 1
				left.pop()
				goto = copy.copy(cur_people)
			else:
				goto = copy.copy(cur_people)
				total_people_move += cur_people.changeMode()

		elif direction == "right":
			cur_people = right[-1] # 수정
			distance = abs(cur_people - head)
			total_people_waiting_move += distance * waitingpeople
			if cur_people.isItEnd():
				total_people += 1
				right.pop()
				goto = copy.copy(cur_people)
			else:
				goto = copy.copy(cur_people)
				total_people_move += cur_people.changeMode()
	
		arr = left+right+now

		total_move += distance
		print(direction, "start", head, "goto", goto, "changed into", cur_people, i, "turn" "\n")
		head = (int) (goto.dest)
  
	print("total move: ", total_move)
	print("total people: ",total_people)
	print("total people waiting move: ", total_people_waiting_move)
	print("total people move in elevator: ", total_people_move)
	print("\nelectric Efficiency (ppl/move):", total_people/total_move, "needed elevator move per 1 person: ",total_move/total_people)
	print("electric Efficiency (ttl ppl move/ttl move): ",total_people_move/total_move)
	print("\ntime efficiency (ATT/total time): ",total_people_move/total_people_waiting_move)
	print("average waiting time (ATT+AWT):", total_people_waiting_move/total_people)
 

# Driver code


SCAN(40, 15) # 층수, 평균 몇 명의 사람이 탑승?
