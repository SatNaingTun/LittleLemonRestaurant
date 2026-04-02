from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
# Import the serializer you already created
from ..serializers import UserSerializer 

class UserRegistrationView(APIView):
    """
    Endpoint: POST /api/users
    Purpose: Creates a new user with name, email and password
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return 201 Created on success
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    """
    Endpoint: GET /api/users/users/me/
    Purpose: Displays only the current user based on Token
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # request.user is automatically populated by the Token in the header
        serializer = UserSerializer(request.user)
        return Response(serializer.data)