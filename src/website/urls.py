from django.urls import path
from .views import HomeView, RulesView, ChampionsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('champions/', ChampionsView.as_view(), name='champions'),
]