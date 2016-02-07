__author__ = 'Jc Romero'

from FIS import *

preference = LinguisticVariable('preference', range=(0.0, 5.0))
preference.addMF('Low',MF.Triangular(-2, 1, 3))
preference.addMF('Mid',MF.Triangular(2.5, 3, 4.5))
preference.addMF('High',MF.Triangular(3, 5, 5))

activity = LinguisticVariable('experience', range=(0.0, 100.0))
activity.addMF('Low',MF.Triangular(1, 1, 50))
activity.addMF('Mid',MF.Triangular(30, 50, 70))
activity.addMF('High',MF.Triangular(50, 100, 100 ))

ranking = LinguisticVariable('ranking', range=(0.0, 30.0))
ranking.addMF('Low',MF.Triangular(1, 1, 30))
ranking.addMF('Mid',MF.Triangular(7.5, 15.5, 22.75))
ranking.addMF('High',MF.Triangular(15.5, 30, 30 ))

#OUT
Out = LinguisticVariable('fitness', type='out', range=(0.0, 100.0))
Out.addMF('Bad',MF.Triangular(-2, 1, 50))
Out.addMF('Normal',MF.Triangular(30, 50, 70))
Out.addMF('Good',MF.Triangular(50, 100, 100 ))




# Rules
#if preferance is low and activity is low then fitness is bad
r1 = FuzzyRule()
r1.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Low']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Low']),
								   FuzzyProposition(ranking,ranking.mfs['Low']))))	
	
r1.consequent.append(FuzzyProposition(Out,Out.mfs['Bad']))

#if preferance is low and activity is mid then fitness is bad
r2 = FuzzyRule()
r2.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Low']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Low']),
								   FuzzyProposition(ranking,ranking.mfs['Mid']))))	
	
r2.consequent.append(FuzzyProposition(Out,Out.mfs['Bad']))

#if preferance is low and activity is mid then fitness is bad
r3 = FuzzyRule()
r3.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Low']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Low']),
								   FuzzyProposition(ranking,ranking.mfs['High']))))	
	
r3.consequent.append(FuzzyProposition(Out,Out.mfs['Bad']))

#if preferance is low and activity is mid then fitness is bad
r4 = FuzzyRule()
r4.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Low']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Mid']),
								   FuzzyProposition(ranking,ranking.mfs['Low']))))	
	
r4.consequent.append(FuzzyProposition(Out,Out.mfs['Bad']))

#if preferance is low and activity is mid then fitness is bad
r5 = FuzzyRule()
r5.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Low']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Mid']),
								   FuzzyProposition(ranking,ranking.mfs['Mid']))))	
	
r5.consequent.append(FuzzyProposition(Out,Out.mfs['Bad']))

#if preferance is low and activity is mid then fitness is bad
r6 = FuzzyRule()
r6.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Low']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Mid']),
								   FuzzyProposition(ranking,ranking.mfs['High']))))	
	
r6.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r7 = FuzzyRule()
r7.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Low']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['High']),
								   FuzzyProposition(ranking,ranking.mfs['Low']))))	
	
r7.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r8 = FuzzyRule()
r8.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Low']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['High']),
								   FuzzyProposition(ranking,ranking.mfs['Mid']))))	
	
r8.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r9 = FuzzyRule()
r9.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Low']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['High']),
								   FuzzyProposition(ranking,ranking.mfs['High']))))	
	
r9.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r10 = FuzzyRule()
r10.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Mid']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Low']),
								   FuzzyProposition(ranking,ranking.mfs['Low']))))	
	
r10.consequent.append(FuzzyProposition(Out,Out.mfs['Bad']))

#if preferance is low and activity is mid then fitness is bad
r11 = FuzzyRule()
r11.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Mid']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Low']),
								   FuzzyProposition(ranking,ranking.mfs['Mid']))))	
	
r11.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r12 = FuzzyRule()
r12.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Mid']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Low']),
								   FuzzyProposition(ranking,ranking.mfs['High']))))	
	
r12.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r13 = FuzzyRule()
r13.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Mid']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Mid']),
								   FuzzyProposition(ranking,ranking.mfs['Low']))))	
	
