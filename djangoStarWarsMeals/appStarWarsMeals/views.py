from django.shortcuts import render
from appStarWarsMeals.utils import characterList

def home(request):
	
	dishList = []
	
	for i in characterList:
		dishList.append(i.dish)

	context = {
		'dishList': dishList
	}
	return render(request, 'recipes/home.html', context)
	