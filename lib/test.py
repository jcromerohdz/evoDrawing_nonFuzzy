from userFitnessFuzzyRules import fisuser




sample = {'sample': [{'fitness': {'DefaultContext': 0, '1:01': '2', '2:02': '3', '3:03': '4', '4:04': '3', '5:05': '5'}}]}
					 #{'fitness': {'DefaultContext': 0, '5:06': '2', '7:07': '3', '8:08': '4', '9:09': '4', '10:010': '4'}}
					 #{'fitness': {'DefaultContext': 0, '11:01': '2', '12:02': '3', '13:03': '4', '14:04': '3', '15:05': '5'}},
					 #{'fitness': {'DefaultContext': 0, '16:01': '2', '17:02': '3', '18:03': '4', '19:04': '3', '20:05': '5'}},
					 #{'fitness': {'DefaultContext': 0, '21:01': '2', '22:02': '3', '23:03': '4', '24:04': '3', '25:05': '5'}}]}


usersample = {'experience': {'1': '30', '2': '45', '3': '25', '4': '57', '5': '80'}}
					 #{'experience': {'5': '2', '7': '3', '8': '4', '9': '4', '10': '4'}}
					 #{'experience': {'11': '2', '12': '3', '13': '4', '14': '3', '15': '5'}},
					 #{'experience': {'16': '2', '17': '3', '18': '4', '19': '3', '20': '5'}},
					 #{'experience': {'21': '2', '22': '3', '23': '4', '24': '3', '25': '5'}}]}



def fuzzy_fitness(fitness):

	rate_by_fuzzy=[]
	fuzzy=[]	
	for u  in fitness:
		if u != "DefaultContext":
			usr, usr_date = u.split(":")
			exp = int(usersample['experience'][usr])
			rate = int(fitness[u])
			print str(rate) +" , " + str(exp)
			
			rate_by_fuzzy.append(rate * fisuser(rate,exp))
			fuzzy.append(fisuser(rate,exp))

	fuzzy_ponderation = sum(rate_by_fuzzy)/sum(fuzzy)


	print rate_by_fuzzy
	print sum(rate_by_fuzzy)
	print fuzzy
	print sum(fuzzy)		
	print fuzzy_ponderation		







fuzzy_fitness(sample['sample'][0]['fitness'])