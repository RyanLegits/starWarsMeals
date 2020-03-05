from django import forms
from .utils import characterTuples

characterFormTuple = characterTuples()
# Form to select character from drop-down
class CharacterListForm(forms.Form):
	post = forms.CharField(label='Choose a character', widget=forms.Select(choices=characterFormTuple))
	