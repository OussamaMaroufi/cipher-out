from backend.app.FAQ.models import FAQ
from backend.app.FAQ.serializers import FAQCreateSerializer, FAQSerializer
from rest_framework import exceptions, permissions, status, viewsets


class FAQViewSet(viewsets.ModelViewSet):
    """ FAQ for AMI assurance  clinets ... """
    queryset = FAQ.objects.all()
    permissions_class=[permissions.AllowAny]
    # def get_permissions(self):
    #     if self.action in ["list", "retrieve"]:
    #         permission_classes = [permissions.AllowAny]
    #     else:
    #         permission_classes = [permissions.IsAuthenticated]
    #     return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return FAQCreateSerializer
        else:
            return FAQSerializer
