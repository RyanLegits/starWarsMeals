from django import forms
from .utils import make_character_tuples

character_form_tuple = make_character_tuples()
# Form to select character from drop-down
class CharacterListForm(forms.Form):
	post = forms.CharField(label='Choose a character', widget=forms.Select(choices=character_form_tuple))
	