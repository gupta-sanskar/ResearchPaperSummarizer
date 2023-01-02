from django.urls import path, include
from . import views
from chat.urls import urlpatterns as chat_urlpatterns

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.handleSignup, name="handleSignup"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('search', views.handleSearch, name="search"),
    path('extract', views.extractPDF, name="extractPDF"),
    path('download', views.download, name="download"),
    path('discussion', include((chat_urlpatterns, "chat-app-namespace"))),
]
