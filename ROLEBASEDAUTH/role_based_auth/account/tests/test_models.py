from django.test import TestCase
from account.models import User, AdminProfile, DoctorProfile, PatientProfile , StaffProfile , Mapping



class UserModelTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@example.com', password='adminpass')    
        self.admin_profile = AdminProfile.objects.create(user=self.admin_user, admin_id='12345')
    
    def test_admin_profile_creation(self):
        self.assertEqual(self.admin_profile.user.username,'adminuser')
        self.assertEqual(self.admin_profile.admin_id,'12345')
        self.assertEqual(self.admin_profile.user.email,'admin@example.com')
        self.assertTrue(self.admin_profile.user.check_password('adminpass'))
    
    def test_doctor_profile_creation(self):
        doctor_user = User.objects.create_user(username='doctoruser',email='doctor@example.com',password='doctorpass',role='Doctor')
        doctor_profile = DoctorProfile.objects.create(user=doctor_user,specialization='Cardiology',license_number='LIC123',hospital='City Hospital',department='Cardio')  
        self.assertEqual(doctor_profile.user.username,'doctoruser')
        self.assertEqual(doctor_profile.specialization,'Cardiology')
        self.assertEqual(doctor_profile.user.email,'doctor@example.com')
        self.assertTrue(doctor_profile.user.check_password('doctorpass'))
        self.assertEqual(doctor_profile.license_number,'LIC123')
        self.assertEqual(doctor_profile.hospital,'City Hospital')
        self.assertEqual(doctor_profile.department,'Cardio')  
    
    def test_staff_profile_creation(self):
        staff_user = User.objects.create_user(username='staffuser',email='staff@example.com',password='staffpass',role='Staff')
        doctor_user = User.objects.create_user(username='doctortostaff',email='doctortostaff@example.com',password='doctortostaffpass',role='Doctor')
        doctor_profile = DoctorProfile.objects.create(user=doctor_user,specialization='Neurology',license_number='LIC456',hospital='General Hospital',department='Neuro')
        staff_profile = staff_profile = StaffProfile.objects.create(user=staff_user,employee_id='EMP123',doctor=doctor_profile)     
        
        self.assertEqual(staff_profile.user.username,'staffuser')
        self.assertEqual(staff_profile.employee_id,'EMP123')
        self.assertEqual(staff_profile.user.email,'staff@example.com')
        self.assertTrue(staff_profile.user.check_password('staffpass'))
        self.assertEqual(staff_profile.doctor.user.username,'doctortostaff') 
    
    def test_patient_profile_creation(self):
        patient_user = User.objects.create_user(username='patientuser',email='patient@example.com',password='patientpass',role='Patient')
        patient_profile = PatientProfile.objects.create(user=patient_user,medical_history='No allergis',date_of_birth='1990-01-01',blood_group='O+',insurance_number='INS123',city='New York',state='NY')    
        
        self.assertEqual(patient_profile.user.username,'patientuser')
        self.assertEqual(patient_profile.medical_history,'No allergis')
        self.assertEqual(str(patient_profile.date_of_birth),'1990-01-01')       
        self.assertEqual(patient_profile.blood_group,'O+')
        self.assertEqual(patient_profile.insurance_number,'INS123')
        self.assertEqual(patient_profile.city,'New York')       
        self.assertEqual(patient_profile.state,'NY')
        self.assertEqual(patient_profile.user.email,'patient@example.com')
        self.assertTrue(patient_profile.user.check_password('patientpass')) 
        
    def test_mapping_creation(self):
        doctor_user = User.objects.create_user(username='mappingdoctor',email='mappingdoctor@example.com',password='mappingdoctorpass',role='Doctor')
        doctor_profile = DoctorProfile.objects.create(user=doctor_user,specialization='Dermatology',license_number='LIC789',hospital='Skin Hospital',department='Dermato')
        patient_user = User.objects.create_user(username='mappingpatient',email='mappingpatient@example.com',password='mappingpatientpass',role='Patient')
        patient_profile = PatientProfile.objects.create(user=patient_user,medical_history='Eczema',date_of_birth='1985-05-05',blood_group='A+',insurance_number='INS456',city='Los Angeles',state='CA')
        mapping = Mapping.objects.create(patient=patient_profile,doctor=doctor_profile,remarks='Initial Consultation')
        
        self.assertEqual(mapping.patient.user.username,'mappingpatient')
        self.assertEqual(mapping.doctor.user.username,'mappingdoctor')
        self.assertEqual(mapping.remarks,'Initial Consultation')
        self.assertEqual(mapping.patient.user.username,'mappingpatient')
        