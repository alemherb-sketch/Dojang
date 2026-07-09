from rest_framework import serializers
from users.models import User
from academy.models import Grade, Section, Activity
from attendance.models import Attendance
from billing.models import Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'qr_code')

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    section_name = serializers.CharField(source='section.name', read_only=True)
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ('id', 'date', 'time', 'status', 'section_name', 'student_name')
        
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}".strip() or obj.student.username
