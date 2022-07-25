
from django.contrib import admin
from django.urls import path
from CinemaTicketsReservation import views

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

]
