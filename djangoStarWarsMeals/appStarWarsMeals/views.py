from django.shortcuts import render
from appStarWarsMeals.utils import luke

def home(request):
	context = {

		'luke': luke.name
	}
	return render(request, 'recipes/home.html', context)
	