''' This file contains all of the code related to computing the queries in part
b, c, and d of question two on the assignment. When running this program, 
please ensure that it is in the same folder as BayesianNetwork.py

This program will output the answer to all queries to the console'''


import numpy
import BayesianNetwork as BN

# Used to restrict a factor based on a variable and a value
def restrict(factor, variable, value):
	tmp = {}
	for i in factor: 
	 	# get the variables and their values involved in each probability who contain the value we are restricting on
	 	if value in i.split('_'):
	 		var = i.split('_')
	 		newval =''
	 		for val in var:
	 			# remove the value that we are trying to restrict on in our new factor since it is no loger relevant
	 			if val <> value:
	 				newval += val + '_'
	 		newval = newval[:-1]		
	 		tmp[newval] = factor[i]
	# only return if we have made a factor, otherwise return the original factor.
	if tmp <> {}:
		return tmp
	return factor

# multiply two factors together
def multiply(factor1, factor2):
	tmp = {}
	# get the values of all of the variables involved in both factors
	factor1_values = factor1.keys()[0].split('_')
	factor1_elts = []
	for val in factor1_values:
		factor1_elts.append(val.replace('~', '').upper())
	factor2_elts = []
	factor2_values = factor2.keys()[0].split('_')
	for val in factor2_values:
		factor2_elts.append(val.replace('~', '').upper())
	
	# get the overlap between the two factors so we know which elements to multiply together
	common_elts = set(factor1_elts).intersection(factor2_elts)
	
	for i in factor1:
		for j in factor2:
			factor1_vals = i.split('_')
			factor2_vals = j.split('_')
			# get the overlapping variables for the current two vales in the factor
			overlap = set(factor1_vals).intersection(factor2_vals)
			
			# if the correct values are in common, multiply the two values together
			if len(overlap) == len(common_elts) and len(common_elts) > 0:
				variables = i
				# construct the new value name based on the variables involved in the multiplicaiton
				for val in factor2_vals: 
					if val not in variables:
						variables += '_' + val
				# multply the two values together
				tmp[variables] = factor1[i] * factor2[j]
	return tmp			


# method that returns a factor with the indicated variable summed out. 
def sumout(factor, variable):
	tmp = {}
	# generate the values for the chosen variable
	values = [variable.lower(), '~' + variable.lower()]
	
	for value in factor:
		val = value.split('_')
		newval = ''
		for var in val:
			# add values that are not the one you are trying to sum out to your new factor
			if var not in values :
				newval += var + '_'
		newval = newval[:-1]
		# add the relevant value from the factor to the summed out value
		if newval in tmp: 
			tmp[newval] += factor[value]
		else: 
			tmp[newval] = factor[value]	
	return tmp


# normalize a factor before returning the result to ensure that all probabilities are valid
def normalize(factor):
	result= {}
	total = 0
	for val in factor:
		total += factor[val]
	for val in factor:
		result[val] = factor[val]/total
	return result
			
# compute a query on a set of factors. 
def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
		newFactorList = []
		orderedFactorList = []
		generatedFactors = []
		# order the factors in the factor list according to the elimination order in
		# orderedListOfHiddenVariables, then by adding anything in the factor list
		# that does not appear in the elimination order, then adding the factor 
		# that corresponds to the query Variable last.
		for var in orderedListOfHiddenVariables:
			for factor in factorList:
				if factor.name == var:
					orderedFactorList.append(factor)
		for factor in factorList:
			if factor.name not in queryVariables and factor not in orderedFactorList:
				orderedFactorList.append(factor) 
		for factor in factorList:
			if factor.name in queryVariables:
				orderedFactorList.append(factor) 

		# Restrict all factors according to the evidence
		for factor in orderedFactorList:
			tmpfactor = factor
			for evidence in evidenceList:
				tmpfactor.cpt = restrict(factor.cpt, evidence.replace('~', '').upper(), evidence)
			newFactorList.append(tmpfactor)
			if factor.cpt <> tmpfactor.cpt:
				generatedFactors.append(tmpfactor.cpt)
		# if no factors were restricted, use the original factor list.
		if newFactorList == []:
			newFactorList = orderedFactorList	

		multipliedFactor = None
		toMultiply = []
		
		j = 0
		# multiply all factors together according to the elimination order as much as possible. 
		# a list called toMultiply is kept to enusure that there are no factors multiplied
		# together who have no common elements.
		while j < len(newFactorList):  
			if multipliedFactor == None:
				if multiply(newFactorList[j].cpt, newFactorList[j+1].cpt) == {}:	
					toMultiply.append(newFactorList[j])
				else:
					multipliedFactor = multiply(newFactorList[j].cpt, newFactorList[j+1].cpt)
					generatedFactors.append(multipliedFactor)
					j+=1
			else:
				if multiply(multipliedFactor, newFactorList[j].cpt) == {}:
					toMultiply.append(newFactorList[j])
				else:
					multipliedFactor = multiply(multipliedFactor, newFactorList[j].cpt)
					generatedFactors.append(multipliedFactor)
			j += 1

		# multiply all remanining factors into the large multiplied factors now that they have common elements
		for factor in toMultiply:
			multipliedFactor = multiply(multipliedFactor, factor.cpt)
			generatedFactors.append(multipliedFactor)
		
		# sum out all variables from the product of all of the factors
		for var in orderedListOfHiddenVariables:
			multipliedFactor = sumout(multipliedFactor, var)
			generatedFactors.append(multipliedFactor)

		# normalize the result
		result = normalize(multipliedFactor)

		#uncomment if you would like to outpur all of the factors that were generated. make sure to comment
		# all options other than the one you would like to see factors before running this.
		'''stringfactors = ''
		for factor in generatedFactors:
			stringfactors += str(factor) + '\n\n'
		f = open('partE-Factors.txt','a')
		f.write(stringfactors)
		f.close()'''
		return result




bn = BN.BN()

# part B

fidohowls = inference([bn.BN[0], bn.BN[2], bn.BN[3], bn.BN[4], bn.BN[5]], ['FH'], ['NA', 'NDG', 'FM', 'FS'], [])
print "the probabilty that fido will howl is " + str(fidohowls['fh'])

# part C
fidosick = inference([bn.BN[0], bn.BN[1], bn.BN[3], bn.BN[4], bn.BN[5]], ['FS'], ['NDG', 'NA','FB'], ['fh', 'fm'])
print "the probabilty that fido is sick given the fact that there is a full moon and he is howling is " + str(fidosick['fs'])

# part D
fidosick2 = inference([bn.BN[0], bn.BN[1], bn.BN[3], bn.BN[4], bn.BN[5]], ['FS'], ['NDG', 'NA'], ['fh', 'fm', 'fb'])
print "the probabilty that fido is sick given the fact that there is a full moon, he is howling, and there is food in his bowl is " + str(fidosick2['fs'])

# part E
fidosick3 = inference([bn.BN[0], bn.BN[1], bn.BN[4], bn.BN[5]], ['FS'], ['NDG'], ['fh', 'fm', 'fb','na'])
print "the probabilty that fido is sick given the fact that there is a full moon, he is howling, there is food in his bowl, and the neighbor is away is " + str(fidosick3['fs'])
