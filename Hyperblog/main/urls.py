from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    WelcomePage, AllPublication, OnePublication,
    MySignUpView, PersonalPage, CreatePublicationView,
    ArticleEdit, ArticleDelete)


app_name = "main"
urlpatterns = [

    path('', WelcomePage.as_view(), name='welcome'),
    path('publications', AllPublication.as_view(), name='publications'),
    path('publications/<int:pk>', OnePublication.as_view(), name='detail'),
    path('login', LoginView.as_view(template_name='main/login.html',
                                    redirect_authenticated_user=True),
         name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', MySignUpView.as_view(), name='signup'),
    path('login/', RedirectView.as_view(url='/login')),
    path('signup/', RedirectView.as_view(url='/signup')),
    path('person', PersonalPage.as_view(), name='person'),
    path('publications/create', CreatePublicationView.as_view(), name='create'),
    path('publications/<int:pk>/edit', ArticleEdit.as_view(), name='post_edit'),
    path('publications/<int:pk>/delete', ArticleDelete.as_view(), name='post_delete'),
]