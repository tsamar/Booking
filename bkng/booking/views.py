from django.shortcuts import render
from rest_framework import viewsets,generics, status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User, MasterProfile, Schedule, Booking
from .serializer import UserSerializer, MasterProfileSerializer, MasterProfileCreateSerializer,\
     ScheduleSerializer, BookingSerializer, ScheduleCreateSerializer, BookingCreateSerializer
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser, IsUserHasMasterProfile, IsUserOwner
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
   HTTP_400_BAD_REQUEST,
   HTTP_404_NOT_FOUND,
   HTTP_200_OK
)
from rest_framework.response import Response

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
       return Response({'error': 'Please provide both username and password'},
                       status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
       return Response({'error': 'Invalid Credentials'},
                       status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                   status=HTTP_200_OK)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListView(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class = UserSerializer
    # class_pagination = CompanyListPagination


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    

class MasterProfileView(generics.RetrieveAPIView):
    queryset = MasterProfile.objects.all()
    serializer_class = MasterProfileSerializer
    


class MyMasterListView(generics.ListAPIView):
    serializer_class = MasterProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return MasterProfile.objects.filter(user=self.request.user)


class MasterProfileCreateView(generics.CreateAPIView):
    serializer_class = MasterProfileCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUserHasMasterProfile)

    def get_serializer_context(self):
        context = super(MasterProfileCreateView, self).get_serializer_context()
        context.update({ "user": self.request.user})
        return context

class ScheduleView(generics.ListAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.filter(master__user=self.request.user)
    

class ScheduleCreateView(generics.CreateAPIView):
    serializer_class = ScheduleCreateSerializer
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated, IsUserHasMasterProfile, IsUserOwner)

    def get_serializer_context(self):
        context = super(ScheduleCreateView, self).get_serializer_context()
        context.update({ "master": self.request.user.profile})
        return context

class BookingView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(master__user=self.request.user)


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer

    # def get_serializer_context(self):
    #     context = super(BookingCreateView, self).get_serializer_context()
    #     context.update({'schedule_booking': self.request.user.profile})
    #     return context






