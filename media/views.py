# from django.shortcuts import render
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# import requests

# # Create your views here.
# class GetUploadURL(APIView):
#     def post(self, request):
#         url= f"https://../accounts{settings.CF_ID}/images/v2/"
#         one_time_url = requests.post(url, headers={
#             "Authorization":f"Bearer {settings.CF_TOCKEN}"
#         })
#         one_time_url = one_time_url.json()
#         result=one_time_url.get('rsult')
#         return Response({"uploadURL": result.get('uploadURL')})