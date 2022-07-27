
from django.contrib import admin
from django.urls import path , include
from CinemaTicketsReservation import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('guests' , views.viewSets_guest)
router.register('movies' , views.viewSets_movie)
router.register('reservations' , views.viewSets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),

    #1
    path('django/JsonResponsenomodel/' , views.no_rest_no_model),

    #2
    path('django/no_rest_from_model/' , views.no_rest_from_model),

    #3 GET POST from rest framework
    path('rest/FBVList/' , views.FBV_List),

    # 3.1 GET PK
    path('rest/FBV/<int:pk>' , views.FBV_PK),

    # 4.1 GET POST from rest framework class based view
    path('rest/CBVList/', views.CBV_List.as_view()),

    # 4.2 GET PUT DELETE class based view --> PK
    path('rest/CBVPK/<int:pk>', views.CBV_PK.as_view()),

    # 5.1 GET POST mixins
    path('rest/mixins_list/', views.mixins_list.as_view()),

    # 5.2 GET put delete  mixins
    path('rest/mixins_pk/<int:pk>', views.mixins_pk.as_view()),

    # 6 Generics
    # 6.1 GET POST
    path('rest/generics_list/', views.generics_list.as_view()),

    # 6.2 GET put delete
    path('rest/generics_pk/<int:pk>', views.generics_pk.as_view()),

    # ViewSets
    path('rest/viewsets/', include(router.urls)),

    # Find_Movies
    path('fbv/findmovie/' , views.find_movie) ,
    # new reservation
    path('fbv/new_reservation/' , views.new_reservation)


]
