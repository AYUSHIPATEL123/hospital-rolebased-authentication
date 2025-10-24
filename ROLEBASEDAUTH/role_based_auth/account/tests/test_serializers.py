from django.test import TestCase,Client
from account.serializers import RegisterSerializer, LoginSerializer, AdminSerializer, UserProfileSerializer, DoctorSerializer, PatientSerializer, StaffSerializer,MappingSerializer
from account.models import User, AdminProfile, DoctorProfile, PatientProfile, StaffProfile,Mapping

class SerializerTestCase(TestCase):
    
    def test_register_serializer(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'role': 'Patient',
            'medical_history': 'No known allergies',
            'date_of_birth': '1990-01-01',
            'blood_group': 'O+',
            'city': 'Test City',
            'state': 'Test State'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['username'], data['username'])
        self.assertEqual(serializer.validated_data['role'], data['role'])
    def test_register_serializer_invalid_role(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'role': 'InvalidRole',
            'medical_history': 'No known allergies',
            'date_of_birth': '1990-01-01',
            'blood_group': 'O+',
            'city': 'Test City',
            'state': 'Test State'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('role', serializer.errors)
    def test_user_profile_serializer(self):
        user = User.objects.create_user(username='testuser',password='testpass123',role='Patient')
        serializer = UserProfileSerializer(user)
        self.assertEqual(serializer.data['username'], user.username)
        self.assertEqual(serializer.data['role'], user.role)    
    
    def test_login_serializer(self):
        User.objects.create_user(username='testuser', password='testpass123')
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            } 
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
    def test_admin_serializer(self):
        user = User.objects.create_user(username='adminuser',password='adminpass',role='Admin')
        admin_serializer = AdminSerializer(data={'user':user.id,'admin_id':'ADM001'})
        self.assertTrue(admin_serializer.is_valid(),admin_serializer.errors)
        self.assertEqual(admin_serializer.validated_data['admin_id'],'ADM001')
    
    def test_doctor_serializer(self):
        user = User.objects.create_user(username='doctoruser',password='doctorpass',role='Doctor')
        # doctor_profile = DoctorProfile.objects.create(user=user,specialization='Cardiology',license_number='LIC1234',hospital='City Hospital',department='Cardiology')
        doctor_serializer = DoctorSerializer(data={'user':user.id,'specialization':'Cardiology','license_number':'LIC123','hospital':'City Hospital','department':'Cardiology'})
        self.assertTrue(doctor_serializer.is_valid(),doctor_serializer.errors)
        self.assertEqual(doctor_serializer.validated_data['specialization'],'Cardiology')
        self.assertEqual(doctor_serializer.validated_data['license_number'],'LIC123')
        self.assertEqual(doctor_serializer.validated_data['hospital'],'City Hospital')
        self.assertEqual(doctor_serializer.validated_data['department'],'Cardiology')
        
    def test_staff_serializer(self):
        doctor_user = User.objects.create_user(username='doctoruser',password='doctorpass',role='Doctor')
        doctor_profile = DoctorProfile.objects.create(user=doctor_user,specialization='Cardiology',license_number='LIC1234',hospital='City Hospital',department='Cardiology')
        doctor_details = DoctorSerializer(source='doctor_profile',read_only=True)
        staff_user = User.objects.create_user(username='staffuser',password='staffpass',role='Staff')
        staff_serializer = StaffSerializer(data={'user':staff_user.id,'employee_id':'EMP123','doctor':doctor_profile.id,'doctor_details':doctor_details})    
        self.assertTrue(staff_serializer.is_valid(),staff_serializer.errors)
        self.assertEqual(staff_serializer.validated_data['employee_id'],'EMP123')
        self.assertEqual(staff_serializer.validated_data['doctor'],doctor_profile)
    
    def test_patient_serializer(self):
        user = User.objects.create_user(username='patientuser',password='patientpass',role='Patient')
        patient_serializer = PatientSerializer(data={'user':user.id,'medical_history':'No known allergies','date_of_birth':'1990-01-01','blood_group':'O+','city':'Test City','state':'Test State'})
        self.assertTrue(patient_serializer.is_valid(),patient_serializer.errors)
        self.assertEqual(patient_serializer.validated_data['medical_history'],'No known allergies')
        self.assertEqual(str(patient_serializer.validated_data['date_of_birth']),'1990-01-01')
        self.assertEqual(patient_serializer.validated_data['blood_group'],'O+')
        self.assertEqual(patient_serializer.validated_data['city'],'Test City')
        self.assertEqual(patient_serializer.validated_data['state'],'Test State')
    
    def test_mapping_serializer(self):
        patient_user = User.objects.create_user(username='patientuser',password='patientpass',role='Patient')
        doctor_user = User.objects.create_user(username='doctoruser',password='doctorpass',role='Doctor')
        doctor_profile = DoctorProfile.objects.create(user=doctor_user,specialization='Cardiology',license_number='LIC1234',hospital='City Hospital',department='Cardiology')
        patient_profile = PatientProfile.objects.create(user=patient_user,medical_history='No known allergies',date_of_birth='1990-01-01',blood_group='O+',city='Test City',state='Test State')     
        doctor_details = DoctorSerializer(source='doctor',read_only=True)
        patient_details = PatientSerializer(source='patient',read_only=True)
        mapping_serializer = MappingSerializer(data={'patient':patient_profile.id,'doctor':doctor_profile.id,'patient_details':patient_details,'doctor_details':doctor_details,'remarks':'Initial Consultation'})  
        self.assertTrue(mapping_serializer.is_valid(),mapping_serializer.errors)
        self.assertEqual(mapping_serializer.validated_data['patient'],patient_profile)
        self.assertEqual(mapping_serializer.validated_data['doctor'],doctor_profile)
        self.assertEqual(mapping_serializer.validated_data['remarks'],'Initial Consultation')