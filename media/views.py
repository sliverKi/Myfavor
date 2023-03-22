from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
import requests
from .models import Photo


class PhotoDetail(APIView):
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

        
class GetUploadURL(APIView):
    def post(self, request):
        url= f"https://../accounts{settings.CF_ID}/images/v2/"
        one_time_url = requests.post(url, headers={
            "Authorization":f"Bearer {settings.CF_TOCKEN}"
        })
        one_time_url = one_time_url.json()
        result=one_time_url.get('result')
        return Response({"id":result.get("id"), "uploadURL": result.get('uploadURL')})