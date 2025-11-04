from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models.customer import Customer
from .models.product import Product


# from tudushnik.models.tag import Tag
# from tudushnik.models.task import Task


class DefaultValueSerializerMixin:
    def get_fields(self):
        fields = super().get_fields()
        # for field_name, field in fields.items():
        #     model_field = self.Meta.model._meta.get_field(field_name)
        #     if hasattr(model_field, 'default'):
        #         field.default = model_field.default
        return fields


class ProductSerializer(DefaultValueSerializerMixin,
                        serializers.ModelSerializer):
    class Meta:
        model = Product
        # read_only_fields = ('owner',)
        fields = '__all__'

    # def create(self, validated_data):
    #     # validated_data['owner_id'] = self.context.get('request').user.pk
    #     # tags = validated_data.pop('tags')
    #     product = Product.objects.create(**validated_data)
    #     # if not isinstance(tags, NOT_PROVIDED):
    #     #     task.tags.set(tags)
    #     task.save()
    #     return task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # read_only_fields = ('last_login', 'is_active', 'date_joined', 'groups')
        # exclude = (
        #     'password', 'is_staff', 'is_superuser', 'user_permissions',
        #     'groups')


class UserSerializerDetails(serializers.ModelSerializer):
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
        # read_only_fields = (
        #     'last_login', 'is_active', 'date_joined', 'user_permissions',
        #     'is_staff', 'is_superuser',)
        fields = '__all__'


class UserSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        # read_only_fields = (
        #     'is_staff', 'is_superuser', 'user_permissions',
        #     'last_login', 'is_active', 'date_joined', 'groups')
        # exclude = ('is_staff', 'is_superuser', 'user_permissions',
        #            'last_login', 'is_active', 'date_joined',
        #            )
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
