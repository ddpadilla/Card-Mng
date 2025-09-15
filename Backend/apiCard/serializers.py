from rest_framework import serializers
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.db import transaction
from .models import User, ParkingCard, Vehicle, Document


class UnifiedResponseSerializer(serializers.Serializer):
    """
    Serializer for the unified flat response structure. read-only.
    """
    id_user = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    card_number = serializers.CharField(read_only=True)
    state = serializers.CharField(read_only=True)
    car_plate = serializers.CharField(read_only=True)
    brand = serializers.CharField(read_only=True)
    authorization_document = serializers.FileField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance):
        """
        Extracts the relation of all models to return a flat structure.
        """
        if isinstance(instance, User):
            user = instance
            try:
                card = user.parkingcard
                vehicle = card.vehicle_set.first()
                document = card.document_set.first()
            except ParkingCard.DoesNotExist:
                card = vehicle = document = None
        elif isinstance(instance, ParkingCard):
            card = instance
            user = card.id_user
            vehicle = card.vehicle_set.first()
            document = card.document_set.first()
        else:
            return {}
        
        return {
            'id_user': user.id_user if user else None,
            'full_name': user.full_name if user else None,
            'card_number': card.card_number if card else None,
            'state': card.state if card else None,
            'car_plate': vehicle.car_plate if vehicle else None,
            'brand': vehicle.brand if vehicle else None,
            'authorization_document': document.authorization_document.url if document and document.authorization_document else None,
            'created': user.created if user else None,
            'updated': user.updated if user else None,
        }


class RegistrationSerializer(serializers.Serializer):
    id_user = serializers.CharField(max_length=20, validators=[MinLengthValidator(13)])
    full_name = serializers.CharField(max_length=100)
    card_number = serializers.CharField(max_length=8, validators=[MinLengthValidator(6)])
    state = serializers.ChoiceField(choices=ParkingCard.STATE_CHOICES, default='active')
    car_plate = serializers.CharField(max_length=8, validators=[MinLengthValidator(6)])
    brand = serializers.CharField(max_length=50)
    authorization_document = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    def validate(self, data):
        """
        Verify that unique fields are not already in use.
        """
        if User.objects.filter(id_user=data['id_user']).exists():
            raise serializers.ValidationError(f"User id {data['id_user']} already registered.")
        
        if ParkingCard.objects.filter(card_number=data['card_number']).exists():
            raise serializers.ValidationError(f"Card number {data['card_number']} already in use.")

        if Vehicle.objects.filter(car_plate=data['car_plate']).exists():
            raise serializers.ValidationError(f"Vehicle plate {data['car_plate']} already registered.")
            
        return data

    @transaction.atomic
    def create(self, validated_data):
        """
        Method to create all related objects in a single transaction ACID.
        """
        # 1. Create user
        user = User.objects.create(
            id_user=validated_data['id_user'],
            full_name=validated_data['full_name']
        )
        
        # 2. Create parking card
        card = ParkingCard.objects.create(
            card_number=validated_data['card_number'],
            id_user=user,
            state=validated_data['state']
        )
        
        # 3. Create vehicle
        vehicle = Vehicle.objects.create(
            car_plate=validated_data['car_plate'],
            card_number=card,
            brand=validated_data['brand']
        )
        
        # 4. Create document
        document = Document.objects.create(
            card_number=card,
            authorization_document=validated_data['authorization_document']
        )
        return {
            'user': user,
            'card': card,
            'vehicle': vehicle,
            'document': document
        }


class UnifiedUpdateSerializer(serializers.Serializer):
    """
    Serializer to update fields across User, ParkingCard, and Vehicle models.
    """
    # Fields that can be updated
    full_name = serializers.CharField(max_length=100, required=False)
    state = serializers.ChoiceField(choices=ParkingCard.STATE_CHOICES, required=False)
    car_plate = serializers.CharField(max_length=8, validators=[MinLengthValidator(6)], required=False)
    brand = serializers.CharField(max_length=50, required=False)
    
    # Read-only fields to identify the records
    id_user = serializers.CharField(read_only=True)
    card_number = serializers.CharField(read_only=True)

    def validate_car_plate(self, value):
        """
        Verify that the car plate is unique, excluding the current vehicle if updating.
        """
        if hasattr(self, 'instance'):
            if isinstance(self.instance, User):
                current_vehicle = getattr(getattr(self.instance, 'parkingcard', None), 'vehicle_set', None)
                current_vehicle = current_vehicle.first() if current_vehicle else None
            elif isinstance(self.instance, ParkingCard):
                current_vehicle = self.instance.vehicle_set.first()
            else:
                current_vehicle = None
            
            # Verify uniqueness excluding the current vehicle
            existing = Vehicle.objects.filter(car_plate=value)
            if current_vehicle:
                existing = existing.exclude(car_plate=current_vehicle.car_plate)
            
            if existing.exists():
                raise serializers.ValidationError(f"Plate {value} already registered.")
        
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Instance can be either User or ParkingCard. Function with transaction ACID
        """
        # 1. Identify related instances
        if isinstance(instance, User):
            user = instance
            try:
                card = user.parkingcard
            except ParkingCard.DoesNotExist:
                card = None
        elif isinstance(instance, ParkingCard):
            card = instance
            user = getattr(card, 'id_user', None)
        else:
            raise serializers.ValidationError("Instance not valid for update.")

        vehicle = card.vehicle_set.first() if card else None
        # 2. Actualizar los campos en cada modelo si los datos vienen en la petición
        if user and 'full_name' in validated_data:
            user.full_name = validated_data['full_name']
            user.save()
            
        if card and 'state' in validated_data:
            card.state = validated_data['state']
            card.save()

        if vehicle:
            vehicle_updated = False
            if 'car_plate' in validated_data:
                vehicle.car_plate = validated_data['car_plate']
                vehicle_updated = True
            if 'brand' in validated_data:
                vehicle.brand = validated_data['brand']
                vehicle_updated = True
            
            if vehicle_updated:
                vehicle.save()
        return instance