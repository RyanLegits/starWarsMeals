from django.urls import path
from . import views
from .views import CharacterListView

urlpatterns = [
	path('', CharacterListView.as_view(), name='home'),
]
