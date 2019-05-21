from rest_framework import serializers
from .models import User, MasterProfile, ServiceType, Schedule, Booking
from django.contrib.auth.hashers import make_password

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('time','date','phonenumber','remarks')


class MasterProfileSerializer(serializers.ModelSerializer):
    services = serializers.StringRelatedField(many=True)
    class Meta:
        model = MasterProfile
        # booking = BookingSerializer(many=True)
        fields = ('full_name', 'address', 'phone', 'profile_photo', 'gallery', \
            'services','schedule', 'book')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'], \
            username=validated_data['username'], password=make_password(validated_data['password']))
        return user


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('service_type', 'id')


class MasterProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterProfile
        services = ServiceTypeSerializer(many=True)
        fields = ('full_name', 'address', 'phone', 'profile_photo', 'gallery', 'services')

    def create(self, validated_data):
        owner = self.context.get('user')
        services = validated_data.pop('services')
        profile = MasterProfile.objects.create(user=owner, **validated_data)
        for service in services:
            # instance = ServiceType.objects.get(**service).first()
            profile.services.add(service)
        profile.save()
        return profile


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        booking = BookingSerializer(many=True)
        fields = ('starttime','endtime','booking')


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('starttime','endtime')

    def create(self, validated_data):
        owner = self.context.get('master')
        schedule = Schedule.objects.create(master=owner, **validated_data)
        schedule.save()
        return schedule

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('time','date','phonenumber', 'remarks')


class BookingCreateSerializer(serializers.ModelSerializer):
    phonenumber = serializers.CharField(required=True)
    class Meta:
        model = Booking
        fields = ('time','date','phonenumber', 'remarks')

    def create(self, validated_data):
        schedule = self.context.get('schedule_booking')
        booking = Booking.objects.create(schedule_booking=schedule, **validated_data)
        booking.save()
        return booking

