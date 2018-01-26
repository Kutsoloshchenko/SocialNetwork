"""Functions to get responces to responde to user request"""


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from controllers.controler import Controler

from datetime import date

mod = Controler()


@api_view(['POST', 'GET'])
def sign_up(request):

    if request.method == "GET":
        data = {"username": "da",
                "email": "dasdf@ada23.com",
                "password": "Nu@TutDa8",
                "repeat_password": "Nu@TutDa8"
                }
    else:
        data = request.data

    result = mod.sign_up(data)
    return Response(result)


@api_view(['POST', 'GET'])
def sign_in(request):

    if request.method == "GET":
        data = {"email": "dasdf@ada23.com",
                "password": "Nu@TutDa8",
                }
    else:
        data = request.data

    result = mod.sign_in(data)
    return Response(result)


@api_view(['POST', 'GET'])
def create_post(request):

    if request.method == "GET":
        data = {'title': 'Norm Tema',
                "content": "bla bla bla some stuffasdf",
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRhc2RmQGFkYS5jb20iLCJpZCI6NX0.qVLLRAZ7XFchM0qTwgcsJPHWGmoZnH-pXcS8roFfWKM",
                "email": "dasdf@ada.com"
                }
    else:
        data = request.data

    result = mod.create_post(data)
    return Response(result)


@api_view(['POST', 'GET'])
def get_posts(request):

    if request.method == "GET":
        data = None
    else:
        data = request.data

    result = mod.get_posts(data)
    return Response(result)


@api_view(['POST', 'GET'])
def delete_post(request):

    if request.method == "GET":
        data = {"id": 6,
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRhc2RmQGFkYS5jb20iLCJpZCI6NX0.qVLLRAZ7XFchM0qTwgcsJPHWGmoZnH-pXcS8roFfWKM",
                "email": "dasdf@ada.com"
                }
    else:
        data = request.data

    result = mod.delete_post(data)
    return Response(result)


@api_view(['POST', 'GET'])
def edit_post(request):

    if request.method == "GET":
        data = {"title": "Post",
                "content": "hello 2",
                "id": 1,
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRhc2RmQGFkYS5jb20iLCJpZCI6NX0.qVLLRAZ7XFchM0qTwgcsJPHWGmoZnH-pXcS8roFfWKM",
                "email": "dasdf@ada.com"
                }
    else:
        data = request.data

    result = mod.edit_post(data)
    return Response(result)


@api_view(['POST', 'GET'])
def update_like(request):

    if request.method == "GET":
        data = {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRhc2RmQGFkYS5jb20iLCJpZCI6NX0.qVLLRAZ7XFchM0qTwgcsJPHWGmoZnH-pXcS8roFfWKM",
                "email": "dasdf@ada.com"
                }
    else:
        data = request.data

    result = mod.update_like(data)
    return Response(result)