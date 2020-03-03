import swapi
import re
import json
import random

## Star Wars Meals: Find what's for dinner -- IN SPACE!

## Getting api data

# Retrieve all people from swapi
people = swapi.get_all("people")

# Retrieve all planets from swapi
planets = swapi.get_all("planets")


## New class of characters
class Character(object):
	characterName = "characterName"
	homeworldName = "homeworldName"
	planetName = "planetName"

	#Method to find 'dish' for characters as "attribute" using property decorator
	@property
	def dish(self):
	# Find new homeworld

		# Contains all climate and terrain keywords combined for each planet
		planetClimateList = []
		# Loops to strip climates and terrains into single keywords
		for i in self.planetName.climate.strip(",").split(" "):
			planetClimateList.append(i)

		for i in self.planetName.terrain.strip(",").split(" "):
			planetClimateList.append(i)
		
		# Function to amend keywords that don't match World Factbook API
		def fixBrokenKeyword(brokenKeyword, list, newKeyword):
			if brokenKeyword in list:
				if newKeyword in brokenKeyword:
					list.remove(brokenKeyword)
					list.append(newKeyword)
				else:
					list.append(newKeyword)

		fixBrokenKeyword('frozen', planetClimateList, 'freeze')
		fixBrokenKeyword('windy', planetClimateList, 'wind')
		fixBrokenKeyword('artificial temperate', planetClimateList, 'temperate')
		fixBrokenKeyword('frigid', planetClimateList, 'bitter')
		# Since 'superheated' called twice, torrid is used first in the function,
		# because function won't then remove 'superheated' from planetClimateList,
		# which allows 'heat' to also be added to list
		fixBrokenKeyword('superheated', planetClimateList, 'torrid')
		fixBrokenKeyword('superheated', planetClimateList, 'heat')
		fixBrokenKeyword('subartic', planetClimateList, 'subarctic')
		fixBrokenKeyword('artic', planetClimateList, 'arctic')

		# Importing data from json files

		# World Factbook API
		with open('/Users/buttercup/Documents/devProjects/projectStarWarsMeals/starWarsMeals/djangoStarWarsMeals/appStarWarsMeals/static/appStarWarsMeals/worldFactbook.json', 'r') as f: countries_dict = json.load(f)

		# National Dishes
		with open('/Users/buttercup/Documents/devProjects/projectStarWarsMeals/starWarsMeals/djangoStarWarsMeals/appStarWarsMeals/static/appStarWarsMeals/nationalDishes.json', 'r') as f: dictDishes = json.load(f)

		# Make all dictDishes keys lowercase to be more searchable
		dictDishes = {k.lower(): v for k, v in dictDishes.items()}

		# Find candidateCountries by:
		# Seeing how many keywords from planetClimateList match with each country in World
		# Factbook API, then taking all countries with the max matched words
		candidateCountries = {}
		for countryMatch in countries_dict["countries"]:
			matchCounter = 0
			for climateKeyword in planetClimateList:
				if climateKeyword in countries_dict.get("countries").get(countryMatch).get("data") \
				.get("geography").get("climate", '').lower() or climateKeyword in countries_dict \
					.get("countries").get(countryMatch).get("data") \
					.get("geography").get("terrain", '').lower():
					matchCounter += 1

			if matchCounter > 0:
				candidateCountries[countryMatch] = matchCounter
		# Exception for if no match between planet and countries
		if not candidateCountries:
			candidateCountries['default'] = '1'

		#'newHomeworld' generated randomly from candidateCountries
		newHomeworld = random.choice([key for m in [max(candidateCountries.values())] for key, \
			val in candidateCountries.items()
			if val == m])

		# Return national dish of newHomeworld
		dishes = dictDishes.get(newHomeworld)
		if dishes == None:
			dishes = "Country not found!"

		#Split dishes into multiple strings if more than one
		dishesList = []
		for i in dishes.split(", "):
			dishesList.append(i)

		#Choose random dish from country's dishes
		dish = random.choice(dishesList)

		return dish


## Find Character: characterName, homeworldName, planetName

# List to index character objects; also used to populate "Character"s
characterList = []

#Getting character data

counter = 0

# swapi function to iterate over all people
for person in people.iter():


	# Setting up 'homeworld' format for use in Character

	rawHomeworld = person.homeworld
	# Strip homeworld to integer since swapi returns a url
	numberHomeworld = int(re.sub('[^0-9]', '', rawHomeworld))

	#Get actual planet object
	dataPlanet = swapi.get_planet(numberHomeworld)

	# Get planetName
	characterHomeworld = dataPlanet.name


	## Creating new characters and indexing them in list
	characterList.append(Character())
	characterList[counter].characterName = person.name
	characterList[counter].homeworldName = characterHomeworld
	characterList[counter].planetName = dataPlanet
	counter += 1


## Code to find friendHomeworld




## Function to find recipes

