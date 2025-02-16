from rest_framework import serializers
from apps.customers.models import Customer, Interaction, CustomerProject
from apps.api.project_api.serializers import ProjectSerializer  
from apps.api.accounnts_api.serializers import CustomUserSerializer

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'
        read_only_fields = ['date']

    def validate(self, data):
        if data['customer'].status == 'inactive':
            raise serializers.ValidationError("Cannot add interaction for inactive customers")
        return data

class CustomerProjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = CustomerProject
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    interactions = InteractionSerializer(many=True, read_only=True)
    projects = CustomerProjectSerializer(many=True, read_only=True, source='customer_projects')
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id', 'user', 'name', 'email', 'phone', 'website', 'status',
            'last_interaction', 'next_session', 'total_spend',
            'address', 'image', 'image_url', 'interactions', 'projects'
        ]
        read_only_fields = ['last_interaction', 'total_spend']

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def validate_status(self, value):
        if value == 'inactive' and self.instance and self.instance.projects.exists():
            raise serializers.ValidationError("Cannot set status to inactive with active projects")
        return value