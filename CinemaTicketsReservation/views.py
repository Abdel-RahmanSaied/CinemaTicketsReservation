from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status , filters
from rest_framework.response import Response
from .serializers import *

# Create your views here.

# without  restframework and no model query

def no_rest_no_model(request):
    guests = [
        {
            "id":1 ,
            "name":"saied",
            "mobile" : 122
        },
        {
            "id": 2,
            "name": "abdo",
            "mobile": 122
        }
    ]

    return JsonResponse(guests , safe=False)

# 2 model data defauls django no rest
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        "guests" : list(data.values("name","mobile"))
    }

    return JsonResponse(response, safe=False)

# list == GET
# Create == POST
# pk query == GET
# Update == PUT
# Delete destroy == DELETE

#3 Function based views

# 3.1 GET POST
@api_view(['GET','POST'])
def FBV_List(request):
    # GET
    if request.method == 'GET' :
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests , many=True)
        return Response(serializer.data )

    # POST
    elif request.method == 'POST':
        name = request.data['name']
        mobile = request.data['mobile']
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def FBV_PK(request,pk):
    try :
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)
    #GET
    if request.method == 'GET' :
        serializer = GuestSerializer(guest )
        return Response(serializer.data )

    # PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    elif request.method == 'DELETE':
            guest.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


