from rest_framework import serializers
from apps.customers.models import Customer, Interaction

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    interactions = InteractionSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'email', 'phone', 'website',
            'status', 'last_interaction', 'next_session', 'interactions', 'image', 'image_url'
        ]

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None