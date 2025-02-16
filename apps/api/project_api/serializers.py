from rest_framework import serializers
from apps.projects.models import Project, Milestone
from apps.accounts.models import CustomUser
from apps.customers.models import Customer
from apps.employes.models import Employee

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'
        read_only_fields = ['completion_date']

    def validate(self, data):
        project = self.context['project']
        if data['start_date'] < project.start_date:
            raise serializers.ValidationError("Milestone start date cannot be before project start")
        if data['due_date'] > project.due_date:
            raise serializers.ValidationError("Milestone due date cannot be after project deadline")
        return data

class ProjectSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all()
    )
    customer = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Customer.objects.all()
    )
    employees = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Employee.objects.all(),
        write_only=True,
        required=False
    )
    milestones = MilestoneSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'manager', 'customer',
            'total_amount', 'remaining_amount', 'start_date', 'due_date',
            'priority', 'status', 'document', 'employees', 'milestones', 'progress'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_progress(self, obj):
        total = obj.milestones.count()
        completed = obj.milestones.filter(status='completed').count()
        return round((completed / total) * 100) if total > 0 else 0

    def validate(self, data):
        if data['start_date'] > data['due_date']:
            raise serializers.ValidationError("Due date must be after start date")
        if data['remaining_amount'] > data['total_amount']:
            raise serializers.ValidationError("Remaining amount cannot exceed total amount")
        return data

    def create(self, validated_data):
        employees = validated_data.pop('employees', [])
        project = Project.objects.create(**validated_data)
        project.employees.set(employees)
        return project