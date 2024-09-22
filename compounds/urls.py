from django.urls import path
from compounds.views.user_views import RegisterUserView, LoginView, UserSearchView
from compounds.views.compound_views import CompoundListView, CompoundUpdateView, ShareCompoundView, SearchCompoundView, CompoundDeleteView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('compounds/', CompoundListView.as_view(), name='compound-list'),
    path('compounds/<uuid:pk>/delete/', CompoundDeleteView.as_view(), name='delete-compound'),
    path('compounds/<uuid:pk>/update/', CompoundUpdateView.as_view(), name='update-compound'),
    path('compounds/search/', SearchCompoundView.as_view(), name='search-compound'),
    path('compounds/<uuid:pk>/share/', ShareCompoundView.as_view(), name='share-compound'),
    path('users/search/', UserSearchView.as_view(), name='search-users'),
]
