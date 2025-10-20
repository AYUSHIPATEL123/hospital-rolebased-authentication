from rest_framework.test import APITestCase , APIClient
from django.urls import reverse
from account.models import User,PatientProfile,AdminProfile
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
        