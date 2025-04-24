from django.urls import include, path
from users.views import *
from . import views
import debug_toolbar
urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('my_recommendations/', my_recommendations, name="my_recommendations"),
    path('logs/', views.view_logs, name='view_logs'),
]
