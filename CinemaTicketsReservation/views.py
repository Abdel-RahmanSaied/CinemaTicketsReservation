from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status , filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import  generics , mixins , viewsets
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

#4.1 Class Based View
class CBV_List(APIView) :
    def get(self , request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests , many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data , status=status.HTTP_400_BAD_REQUEST)

#4.2 GET PUT DELETE --> PK

class CBV_PK(APIView) :
    def get_object(self , pk):
        try :
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist :
            raise Http404

    def get(self , request , pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return  Response(serializer.data)
    def put(self , request , pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest , data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5 Mixins
# 5.1 mixins list

class mixins_list(mixins.ListModelMixin , mixins.CreateModelMixin , generics.GenericAPIView ):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self , request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

#5.2 mixins Get put delete

class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self , request , pk):
        return self.retrieve(request)
    def put(self,request , pk):
        return self.update(request)
    def delete(self,request , pk):
        return self.destroy(request)


# 6 Generics
# 6.1  get and post

class generics_list(generics.ListCreateAPIView) :
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer



# ViewSets

class viewSets_guest(viewsets.ModelViewSet) :
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class viewSets_movie(viewsets.ModelViewSet) :
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class viewSets_reservation(viewsets.ModelViewSet) :
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

#8 Find Movie
@api_view(['GET'])
def find_movie(request):
    movie = request.data['movie']
    hall = request.data['hall']
    movies = Movie.objects.filter( movie = movie  , hall = hall)

    serializer = MovieSerializer(movies , many= True)
    return Response(serializer.data)

#9 Create new Reservation

@api_view(["POST"])
def new_reservation(request):
    movie = request.data['movie']
    hall = request.data['hall']
    name = request.data['name']
    mobile = request.data['mobile']

    guest = Guest()
    reservation = Reservation()

    try :
        movies = Movie.objects.get(hall=hall , movie=movie)
    except  Movie.DoesNotExist  :
        return Response( {"Response":" invalid film data"} , status=status.HTTP_404_NOT_FOUND)

    guest.name = name
    guest.mobile = mobile
    guest.save()

    reservation.guest = guest
    reservation.movie = movies
    reservation.save()

    return Response( {"Response":" Reservation Successfully "} , status=status.HTTP_201_CREATED)



