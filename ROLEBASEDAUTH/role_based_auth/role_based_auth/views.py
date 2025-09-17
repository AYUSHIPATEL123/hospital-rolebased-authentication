from rest_framework.response import Response
from rest_framework.views import APIView
class HomeView(APIView):
    def get(self, request):
        data = {
            "api": "role_based_auth",
            "version": "1.0.0"
        }
        return Response(data) 