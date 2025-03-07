from rest_framework import serializers

from users.models import Customer, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'phone',
            'email',
            'password',
            'avatar',
            'date_joined',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser'
        ]


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
