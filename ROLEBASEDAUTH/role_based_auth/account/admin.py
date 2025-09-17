from django.contrib import admin
from .models import User,AdminProfile,DoctorProfile,PatientProfile,Mapping,StaffProfile
# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','role','first_name','last_name']

admin.site.register(User,UserProfileAdmin)

class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','admin_id']

admin.site.register(AdminProfile,AdminProfileAdmin)

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','specialization','license_number','hospital','department']

admin.site.register(DoctorProfile,DoctorProfileAdmin)

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','employee_id','doctor']
    

admin.site.register(StaffProfile,StaffProfileAdmin)    
    
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','medical_history','date_of_birth','blood_group','city','state']

admin.site.register(PatientProfile,PatientProfileAdmin)

class MappingAdmin(admin.ModelAdmin):
    list_display = ['id','mapping_id','patient','doctor','remarks']

admin.site.register(Mapping,MappingAdmin)
