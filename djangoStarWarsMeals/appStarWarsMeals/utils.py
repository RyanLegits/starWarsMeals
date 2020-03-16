import requests
import json
import random

## Star Wars Meals: Find what's for dinner -- IN SPACE!


## Function to get swapi data
def get_swapi(str_data):
	# Pulling json data from swapi
	list_data = []
	swapi_data = requests.get("https://swapi.co/api/" + str_data + "/")
	json_data = swapi_data.json()

	# First page of swapi data results
	list_data = list_data + json_data['results']

	# Adding all other pages of data from swapi
	while json_data['next'] is not None:
		swapi_data = requests.get(json_data['next'])
		json_data = swapi_data.json()
		# Add current results page to 'list_data'
		list_data = list_data + json_data['results']

	return list_data


## Getting api data

# Retrieve all people from swapi
people = get_swapi('people')

# Retrieve all planets from swapi
planets = get_swapi('planets')


## New class of characters
class Character(object):
	character_name = "character_name"
	homeworld_name = "homeworld_name"
	planet_climate = "planet_climate"
	planet_terrain = "planet_terrain"
	
	character_dialogue = "Hello, there. It looks like we've got a problem!"
	recipe_label = ""
	recipe_image = ""
	recipe_url = ""
	recipe_ingredients = ""

	#Method to find recipe related attributes for characters 
	def dish(self):
	# Find new homeworld

		# Contains all climate and terrain keywords combined for each planet
		planet_climateList = []
		# Loops to strip climates and terrains into single keywords
		for i in self.planet_climate.strip(",").split(" "):
			planet_climateList.append(i)

		for i in self.planet_terrain.strip(",").split(" "):
			planet_climateList.append(i)

		# Function to amend keywords that don't match World Factbook API
		def fix_broken_keyword(broken_keyword, list, new_keyword):
			if broken_keyword in list:
				if new_keyword in broken_keyword:
					list.remove(broken_keyword)
					list.append(new_keyword)
				else:
					list.append(new_keyword)

		fix_broken_keyword('frozen', planet_climateList, 'freeze')
		fix_broken_keyword('windy', planet_climateList, 'wind')
		fix_broken_keyword('artificial temperate', planet_climateList, 'temperate')
		fix_broken_keyword('frigid', planet_climateList, 'bitter')
		# Since 'superheated' is called twice, torrid is used first in the function,
		# because function won't then remove 'superheated' from planet_climateList,
		# which allows 'heat' to also be added to list
		fix_broken_keyword('superheated', planet_climateList, 'torrid')
		fix_broken_keyword('superheated', planet_climateList, 'heat')
		fix_broken_keyword('subartic', planet_climateList, 'subarctic')
		fix_broken_keyword('artic', planet_climateList, 'arctic')

		# Importing data from json files

		# World Factbook API
		with open('staticfiles/appStarWarsMeals/worldFactbook.json', 'r') as f: countries_dict = json.load(f)

		# National Dishes
		with open('staticfiles/appStarWarsMeals/nationalDishes.json', 'r') as f: dict_dishes = json.load(f)

		# Make all dict_dishes keys lowercase to be more searchable
		dict_dishes = {k.lower(): v for k, v in dict_dishes.items()}

		# Find candidate_countries by:
		# Seeing how many keywords from planet_climateList match with each country in World
		# Factbook API, then taking all countries with the max matched words
		candidate_countries = {}
		for country_match in countries_dict["countries"]:
			match_counter = 0
			for climate_keyword in planet_climateList:
				if climate_keyword in countries_dict.get("countries").get(country_match).get("data") \
				.get("geography").get("climate", '').lower() or climate_keyword in countries_dict \
					.get("countries").get(country_match).get("data") \
					.get("geography").get("terrain", '').lower():
					match_counter += 1

			if match_counter > 0:
				candidate_countries[country_match] = match_counter
		# Exception for if no match between planet and countries
		if not candidate_countries:
			candidate_countries['default'] = '1'

		#'new_homeworld' generated randomly from candidate_countries
		new_homeworld = random.choice([key for m in [max(candidate_countries.values())] for key, \
			val in candidate_countries.items()
			if val == m])


		## Find dish in API

		# Search edamam API
		def search_recipes(recipe_keyword):
			edamam_id = 'aa9cc0ca'
			edamam_key = 'c120cd72f8c76ced88f1977e1c227c59'
			edamam_data = requests.get('https://api.edamam.com/search?q=' + recipe_keyword + '&app_id=' + edamam_id + '&app_key=' + edamam_key)
			return edamam_data.json()

		# Choose random recipe from edamam results
		def choose_recipe(recipe_results):
			recipe_hits = -1
			for i in recipe_results['hits']:
				recipe_hits += 1

			# If recipe found, choose one randomly
			random_recipe = -1
			if recipe_hits > -1:
				random_recipe = random.randint(0, recipe_hits)
			
			return random_recipe


		## Add dish info to 'Character' object
		def populate_recipe(results, chosen_recipe):
			# Setting up 'recipe_ingredients' attribute for 'RecipeData'
			list_ingredients = []
			for line in results['hits'][chosen_recipe]['recipe']['ingredientLines']:
				list_ingredients.append(line)

			Character.character_dialogue = "Hello! I'm " + self.character_name + "." + " I'm from " + self.homeworld_name + ", but on Earth I really like to eat "
			Character.recipe_label = results['hits'][chosen_recipe]['recipe']['label']
			Character.recipe_image = results['hits'][chosen_recipe]['recipe']['image']
			Character.recipe_url = results['hits'][chosen_recipe]['recipe']['url']
			Character.recipe_ingredients = list_ingredients

		#Search for recipe using character's 'newhomeworld'
		edamam_recipes = search_recipes(new_homeworld)
		character_recipe = choose_recipe(edamam_recipes)
		if character_recipe > -1:
			populate_recipe(edamam_recipes, character_recipe)


		# ###1 Save this code as part of larger dish finding algo in future version

		# # Return national dish of new_homeworld
		# dishes = dict_dishes.get(new_homeworld)
		# if dishes == None:
		# 	dishes = "Country not found!"

		# #Split dishes into multiple strings if more than one
		# list_dishes = []
		# for i in dishes.split(", "):
		# 	list_dishes.append(i)

		# #Choose random dish from country's dishes
		# dish = random.choice(list_dishes)

		# return dish

		# ###1 end


## Find Character attributes

# List to index and populate 'Character' objects
character_list = []
counter = 0

# swapi function to iterate over all people
for person in people:

	character_homeworld = ''
	character_climate = ''
	character_terrain = ''
	for planet in planets:
		if person['homeworld'] == planet['url']:
			character_homeworld = planet['name']
			character_climate = planet['climate']
			character_terrain = planet['terrain']


	## Creating new characters and indexing them in list
	character_list.append(Character())
	character_list[counter].character_name = person['name']
	character_list[counter].homeworld_name = character_homeworld
	character_list[counter].planet_climate = character_climate
	character_list[counter].planet_terrain = character_terrain

	counter += 1


## Function to make tuple list for use in drop-down list form
def make_character_tuples():
	list_character_tuples = []
	for index in character_list:
		list_character_tuples.append((index.character_name, index.character_name))
	return list_character_tuples
