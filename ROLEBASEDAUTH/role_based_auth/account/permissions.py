from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == "Admin"

class IsDoctor(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == "Doctor"

class IsPatient(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == "Patient"

class IsDoctorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["Admin","Doctor"]
class IsDoctorOrAdminOrPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["Admin","Doctor","Patient"]  
class IsDoctorOrAdminOrPatientOrStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["Admin","Doctor","Patient",'Staff']  

class IsDoctorOrAdminOrStaff(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role in ["Admin","Doctor","Staff"]          
class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self,request,view,obj):
        if request.user.role == "Admin":
            return True
        return hasattr(obj, 'user') and obj.user == request.user    
            