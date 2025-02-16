from rest_framework import serializers
from .models import Complaint
from apps.api.project_api.serializers import ProjectSerializer
from apps.api.accounnts_api.serializers import CustomUserSerializer

class ComplaintSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Complaint
        fields = [
            'id', 'project', 'user', 'title', 'description', 
            'category', 'priority', 'status', 'attachment', 'date_filed'
        ]
        read_only_fields = ['user', 'date_filed']

class CreateComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = [
            'project', 'title', 'description', 
            'category', 'priority', 'attachment'
        ]

    def validate_project(self, value):
        if not value.customer_projects.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError("You don't have access to this project")
        return value