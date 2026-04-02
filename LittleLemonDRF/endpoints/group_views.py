from django.contrib.auth.models import User, Group
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..permissions import IsManager
from ..serializers import UserSerializer

class GroupUserView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    serializer_class = UserSerializer

    def get_queryset(self):
        # Dynamically filter group based on the URL path
        group_name = 'Manager' if 'manager' in self.request.path else 'Delivery-Crew'
        return User.objects.filter(groups__name=group_name)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        group_name = 'Manager' if 'manager' in self.request.path else 'Delivery-Crew'
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        return Response({"message": "User added to group"}, status=status.HTTP_201_CREATED)

class GroupUserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsManager]

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        group_name = 'Manager' if 'manager' in self.request.path else 'Delivery-Crew'
        group = Group.objects.get(name=group_name)
        user.groups.remove(group)
        return Response({"message": "User removed from group"}, status=status.HTTP_200_OK)