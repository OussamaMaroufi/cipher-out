# -*- coding: utf-8 -*

from __future__ import unicode_literals
from django.http import HttpResponse

import logging
from importlib import import_module
from backend.app.ChatBot.models import Message
from django.conf import settings
from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

engine = import_module(settings.SESSION_ENGINE)
SessionStore = engine.SessionStore

logger = logging.getLogger('django.request')


class AnonymousSessionMiddleware:
    # pass
    def __init__(self, get_response):
        
        self.get_response = self.get_response

    def __call__(self, request):
        return self.get_response(request)

#     def process_request(self, request):
#         if request.user.is_anonymous:
#             request.session = SessionStore()
#             request.session.create()
#             process_anonymous_session(request)
#             return HttpResponse('Ann', status.HTTP_404_NOT_FOUND)
#         else:
#             return HttpResponse('Not Anon', status.HTTP_404_NOT_FOUND)
# def process_anonymous_session(request):
#     print('session',dir(request.session))
#     request.session["messages"] = []
#     new_msg = Message(body="helllo")
#     request.session["messages"].append("hello")
