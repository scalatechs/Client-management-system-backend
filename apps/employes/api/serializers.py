from rest_framework import serializers
from apps.employes import Employee, Contract, EmployeeWorkHistory

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

class EmployeeWorkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeWorkHistory
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    contracts = ContractSerializer(read_only=True)  # One-to-one relationship
    work_history = EmployeeWorkHistorySerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    email = serializers.CharField(source='user.email', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 'full_name', 'position', 'email', 'phone', 'address',
            'date_joined', 'contracts', 'work_history', 'image', 'image_url'
        ]

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None