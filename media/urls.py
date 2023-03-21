
from django.urls import path
from .views import GetUploadURL, PhotoDetail

urlpatterns=[
    # path("photos/get-url", GetUploadURL),
    path("photos/<int:pk>", PhotoDetail.as_view())
]

# class GetUploadURL(APIView):
#     def post(self, request):
#         url="https://api.cloudflare.com/client/v4/accounts/{}/images/v1"