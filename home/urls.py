# home/urls.py
from django.urls import path
from .views.base_views import *
from .views.author_views import *
#from .views.participant_views import participant_dashboard

urlpatterns = [
    # Base/public views
    path('', home, name='home'),
    path('author-signup/', author_signup, name='author_signup'),
    path('participant-join/', participant_join, name='participant_join'),
    path('authors/', show_authors, name='authors'),
    path('sign_in/', sign_in, name='sign_in'),
    
    # Author views
    path('author-dashboard/', author_dashboard, name='author_dashboard'),
    path('update_author_profile/', update_author_profile, name='update_author_profile'),
    path('author_subjects_api/', author_subjects_api, name='author_subjects_api'),

    
    # Participant views
    path('participant-dashboard/', participant_dashboard, name='participant_dashboard'),
]