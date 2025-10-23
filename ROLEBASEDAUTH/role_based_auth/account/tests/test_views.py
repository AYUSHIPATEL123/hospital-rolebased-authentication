from rest_framework.test import APITestCase , APIClient
from django.urls import reverse
from account.models import User,PatientProfile,AdminProfile,DoctorProfile,Mapping,StaffProfile
class WeeklyReminderViewTestCase(APITestCase):
    def test_weekly_reminder_view(self):
        response = self.client.get(reverse('weekly_reminder'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('weekly reminder', response.content.decode())
        self.assertTrue('✅ Weekly reminder task created.',response.content.decode())

class RegisterViewTestCase(APITestCase):
    def test_register_view(self):
        url = '/api/register/'
        data = {
            'username':'testuser',
            'email':'testuser@example.com',
            'first_name':'Test',    
            'last_name':'User',
            'password': 'testpassword',
            'role':'Patient',
            'medical_history':'No significant history',
            'date_of_birth':'1990-01-01',       
            'blood_group':'O+',
            'city':'TestCity',
            'state':'TestState'
        }
        response = self.client.post(url,data=data,format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')                            
        self.assertEqual(response.data['role'], 'Patient')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')
        self.assertNotIn('password', response.data)         
        
        
class LoginViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword', first_name='Test', last_name='User', role='Patient')
        PatientProfile.objects.create(user=self.user, medical_history='No significant history', date_of_birth='1990-01-01', blood_group='O+', city='TestCity', state='TestState')
        self.client = APIClient()
    def test_login_view(self):
        url = '/api/login/'
        data = {
            'username':'testuser',
            'password':'testpassword'
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertEqual(response.data['data']['username'], 'testuser')
        self.assertEqual(response.data['data']['email'],'testuser@example.com')
        self.assertTrue(self.user.check_password('testpassword'))

class AdminViewSetTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='adminuser', email='admin@example.com', password='adminpass', role='Admin')
        self.admin_profile = AdminProfile.objects.create(user=self.admin_user, admin_id='12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
    
    def test_adminprofile_view(self):
        url = f'/api/admin/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['admin_id'], '12345')
        self.assertEqual(response.data[0]['user'], self.admin_user.id)
        
class PatientViewSetTestCase(APITestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user(username='patientuser',password='patientpass',role='Patient',email='patient@example.com')
        self.patient_profile = PatientProfile.objects.create(user=self.patient_user,medical_history='No allergies',date_of_birth='1990-01-01',blood_group='O+',city='TestCity',state='TestState')
        self.client = APIClient()
        self.client.force_authenticate(user=self.patient_user)
        
    
    def test_patientprofile_view(self):
        url = f'/api/patient/{self.patient_profile.id}/'  
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['medical_history'], 'No allergies')
        self.assertEqual(response.data['user'], self.patient_user.id)
        self.assertEqual(response.data['date_of_birth'], '1990-01-01')
        self.assertEqual(response.data['blood_group'], 'O+')
        self.assertEqual(response.data['city'], 'TestCity')
        self.assertEqual(response.data['state'], 'TestState')

class DoctorViewSetTestCase(APITestCase):
    def setUp(self):
        self.doctor_user = User.objects.create_user(username='doctoruser',password='doctorpass',role='Doctor',email='doctor@example.com')
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor_user,specialization='Cardiology',license_number='LIC123',hospital='City Hospital',department='Cardio')
        self.client = APIClient()
        self.client.force_authenticate(user=self.doctor_user)

    def test_doctorprofile_view(self):
        url = f'/api/doctor/{self.doctor_profile.id}/'
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['user'],self.doctor_user.id)
        self.assertEqual(response.data['specialization'],'Cardiology') # 'secialization'
        self.assertEqual(response.data['license_number'],'LIC123')
        self.assertEqual(response.data['hospital'],'City Hospital')
        self.assertEqual(response.data['department'],'Cardio')

class StaffViewSetTestCase(APITestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staffuser',password='staffpass',role='Staff',email='staff@example.com')
        self.doctor_user = User.objects.create_user(username='doctoruser2',password='doctorpass2',role='Doctor',    email='doctor@example.com')
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor_user,specialization='Cardiology',license_number='LIC123',hospital='City Hospital',department='Cardio')
        self.staff_profile = StaffProfile.objects.create(user=self.staff_user,employee_id='EMP123',doctor=self.doctor_profile)
        self.client = APIClient()
        self.client.force_authenticate(user=self.staff_user)
    def test_staffprofile_view(self):
        url = f'/api/staff/{self.staff_profile.id}/'
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['user'],self.staff_user.id)
        self.assertEqual(response.data['employee_id'],'EMP123')
        self.assertEqual(response.data['doctor'],self.doctor_profile.id)
    
    
class MappingViewSetTestCase(APITestCase):
    def setUp(self):
        self.doctor_user = User.objects.create_user(username='doctoruser',password='doctorpass',role='Doctor',email='doctor@example.com')
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor_user,specialization='Cardiology',license_number='LIC123',hospital='City Hospital',department='Cardio')
        self.patient_user = User.objects.create_user(username='patientuser',password='patientpass',role='Patient',email='patient@example.com')
        self.patient_profile = PatientProfile.objects.create(user=self.patient_user,medical_history='No allergies',date_of_birth='1990-01-01',blood_group='O+',city='TestCity',state='TestState')
        self.mapping = Mapping.objects.create(doctor=self.doctor_profile,patient=self.patient_profile,remarks='Regular checkup')
        self.client = APIClient()
        self.client.force_authenticate(user=self.doctor_user)
    def test_mapping_view(self):
        url = f'/api/mapping/{self.mapping.id}/'
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['doctor'],self.doctor_profile.id)
        self.assertEqual(response.data['patient'],self.patient_profile.id)
        self.assertEqual(response.data['remarks'],'Regular checkup')