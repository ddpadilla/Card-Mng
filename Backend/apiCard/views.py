from rest_framework import generics, status
from rest_framework.response import Response
from .models import User, ParkingCard
from .serializers import RegistrationSerializer, UnifiedResponseSerializer, UnifiedUpdateSerializer


class UserDetailView(generics.RetrieveAPIView):
    """
    Gather unified information of a user by their ID
    """
    serializer_class = UnifiedResponseSerializer
    lookup_field = 'id_user'
    lookup_url_kwarg = 'user_id'
    queryset = User.objects.all()


class CardDetailView(generics.RetrieveAPIView):
    """
    Gather unified information of a user by their card number
    """
    serializer_class = UnifiedResponseSerializer
    lookup_field = 'card_number'
    lookup_url_kwarg = 'card_number'
    queryset = ParkingCard.objects.all()


class UserUpdateView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id_user'
    lookup_url_kwarg = 'user_id'
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UnifiedUpdateSerializer
        return UnifiedResponseSerializer


class CardUpdateView(generics.RetrieveUpdateAPIView):
    lookup_field = 'card_number'
    lookup_url_kwarg = 'card_number'
    queryset = ParkingCard.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UnifiedUpdateSerializer
        return UnifiedResponseSerializer


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        unified_serializer = UnifiedResponseSerializer(result['user'])
        return Response(unified_serializer.data, status=status.HTTP_201_CREATED)