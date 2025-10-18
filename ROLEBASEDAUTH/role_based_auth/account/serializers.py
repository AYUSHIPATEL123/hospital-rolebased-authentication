from rest_framework import serializers
from .models import User,AdminProfile,DoctorProfile,PatientProfile,Mapping,StaffProfile
from .tasks import send_email
class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLES, required=True)
    admin_id = serializers.CharField(required=False,allow_blank=True)
    specialization = serializers.CharField(required=False,allow_blank=True)
    license_number = serializers.CharField(required=False,allow_blank=True)
    hospital = serializers.CharField(required=False,allow_blank=True)
    department = serializers.CharField(required=False,allow_blank=True)
    medical_history  = serializers.CharField(required=False,allow_blank=True)
    date_of_birth = serializers.DateField(required=False)
    blood_group = serializers.CharField(required=False,allow_blank=True)
    city = serializers.CharField(required=False,allow_blank=True)
    state = serializers.CharField(required=False,allow_blank=True)
    employee_id = serializers.CharField(required=False,allow_blank=True)
    doctor = serializers.PrimaryKeyRelatedField(queryset=DoctorProfile.objects.all(),required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email','password',
        'role','admin_id','specialization','license_number','hospital','department',
        'medical_history','date_of_birth','blood_group','city', 'state','employee_id','doctor'
       ]
        extra_kwargs = {
            'password':{"write_only":True},
        }

    def validate(self, data):
        if data['role'] == "Admin" and not data.get('admin_id'):
            raise serializers.ValidationError({"message":"admin_id is required"})
        elif data['role'] == "Doctor" and not all([data.get('specialization'), data.get('license_number'), data.get('hospital'), data.get('department')]):
            raise serializers.ValidationError({"message":"specialization, license Number, hospital, department are required"})
        elif data['role'] == "Patient" and not all([data.get('medical_history'), data.get('date_of_birth'), data.get('blood_group'), data.get('city'), data.get('state')]):
            raise serializers.ValidationError({"message":"Medical History, Date of Birth, Blood Group, City, State are required"})
        elif data['role'] == "Staff" and not all([data.get('employee_id'), data.get('doctor')]):
            raise serializers.ValidationError({"message":"employee_id and doctor are required"})
        return data
    
    def create(self, validated_data):  
        user = User.objects.create_user(username=validated_data['username'],email=validated_data['email'],first_name=validated_data['first_name'],last_name=validated_data['last_name'],password=validated_data['password'],role=validated_data['role']) 
        user.save()
        role = validated_data.get('role')
        if role == "Admin":
            admin_id = validated_data.pop('admin_id','')
            AdminProfile.objects.create(user=user,admin_id=admin_id).save()
        
        elif role == "Doctor":
            specialization = validated_data.pop('specialization','')
            license_number = validated_data.pop('license_number','')
            hospital = validated_data.pop('hospital','')
            department = validated_data.pop('department','')
            DoctorProfile.objects.create(user=user,specialization=specialization,license_number=license_number,hospital=hospital,department=department).save()
        elif role == "Patient":
            medical_history = validated_data.pop('medical_history','')
            date_of_birth = validated_data.pop('date_of_birth')
            blood_group = validated_data.pop('blood_group','')
            city = validated_data.pop('city','')
            state = validated_data.pop('state','')
            PatientProfile.objects.create(user=user,medical_history=medical_history,date_of_birth=date_of_birth,blood_group=blood_group,city=city,state=state).save()
        elif role == "Staff":
            employee_id = validated_data.pop('employee_id','')
            doctor = validated_data.pop('doctor',None)
            StaffProfile.objects.create(user=user,employee_id=employee_id,doctor=doctor).save()
        send_email.delay(user.pk)    
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AdminSerializer(serializers.ModelSerializer):
    class Meta: 
        model = AdminProfile
        fields = ['id','user','admin_id']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['id','user','specialization','license_number','hospital','department']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['id','user','medical_history','date_of_birth','blood_group','city','state']

class StaffSerializer(serializers.ModelSerializer):
    doctor_details = DoctorSerializer(source='doctor',read_only=True)
    class Meta:
        model = StaffProfile
        fields = ['id','user','employee_id','doctor','doctor_details']        
class MappingSerializer(serializers.ModelSerializer):
    doctor_details = DoctorSerializer(source='doctor',read_only=True)
    patient_details = PatientSerializer(source='patient',read_only=True)
    class Meta:
        model = Mapping
        fields = ['id','mapping_id','remarks','patient','doctor','patient_details','doctor_details']
                                
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id','first_name','last_name','username','email','role']
    
    def to_representation(self, instance):
        profile = None
        data = super().to_representation(instance)
        if instance.role == "Admin":
            profile = AdminProfile.objects.filter(user=instance).first()
            if profile:
                data['profile'] = AdminSerializer(profile).data
        elif instance.role == "Docter":
            profile = DoctorProfile.objects.filter(user=instance).first()
            if profile:
                data['profile'] = DoctorSerializer(profile).data
        elif instance.role == "Patient":
            profile = PatientProfile.objects.filter(user=instance).first()
            if profile:
                data['profile'] = PatientSerializer(profile).data
        elif instance.role == "Staff":
            profile = StaffProfile.objects.filter(user=instance).first()
            if profile:
                data['profile'] = StaffSerializer(profile).data        
        return data

        