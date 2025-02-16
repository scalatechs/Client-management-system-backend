# employees/serializers.py
from rest_framework import serializers
from apps.employes.models import Employee, Contract, EmployeeProjectAssignment
from apps.api.accounnts_api.serializers import CustomUserSerializer
from apps.accounts.models import CustomUser

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ['employee']

class EmployeeProjectAssignmentSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    
    class Meta:
        model = EmployeeProjectAssignment
        fields = '__all__'
        read_only_fields = ['employee']

class EmployeeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # Remove write_only=True
    contracts = ContractSerializer(read_only=True)
    assignments = EmployeeProjectAssignmentSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
   
    
    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'phone', 'address', 'position',
            'date_joined', 'image_url', 'contracts', 'assignments',
        
        ]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        return Employee.objects.create(user=user, **validated_data)

class EmployeeDetailSerializer(EmployeeSerializer):
    projects = serializers.SlugRelatedField(
        many=True,
        slug_field='title',
        read_only=True,
        source='project_assignments.project'
    )