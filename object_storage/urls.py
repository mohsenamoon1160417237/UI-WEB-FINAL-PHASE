from django.urls import path

from .views import (
    upload_object,
    delete_object,
    download_object
)

urlpatterns = [
    path('upload/', upload_object, name='upload_object'),
    path('delete/<int:file_id>/', delete_object, name='delete_object'),
    path('download/<int:file_id>/', download_object, name='download_object')
]
