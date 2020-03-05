from django.shortcuts import render
from django.views.generic import TemplateView

from .utils import characterList
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
			for i in characterList:
				if i.characterName == text:
					text = i.dish
					
		args = {'form': form, 'text': text}

		return render(request, self.template_name, args)
