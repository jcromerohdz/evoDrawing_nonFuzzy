def usr_last_date(fitness):
	print "CCCCCCCCFFFFFFFFF"
	print fitness
	current_date =[]

	fitness = fitness.keys()
	
	for d in fitness:
		if d !='DefaultContext':
			ud = d.split(':')
			print ud
			current_date.append(int(ud[1]))

	print current_date
	print max(current_date)
	result=max(current_date)
	
	print result

	return result		