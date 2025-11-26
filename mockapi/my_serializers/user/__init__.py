from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from mockapi.models.customer import Customer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializerDetails(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()

    def get_is_admin(self, obj):
        return obj.is_staff

    def __init__(self, *args, **kwargs):
        excluded_fields = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)
        if excluded_fields:
            current_fields = list(self.fields.keys())
            for field_name in excluded_fields:
                if field_name in current_fields:
                    self.fields.pop(field_name)

    class Meta:
        model = User
        fields = '__all__'


class UserSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = '__all__'

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        password = validated_data.get('password')
        if password is not None:
            instance.set_password(password)
            instance.save()

        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = { 
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializerPost(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        customer = Customer(user=user)
        customer.save()
        return user
