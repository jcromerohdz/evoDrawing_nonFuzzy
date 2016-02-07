import os
import time




def task(action='start'):
	s = 0
	m = 0 
	h = 0

	while s<= 60 or action=='start':
		#os.system('cls')
		print h, 'Hours', m, 'Minutes', s, 'Secounds'
		time.sleep(1)
		s+=1
		if s == 60:
			m+= 1
			s= 0
		elif m == 60:
			h+=1
			m=0
			s=0
		elif action == 'stop':
			s=s
			m=m
			h=h
			break

	print  h, ' :', m, ' :', s, ' :'		
