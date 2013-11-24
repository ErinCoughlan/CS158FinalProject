

# returns a Cosine similarity score for p1 and p2
def sim_cosine(ratings, p1, p2):
	# get the list of shared_items
	si = {}
	for item in ratings[p1]:
		if item in ratings[p2]:
			si[item] = 1

	# if they have no rating in common, return 0
	if len(si) == 0: 
		return 0

	# sum of the products 
	numerator = sum([ratings[p1][x] * ratings[p2][x] for x in si])

	# sum of squares
	sum1 = sum([ratings[p1][x]**2 for x in si])
	sum2 = sum([ratings[p2][x]**2 for x in si])
	
	# dot product calculation
	denominator = sqrt(sum1) * sqrt(sum2)

	# check for denom == 0
	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator


# returns the Pearson correlation coefficient for p1 and p2 
def sim_pearson(ratings,p1,p2):
	# get the list of mutually rated items
	si = {}
	for item in ratings[p1]:
		if item in ratings[p2]: 
			si[item] = 1

	# if they are no rating in common, return 0
	if len(si) == 0:
		return 0

	# sum calculations
	n = len(si)

	# sum of all preferences
	sum1 = sum([ratings[p1][x] for x in si])
	sum2 = sum([ratings[p2][x] for x in si])

	# sum of the squares
	sum1Sq = sum([ratings[p1][x]**2 for x in si])
	sum2Sq = sum([ratings[p2][x]**2 for x in si])

	# sum of the products
	pSum = sum([ratings[p1][x] * ratings[p2][x] for x in si])

	# calculate r (Pearson score)
	num = pSum - (sum1 * sum2/n)
	den = sqrt((sum1Sq - (sum1**2/n)) * (sum2Sq - (sum2**2/n)))
	if den == 0:
		return 0

	r = num/den

	return r

# returns the best matches for person from the ratings dictionary
# number of the results and similiraty function are optional params.
def top_matches(ratings,person,n=5,similarity=sim_cosine):
	scores = [(similarity(ratings,person,other),other)
				for other in ratings if other != person]
	scores.sort()
	scores.reverse()
	return scores[0:n]


# gets recommendations for a person by using a weighted average
# of every other user's rankings
def get_recommendations(ratings,person,similarity=sim_cosine):
	totals = {}
	sim_sums = {}

	for other in ratings:
		# don't compare user to itself
		if other == person:
			continue

		# call the similarity function we define
		sim = similarity(ratings,person,other)

		# ignore scores of zero or lower
		if sim <= 0: 
			continue

		# for each of other's items calc totals + sim_sums
		for item in ratings[other]:
			
			# only score items user hasn't seen yet
			if item not in ratings[person] or ratings[person][item] == 0:
				
				# similarity * score
				totals.setdefault(item,0)
				totals[item] += ratings[other][item] * sim
		
				# sum of similarities
				sim_sums.setdefault(item,0)
				sim_sums[item] += sim

	# create the normalized list
	rankings = [(total/sim_sums[item],item) for item,total in totals.items()]

	# return the sorted list
	rankings.sort()
	rankings.reverse()
	return rankings


# function to transform Person, item - > Item, person
def compose_ratings(ratings):
	results = {}
	for person in ratings:
		for item in ratings[person]:
			results.setdefault(item,{})

			# flip item and person
			results[item][person] = ratings[person][item]
	return results

if __name__=="__main__":

	recs = get_recommendations(movies,'Leopoldo Pires')
	print recs