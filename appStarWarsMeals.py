import swapi
import re
import json
import random

# Star Wars Meals: Find what's for dinner -- IN SPACE!

# Retrieve all people from swapi
people = swapi.get_all("people")

# New class of characters
class Character:
    def __init__(self, name, homeworld, dish):
        self.name = name
        self.homeworld = homeworld
        self.dish = dish


# List to index character objects; also used to populate "Character"s
characterList = []


# Function to amend keywords that don't match World Factbook API
def fixBrokenKeyword(brokenKeyword, list, newKeyword):
    if brokenKeyword in list:
        if newKeyword in brokenKeyword:
            list.remove(brokenKeyword)
            list.append(newKeyword)
        else:
            list.append(newKeyword)


#Importing data from json files

# World Factbook API
with open('/Users/eflash/Documents/devProjects/appStarWarsMeals/worldFactbook.json', \
          'r') as f:
    countries_dict = json.load(f)

# National Dishes
with open('/Users/eflash/Documents/devProjects/appStarWarsMeals/nationalDishes.json', \
          'r') as f:
    dictDishes = json.load(f)

dictDishes = {k.lower(): v for k, v in dictDishes.items()}

#Getting character data

# swapi function to iterate over all people
for person in people.iter():

    # Setting up 'homeworld' format for use in Character

    rawHomeworld = person.homeworld
    # Strip homeworld to integer since swapi returns a url
    strippedHomeworld = re.sub('[^0-9]', '', rawHomeworld)

    dataPlanet = swapi.get_planet(strippedHomeworld)
    # Get actual planet name
    characterHomeworld = dataPlanet.name

    # Find new homeworld

    # Contains all climate and terrain keywords combined for each planet
    planetClimateList = []
    # Loops to strip climates and terrains into single keywords
    for i in dataPlanet.climate.strip(",").split(" "):
        planetClimateList.append(i)

    for i in dataPlanet.terrain.strip(",").split(" "):
        planetClimateList.append(i)

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


    # Creating new characters and indexing them in list
    characterList.append(Character(person.name, characterHomeworld, dish))
