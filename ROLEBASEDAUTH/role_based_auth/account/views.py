from django.shortcuts import render
from .serializers import RegisterSerializer , UserProfileSerializer ,LoginSerializer,PatientSerializer,AdminSerializer,DoctorSerializer,MappingSerializer,StaffSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets,status
from rest_framework.permissions import AllowAny
from .models import User,PatientProfile,AdminProfile,DoctorProfile,Mapping,StaffProfile
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from .permissions import IsAdmin,IsPatient,IsDoctor,IsOwnerOrAdmin,IsDoctorOrAdmin,IsDoctorOrAdminOrPatient,IsDoctorOrAdminOrPatientOrStaff,IsDoctorOrAdminOrStaff
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from .tasks import send_email,add
from django_celery_beat.models import PeriodicTask,CrontabSchedule
# Create your views here.

def home(request):
    add.delay(4,5)
    # add(4,5)
    return HttpResponse("<h1>hello..v..</h1>")
def weekly_reminder_view(request):
    schedule, created = CrontabSchedule.objects.get_or_create(hour=13,minute=45,week_of_month='*',day_of_week='*',day_of_month='*',month_of_year='*')
    task = PeriodicTask.objects.create(crontab=schedule,name="weekly-reminder-task",task="account.tasks.weekly_reminder")
    return HttpResponse("<h1>weekly reminder set</h1>")

class RegisterView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    
    
class LoginView(APIView):
    permission_classes = [AllowAny]    
    def post(self, request):
        data=request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            raise Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=serializer.validated_data.get('username'),password=serializer.validated_data.get('password'))
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'data':UserProfileSerializer(user).data,"refresh_token":str(refresh),"access_token":access_token},status=status.HTTP_200_OK)
        else:
            return Response({'message':'invalid credentials'},status=status.HTTP_400_BAD_REQUEST)
        
class AdminViewSet(viewsets.ModelViewSet):
    serializer_class = AdminSerializer
    # queryset = AdminProfile.objects.all()
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action == 'create':
            return [IsAdmin()]
        elif self.action in ['update','partial_update']:
            return [IsAdmin()]
        elif self.action == 'retrieve':
            return [IsAdmin()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        elif self.action == 'list':
            return [IsAdmin()]
        return [IsAdmin()]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == "Admin":
            return AdminProfile.objects.filter(user=user)
        else:
            return AdminProfile.objects.none()        
class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    # queryset = DoctorProfile.objects.all()
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action == 'create':
            return [IsAdmin()]
        elif self.action in ['update','partial_update']:
            return [IsDoctorOrAdmin()]
        elif self.action == 'retrieve':
            return [IsDoctorOrAdmin()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        elif self.action == 'list':
            return [IsAdmin()]
        return [IsAdmin()]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == "Admin":
            return DoctorProfile.objects.all()
        elif user.role == "Doctor":
            return DoctorProfile.objects.filter(user=user)
        else:
            return DoctorProfile.objects.none()
        
class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    # queryset  = StaffProfile.objects.all()
    permission_classes = [IsAuthenticated]
    
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAdmin()]
        elif self.action in ['update','partial_update']:
            return [IsDoctorOrAdminOrStaff()]
        elif self.action == 'retrieve':
            return [IsDoctorOrAdminOrStaff()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        elif self.action == 'list':
            return [IsDoctorOrAdminOrStaff()]
        return [IsAdmin()]
    
    def get_queryset(self):
        user = self.request.user
        doctor = DoctorProfile.objects.filter(user=self.request.user).first()
        if user.role == "Admin":
            return StaffProfile.objects.all()
        elif user.role == "Doctor":
            return StaffProfile.objects.filter(doctor=doctor)
        elif user.role == "Staff":
            return StaffProfile.objects.filter(user=user)
        else:
            return StaffProfile.objects.none()
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    # queryset = PatientProfile.objects.all()
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action == 'create':
            return [IsAdmin()]
        elif self.action in ['update','partial_update']:
            return [IsDoctorOrAdminOrPatientOrStaff()]
        elif self.action == 'retrieve':
            return [IsDoctorOrAdminOrPatientOrStaff()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        elif self.action == 'list':
            return [IsDoctorOrAdminOrStaff()]
        return [IsAdmin()]

    def get_queryset(self):
        user = self.request.user
        doctor = DoctorProfile.objects.filter(user=self.request.user).first()
        if user.role == "Admin":
            return PatientProfile.objects.all()
        elif user.role == "Doctor":
            return PatientProfile.objects.all()
        elif user.role == "Patient":
            return PatientProfile.objects.filter(user=user)
        else:
            return PatientProfile.objects.none()

class MappingViewSet(viewsets.ModelViewSet):
    # queryset = Mapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action == 'create':
            return [IsDoctorOrAdminOrStaff()]
        elif self.action in ['update','partial_update']:
            return [IsDoctorOrAdminOrStaff()]
        elif self.action == 'retrieve':
            return [IsDoctorOrAdminOrPatientOrStaff()]
        elif self.action == 'destroy':
            return [IsDoctorOrAdmin()]
        elif self.action == 'list':
            return [IsDoctorOrAdminOrPatientOrStaff()] 
        else:
            return [IsAdmin()] 
             
    def get_queryset(self):
        doctor = DoctorProfile.objects.filter(user=self.request.user).first()
        user = self.request.user
        if user.role == "Admin":
            return Mapping.objects.all()
        elif user.role == "Doctor":
            return Mapping.objects.filter(doctor = doctor)
        elif user.role == "Patient":
            return Mapping.objects.filter(patient = PatientProfile.objects.filter(user=user).first()) 
        elif user.role == "Staff":
            return Mapping.objects.filter(doctor = StaffProfile.objects.filter(user=user).first().doctor) 
        return Mapping.objects.none()
