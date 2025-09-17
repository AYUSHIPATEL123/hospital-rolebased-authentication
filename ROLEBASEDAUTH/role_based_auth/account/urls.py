from django.urls import path,include
from .views import RegisterView,LoginView,PatientViewSet,DoctorViewSet,MappingViewSet,AdminViewSet,StaffViewSet,home
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework import routers
router = routers.DefaultRouter()
router.register('register',RegisterView,basename='register')
router.register('patient',PatientViewSet,basename='patient')
router.register('doctor',DoctorViewSet,basename='doctor')
router.register('admin',AdminViewSet,basename='admin')
router.register('staff',StaffViewSet,basename='staff')
router.register('mapping',MappingViewSet,basename='mapping')

urlpatterns = [
    path('',include(router.urls)),
    path('home/',home,name='home'),
    path('login/',LoginView.as_view(),name='login'),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
]