r13.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r14 = FuzzyRule()
r14.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Mid']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Mid']),
								   FuzzyProposition(ranking,ranking.mfs['Mid']))))	
	
r14.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r15 = FuzzyRule()
r15.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Mid']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Mid']),
								   FuzzyProposition(ranking,ranking.mfs['High']))))	
	
r15.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r16 = FuzzyRule()
r16.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Mid']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['High']),
								   FuzzyProposition(ranking,ranking.mfs['Low']))))	
	
r16.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r17 = FuzzyRule()
r17.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Mid']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['High']),
								   FuzzyProposition(ranking,ranking.mfs['Mid']))))	
	
r17.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r18 = FuzzyRule()
r18.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['Mid']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['High']),
								   FuzzyProposition(ranking,ranking.mfs['High']))))	
	
r18.consequent.append(FuzzyProposition(Out,Out.mfs['Good']))

#if preferance is low and activity is mid then fitness is bad
r19 = FuzzyRule()
r19.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['High']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Low']),
								   FuzzyProposition(ranking,ranking.mfs['Low']))))	
	
r19.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r20 = FuzzyRule()
r20.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['High']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Low']),
								   FuzzyProposition(ranking,ranking.mfs['Mid']))))	
	
r20.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r21 = FuzzyRule()
r21.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['High']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Low']),
								   FuzzyProposition(ranking,ranking.mfs['High']))))	
	
r21.consequent.append(FuzzyProposition(Out,Out.mfs['Good']))

#if preferance is low and activity is mid then fitness is bad
r22 = FuzzyRule()
r22.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['High']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Mid']),
								   FuzzyProposition(ranking,ranking.mfs['Low']))))	
	
r22.consequent.append(FuzzyProposition(Out,Out.mfs['Normal']))

#if preferance is low and activity is mid then fitness is bad
r23 = FuzzyRule()
r23.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['High']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Mid']),
								   FuzzyProposition(ranking,ranking.mfs['Mid']))))	
	
r23.consequent.append(FuzzyProposition(Out,Out.mfs['Good']))

#if preferance is low and activity is mid then fitness is bad
r24 = FuzzyRule()
r24.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['High']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['Mid']),
								   FuzzyProposition(ranking,ranking.mfs['High']))))	
	
r24.consequent.append(FuzzyProposition(Out,Out.mfs['Good']))

#if preferance is low and activity is mid then fitness is bad
r25 = FuzzyRule()
r25.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['High']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['High']),
								   FuzzyProposition(ranking,ranking.mfs['Low']))))	
	
r25.consequent.append(FuzzyProposition(Out,Out.mfs['Good']))

#if preferance is low and activity is mid then fitness is bad
r25 = FuzzyRule()
r25.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['High']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['High']),
								   FuzzyProposition(ranking,ranking.mfs['Low']))))	
	
r25.consequent.append(FuzzyProposition(Out,Out.mfs['Good']))

#if preferance is low and activity is mid then fitness is bad
r26 = FuzzyRule()
r26.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['High']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['High']),
								   FuzzyProposition(ranking,ranking.mfs['Mid']))))	
	
r26.consequent.append(FuzzyProposition(Out,Out.mfs['Good']))

#if preferance is low and activity is mid then fitness is bad
r27 = FuzzyRule()
r27.antecedent.append(FuzzyOperator('and',FuzzyProposition(preference,preference.mfs['High']),
								   FuzzyOperator('and',FuzzyProposition(activity,activity.mfs['High']),
								   FuzzyProposition(ranking,ranking.mfs['High']))))	
	
r27.consequent.append(FuzzyProposition(Out,Out.mfs['Good']))

Rules=[r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20,r21,r22,r23,r24,r25,r26,r27]
fis = FIS(Rules)


def fisuser(a,b,c):
	preference.current_value = a
	activity.current_value = b
	ranking.current_value = c
	print preference.current_value
	print activity.current_value
	print ranking.current_value


	return fis.eval( out_var = 0)

# if __name__ == '__main__':
#     print fisuser(0,75,27)
