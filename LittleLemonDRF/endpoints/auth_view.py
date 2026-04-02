from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomTokenCreateView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # This uses DRF's built-in validation for username/password
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Returns the exact format you need
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })