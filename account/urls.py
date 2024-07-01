from django.urls import path

from .views import (
    user_login,
    user_register,
    home,
    get_list_of_people_by_file,
    add_people_to_file,
    activate,
    email_sent

)

urlpatterns = [
    path('', home, name='home'),
    path('add-people/<int:file_id>/', add_people_to_file, name='add_people'),
    path('login/', user_login, name='login'),
    path('share/<int:file_id>/', get_list_of_people_by_file, name='share_file'),
    path('register/', user_register, name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('sent/', email_sent, name='email-sent')
]
