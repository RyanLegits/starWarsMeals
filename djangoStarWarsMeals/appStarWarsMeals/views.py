from django.shortcuts import render
from appStarWarsMeals.utils import characterList

def home(request):

	context = {
		'characterList': characterList
	}
	return render(request, 'recipes/home.html', context)
	