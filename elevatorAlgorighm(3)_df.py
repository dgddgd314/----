import numpy as np
import copy
import random
import pandas as pd

class Person:
	def __init__(self, disk_size):
		self.disk_size = disk_size
		self.dest = self.start_distribution()
		self.mode = 0

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
		return np.random.randint(1, self.disk_size, size=1)[0] #random, 출근길
		#return 1 # 퇴근길

	def end_distribution(self):
		#return np.random.randint(1, self.disk_size, size=1)[0] #random, 퇴근길
		return 1 #출근길

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
	tick = 1
	ticking = tick
	sumdistance = 0
	cnt = 0
 
	for i in range(1, cycle):  # 10000 사이클 회전
		if ticking >= 0:
			ticking -= 1;
			sumdistance += distance

		if ticking == 0:
			addPerson(arr, sumdistance, disk_size, personperRTT=personperRTT)

		left = []
		right = []
		now = []
  
		if ticking == -1:
			addPerson(arr, distance, disk_size, personperRTT=personperRTT)
  
		#print(head, "start\n")

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
		"""
		for person in left: print(person)
		print("/")
		for person in now : print(person)
		print("/")
		for person in right : print(person)
		"""
  
		if len(left) == 0:
			direction = "right"

		if len(right) == 0:
			direction = "left"
   
		if waitingpeople == 0:
			#print("pass due to no calling/", i, "turn\n")
			distance = 2
			if ticking == -1:
				ticking = tick
				cnt += 1
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
		#print(direction, "start", head, "goto", goto, "changed into", cur_people, i, "turn" "\n")
		head = (int) (goto.dest)
	"""
	print("total move: ", total_move)
	print("total people: ",total_people)
	print("total people waiting move: ", total_people_waiting_move)
	print("total people move in elevator: ", total_people_move)
	print("\nelectric Efficiency (ppl/move):", total_people/total_move, "needed elevator move per 1 person: ",total_move/total_people)
	print("electric Efficiency (ttl ppl move/ttl move): ",total_people_move/total_move)
	print("\ntime efficiency (ATT/total time): ",total_people_move/total_people_waiting_move)
	print("average waiting time (ATT+AWT):", total_people_waiting_move/total_people)
 
	print(cnt)
	"""
	return [personperRTT,total_move, total_people, total_people_waiting_move, total_people_move, total_people/total_move, total_move/total_people, total_people_move/total_move, total_people_move/total_people_waiting_move, total_people_waiting_move/total_people, total_people_move/total_people]
 

# Driver code


df = pd.DataFrame(columns = ['personperRTT','tm', 'tp', 'tpwm', 'tpmie', 'ppl/move', 'move per 1p','tpm/move', 'ATT/tt', 'ATT+AWT', 'ATT'])
dftm = pd.DataFrame(columns = ['personperRTT', '5','7','10','12','15','17','20','22','25','27','30','32','35','37','40','42','45','47','50'])
dftp = pd.DataFrame(columns = ['personperRTT', '5','7','10','12','15','17','20','22','25','27','30','32','35','37','40','42','45','47','50'])
dftpwm = pd.DataFrame(columns = ['personperRTT', '5','7','10','12','15','17','20','22','25','27','30','32','35','37','40','42','45','47','50'])
dftpmie = pd.DataFrame(columns = ['personperRTT', '5','7','10','12','15','17','20','22','25','27','30','32','35','37','40','42','45','47','50'])
dfpplmove = pd.DataFrame(columns = ['personperRTT', '5','7','10','12','15','17','20','22','25','27','30','32','35','37','40','42','45','47','50'])
dfmoveper1p = pd.DataFrame(columns = ['personperRTT', '5','7','10','12','15','17','20','22','25','27','30','32','35','37','40','42','45','47','50'])
dftpmmove = pd.DataFrame(columns = ['personperRTT', '5','7','10','12','15','17','20','22','25','27','30','32','35','37','40','42','45','47','50'])
dfATTtt = pd.DataFrame(columns = ['personperRTT', '5','7','10','12','15','17','20','22','25','27','30','32','35','37','40','42','45','47','50'])
dfATTAWT = pd.DataFrame(columns = ['personperRTT', '5','7','10','12','15','17','20','22','25','27','30','32','35','37','40','42','45','47','50'])
dfATT = pd.DataFrame(columns = ['personperRTT', '5','7','10','12','15','17','20','22','25','27','30','32','35','37','40','42','45','47','50'])
my_list = []

for i in range(2, 151, 2): #0.2~15.0 까지
	my_list.append(i / 10)

dftm['personperRTT'] = my_list
dftp['personperRTT'] = my_list
dftpwm['personperRTT'] = my_list
dftpmie['personperRTT'] = my_list
dfpplmove['personperRTT'] = my_list
dfmoveper1p['personperRTT'] = my_list
dftpmmove['personperRTT'] = my_list
dfATTtt['personperRTT'] = my_list
dfATTAWT['personperRTT'] = my_list
dfATT['personperRTT'] = my_list

for i in [5,7,10,12,15,17,20,22,25,27,30,32,35,37,40,42,45,47,50]:
	for j in my_list:
		df = df.append(pd.Series(SCAN(i,j), index = df.columns), ignore_index = True)
		print("SCAN(",i,",",j,") is done!")

	dftm[(str)(i)] = df['tm'] 
	dftp[(str)(i)] = df['tp']
	dftpwm[(str)(i)] = df['tpwm']
	dftpmie[(str)(i)] = df['tpmie']
	dfpplmove[(str)(i)] = df['ppl/move']
	dfmoveper1p[(str)(i)] = df['move per 1p']
	dftpmmove[(str)(i)] = df['tpm/move']
	dfATTtt[(str)(i)] = df['ATT/tt']
	dfATTAWT[(str)(i)] = df['ATT+AWT']
	dfATT[(str)(i)] = df['ATT']

	df = pd.DataFrame(columns = ['personperRTT','tm', 'tp', 'tpwm', 'tpmie', 'ppl/move', 'move per 1p','tpm/move', 'ATT/tt', 'ATT+AWT', 'ATT'])

dftm.to_csv('1.csv', index = False)
dftp.to_csv('2.csv', index = False)
dftpwm.to_csv('elevatorAlgorithm SCAN([5~50], [0.2~15.0], tpwm).csv', index = False)
dftpmie.to_csv('elevatorAlgorithm SCAN([5~50], [0.2~15.0], tpmie).csv', index = False)
dfpplmove.to_csv('elevatorAlgorithm SCAN([5~50], [0.2~15.0], pplpermove).csv', index = False)
dfmoveper1p.to_csv('elevatorAlgorithm SCAN([5~50], [0.2~15.0], move per 1p).csv', index = False)
dftpmmove.to_csv('elevatorAlgorithm SCAN([5~50], [0.2~15.0], tpmpermove).csv', index = False)
dfATTtt.to_csv('elevatorAlgorithm SCAN([5~50], [0.2~15.0], ATTpertt).csv', index = False)
dfATTAWT.to_csv('elevatorAlgorithm SCAN([5~50], [0.2~15.0], ATT+AWT).csv', index = False)
dfATT.to_csv('elevatorAlgorithm SCAN([5~50], [0.2~15.0], ATT).csv', index = False)

print(dftm)
print("download complete!")