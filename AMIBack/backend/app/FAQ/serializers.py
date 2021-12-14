from rest_framework import exceptions, serializers

from backend.app.FAQ.models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')
    class Meta:
        model = FAQ
        fields = ['id', 'content','count', 'createdAt','updatedAt']

    def get_created_at(self, instance):
        print("instance ...",instance)
        return str(instance.created_at)

    def get_updated_at(self, instance):
        return str(instance.updated_at)
class FAQCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'content','count']
