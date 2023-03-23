
from django.urls import path
from .views import GetUploadURL, PhotoDetail

urlpatterns=[
    path("photos/<int:pk>/", PhotoDetail.as_view()),
    path("photos/get-url/", GetUploadURL.as_view()),
]
<<<<<<< HEAD
=======

     
>>>>>>> f71ffa0d58e5fe4c063db0a9fc9ed589f9d867c2
