__author__ = 'frank'
from FIS import *
Age = LinguisticVariable('Age')
Age.addMF('Low',MF.Triangular(-10, 0, 10))
Age.addMF('Mid',MF.Triangular(3, 13, 23))
Age.addMF('High',MF.Triangular(15, 25, 35))

Schoolar = LinguisticVariable('Schoolar')
Schoolar.addMF('Low',MF.Triangular(-10, 0, 10))
Schoolar.addMF('Mid',MF.Triangular(0, 11, 21))
Schoolar.addMF('High',MF.Triangular(12, 21, 32))
#OUT
Out = LinguisticVariable('topN', type='out', range=(0, 9))
Out.addMF('Begginer',MF.Triangular(-3, 0, 3))
Out.addMF('Junior',MF.Triangular(0, 3, 6))
Out.addMF('Senior',MF.Triangular(3, 6, 9))
Out.addMF('Pro',MF.Triangular(6, 9, 12))
# Rules
#if Logs == Low and Answer == low and Approached == Low then Out == Low
r1 = FuzzyRule()
r1.antecedent.append(FuzzyOperator('and',FuzzyProposition(Age,Age.mfs['Low']),FuzzyProposition(Schoolar,Schoolar.mfs['Low'])))
r1.consequent.append(FuzzyProposition(Out,Out.mfs['Begginer']))
#if Logs == Low and Answer == High and Approached == Low then Out == Low
r2 = FuzzyRule()
r2.antecedent.append(FuzzyOperator('and',FuzzyProposition(Age,Age.mfs['Low']),FuzzyProposition(Schoolar,Schoolar.mfs['Mid'])))
r2.consequent.append(FuzzyProposition(Out,Out.mfs['Begginer']))
#if Logs == Low and Answer == High and Approached == Low then Out == Low
r3 = FuzzyRule()
r3.antecedent.append(FuzzyOperator('and',FuzzyProposition(Age,Age.mfs['Low']),FuzzyProposition(Schoolar,Schoolar.mfs['High'])))
r3.consequent.append(FuzzyProposition(Out,Out.mfs['Junior']))
#if Logs == Low and Answer == High and Approached == Low then Out == Low
r4 = FuzzyRule()
r4.antecedent.append(FuzzyOperator('and',FuzzyProposition(Age,Age.mfs['Mid']),FuzzyProposition(Schoolar,Schoolar.mfs['Low'])))
r4.consequent.append(FuzzyProposition(Out,Out.mfs['Junior']))
#if Logs == Low and Answer == High and Approached == Low then Out == Low
r5 = FuzzyRule()
r5.antecedent.append(FuzzyOperator('and',FuzzyProposition(Age,Age.mfs['Mid']),FuzzyProposition(Schoolar,Schoolar.mfs['Mid'])))
r5.consequent.append(FuzzyProposition(Out,Out.mfs['Junior']))
#if Logs == Low and Answer == High and Approached == Low then Out == Low
r6 = FuzzyRule()
r6.antecedent.append(FuzzyOperator('and',FuzzyProposition(Age,Age.mfs['Mid']),FuzzyProposition(Schoolar,Schoolar.mfs['High'])))
r6.consequent.append(FuzzyProposition(Out,Out.mfs['Senior']))
#if Logs == Low and Answer == High and Approached == Low then Out == Low
r7 = FuzzyRule()
r7.antecedent.append(FuzzyOperator('and',FuzzyProposition(Age,Age.mfs['High']),FuzzyProposition(Schoolar,Schoolar.mfs['Low'])))
r7.consequent.append(FuzzyProposition(Out,Out.mfs['Senior']))
#if Logs == Low and Answer == High and Approached == Low then Out == Low
r8 = FuzzyRule()
r8.antecedent.append(FuzzyOperator('and',FuzzyProposition(Age,Age.mfs['High']),FuzzyProposition(Schoolar,Schoolar.mfs['Mid'])))
r8.consequent.append(FuzzyProposition(Out,Out.mfs['Pro']))
#if Logs == Low and Answer == High and Approached == Low then Out == Low
r9 = FuzzyRule()
r9.antecedent.append(FuzzyOperator('and',FuzzyProposition(Age,Age.mfs['High']),FuzzyProposition(Schoolar,Schoolar.mfs['High'])))
r9.consequent.append(FuzzyProposition(Out,Out.mfs['Pro']))
#if Logs == Low and Answer == High and Approached == Low then Out == Low
Rules=[r1,r2,r3,r4,r5,r6,r7,r8,r9]
fis = FIS(Rules)


def fisuser(a,b):
    Age.current_value=a
    Schoolar.current_value=b
    return fis.eval( out_var = 0)

if __name__ == '__main__':
    print eval(25,15)
