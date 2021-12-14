import pickle
import random
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras
import numpy as np
import json
import os
# from django.contrib.auth.models import User
from django.http.response import JsonResponse
from backend.app.ChatBot.models import Chat, Client, Message
from backend.app.ChatBot.serializers import (ChatSerializer,
                                             MessageCreateSerializer,
                                             MessageSerializer)
from django.shortcuts import render
from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.contrib.auth import get_user_model
User = get_user_model()


# ML dependencies
###############################################
##################################################


class ChatViewSet(viewsets.ModelViewSet):
    """ For Chat conv with bot """
    serializer_class = ChatSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Chat.objects.filter(owner__pk=-1)
        else:
            return Chat.objects.filter(owner__pk=user.pk)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    # permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return MessageCreateSerializer
        else:
            return MessageSerializer


MESSAGES = []

@api_view(['POST'])
def sendMessage(request):
    print("request...", request.session.items(),request.session.modified,dir(request.session))
    # session id ...
    print(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.dirname(os.path.abspath(__file__))+'/ML/test.json') as file:
        data = json.load(file)

    # load trained model
    model = keras.models.load_model(os.path.dirname(
        os.path.abspath(__file__))+'/ML/chat_model')

    # load tokenizer object
    with open(os.path.dirname(os.path.abspath(__file__))+'/ML/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

        # load label encoder object
    with open(os.path.dirname(os.path.abspath(__file__))+'/ML/label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

     # parameters
    # max_len = 20

    _body = request.data.get('body', '')
    result = model.predict(keras.preprocessing.sequence.pad_sequences(
        tokenizer.texts_to_sequences([_body]), truncating='post', maxlen=20))
    print("result is", result)

    tag = lbl_encoder.inverse_transform([np.argmax(result)])
    message = ''
    for i in data['intents']:
        if i['tag'] == tag:
            message = np.random.choice(i['responses'])
    if request.user.is_anonymous:
        MESSAGES.append({
                "body": _body,
                "result": message
            })

            # print(dir(new_msg),new_msg.serializable_value)
        return JsonResponse(MESSAGES, safe=False)
    else:

        chat = Chat.objects.get(owner__pk=request.user.id)
        # if we get client
        # create new message
        if chat:
                
            new_msg = Message(body=_body, client=request.user, result=message)
            new_msg.save()

            if new_msg:
                chat.messages.add(new_msg)
                return Response("sent", status=status.HTTP_201_CREATED)
            else:
                return Response('error', status=status.HTTP_400_BAD_REQUEST)
        else:
                    
            ch = Chat(owner=request.user.id)
            ch.save()
            new_msg = Message(body=_body, client=request.user.id, result=message)
            # new_msg_bot = Message(result=message,client=client)
            new_msg.save()
            # new_msg_bot.save()
            if new_msg:
                ch.messages.add(new_msg)
                # ch.messages.add(new_msg_bot)
                return Response("sent", status=status.HTTP_201_CREATED)
            else:
                return Response('error', status=status.HTTP_400_BAD_REQUEST)

