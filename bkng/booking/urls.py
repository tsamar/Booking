from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, UserListView, UserCreateView, MasterProfileView,\
    MyMasterListView, MasterProfileCreateView, login, ScheduleView, \
        BookingCreateView, ScheduleCreateView, BookingView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/', include('rest_auth.urls')),
    path('regist/', UserCreateView.as_view(), name='registration'),
    path('login/', login, name='login'),
    path('userslist/', UserListView.as_view(), name='userslist'),
    path('master/<int:pk>/', MasterProfileView.as_view(), name='profiledetails'),
    path('mymaster/', MyMasterListView.as_view(), name='mymaster'),
    path('newprofile/', MasterProfileCreateView.as_view(), name='create_new_profile'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('bookingcreate/', BookingCreateView.as_view(), name='bookingcreate'),
    path('booking/', BookingView.as_view(), name='booking'),
    path('schedule/create/', ScheduleCreateView.as_view(), name='schedule_create'),
]