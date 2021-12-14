from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from backend.app.ChatBot.models import Chat, Client, Message
from backend.app.users.models import User
from backend.app.users.serializers import UserSerializer


class clientUserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, write_only=True)
    phone_number = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name',
                  'email', 'password', 'phone_number']

    def validate(self, data):
        client_ = User.objects.filter(email=data.get("email"))
        if client_:
            raise ValidationError('a client has already this email')
        isphonetaken = User.objects.filter(
            phone_number=data.get("phone_number"))
        if isphonetaken:
            raise ValidationError('phone number already taken')
        return data

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.pop('password')
        print("validated data..", validated_data)
        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                        password=password)
        user.save()
        client = Client.objects.create(user=user, **validated_data)
        client.save()
        return client


class MessageSerializer(serializers.ModelSerializer):
    client = UserSerializer()
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Message
        fields = ['id', 'body', 'client', 'result', 'createdAt',
                  'updatedAt']

    def get_created_at(self, instance):

        return str(instance.created_at)

    def get_updated_at(self, instance):
        return str(instance.updated_at)


class MessageCreateSerializer(serializers.ModelSerializer):
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Message
        fields = ['id', 'body', 'result', 'client', 'createdAt',
                  'updatedAt']

    def get_created_at(self, instance):
        return str(instance.created_at)

    def get_updated_at(self, instance):
        return str(instance.created_at)


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Chat
        fields = ['id', 'owner', 'messages', ]
