from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
import requests
from .models import Photo
from rest_framework.status import HTTP_200_OK

class PhotoDetail(APIView):
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound
   
    def delete(self, request, pk):
        photo = self.get_object(pk)
        if request.user.is_admin:
            photo.delete()
        return Response(status=HTTP_200_OK)    

        
class GetUploadURL(APIView):
    def post(self, request):
        url= f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        one_time_url = requests.post(url, headers={
            "Authorization":f"Bearer {settings.CF_TOKEN}"
        })
        one_time_url = one_time_url.json()
        result=one_time_url.get('result')
        return Response({"id":result.get("id"), "uploadURL": result.get('uploadURL')})