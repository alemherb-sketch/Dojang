from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from academy.models import Activity
from attendance.models import Attendance
from billing.models import Payment
from .serializers import UserSerializer, ActivitySerializer, PaymentSerializer, AttendanceSerializer

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.filter(is_active=True).order_by('-date_posted')
    serializer_class = ActivitySerializer
    permission_classes = [permissions.AllowAny] # Can be restricted if needed

class StudentDashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def payments(self, request):
        payments = Payment.objects.filter(student=request.user).order_by('-year', '-month')
        return Response(PaymentSerializer(payments, many=True).data)

    @action(detail=False, methods=['get'])
    def attendance(self, request):
        user = request.user
        if user.role == 'PARENT':
            attendances = Attendance.objects.filter(student__parent=user).order_by('-date', '-time')[:30]
        else:
            attendances = Attendance.objects.filter(student=user).order_by('-date', '-time')[:30]
        return Response(AttendanceSerializer(attendances, many=True).data)
