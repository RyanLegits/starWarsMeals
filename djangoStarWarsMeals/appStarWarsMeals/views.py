from django.shortcuts import render
from django.views.generic import TemplateView

from .utils import character_list
from .forms import CharacterListForm

class CharacterListView(TemplateView):
	template_name = 'recipes/home.html'

	def get(self, request):
		form = CharacterListForm()
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = CharacterListForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['post']
			for i in character_list:
				if i.character_name == text:
					i.dish()
					character_dialogue = i.character_name + ": I'm from " + i.homeworld_name + ", but on Earth I really like to make "
					recipe_label = i.recipe_label + "."
					recipe_image = i.recipe_image
					recipe_url = i.recipe_url
					ingredients_label = 'Shopping list: '
					recipe_ingredients = i.recipe_ingredients
					
		args = {'form': form, 'character_dialogue': character_dialogue, 'recipe_label': recipe_label, 'recipe_image': recipe_image, 'recipe_url': recipe_url, 'ingredients_label': ingredients_label, 'recipe_ingredients': recipe_ingredients}

		return render(request, self.template_name, args)
