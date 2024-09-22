from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from compounds.models.compound import Compound, SharedCompound
from compounds.serializers.compound import CompoundSerializer, SharedCompoundSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

# List and Create Compounds
class CompoundListView(generics.ListCreateAPIView):
    serializer_class = CompoundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        query = self.request.query_params.get('q', None)
        
        # Get compounds owned by the user
        owned_compounds = Compound.objects.filter(owner=user)

        # Get active shared compounds
        shared_compound_ids = SharedCompound.objects.filter(
            user=user
        ).exclude(
            expiration_time__isnull=False,
            expiration_time__lte=timezone.now()
        ).values_list('compound_id', flat=True)

        shared_compounds = Compound.objects.filter(id__in=shared_compound_ids)

        # Filter by search query if provided
        if query:
            owned_compounds = owned_compounds.filter(Q(name__icontains=query) | Q(smiles__icontains=query))
            shared_compounds = shared_compounds.filter(Q(name__icontains=query) | Q(smiles__icontains=query))

        return owned_compounds | shared_compounds

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompoundUpdateView(generics.UpdateAPIView):
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only update compounds they own
        return Compound.objects.filter(owner=self.request.user)

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompoundDeleteView(generics.DestroyAPIView):
    serializer_class = CompoundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Compound.objects.filter(owner=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Compound deleted successfully"}, status=status.HTTP_200_OK)

# Share Compound with another User
class ShareCompoundView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompoundSerializer

    def post(self, request, *args, **kwargs):
        compound_id = kwargs.get('pk')
        user_id = request.data.get('user_id')

        # Validate the inputs
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            compound = Compound.objects.get(id=compound_id)
        except Compound.DoesNotExist:
            return Response({"error": "Compound not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if compound.owner != request.user:
            return Response({"error": "Only the owner can share the compound."}, status=status.HTTP_403_FORBIDDEN)

        # Set expiration time to one week from now
        expiration_time = timezone.now() + timedelta(weeks=1)

        # Create or update the SharedCompound entry
        shared_compound, created = SharedCompound.objects.update_or_create(
            compound=compound,
            user=user,
            defaults={'expiration_time': expiration_time}
        )

        action = "created" if created else "updated"
        return Response({
            "message": f"Compound share {action} successfully.",
            "compound_id": str(compound.id),
            "shared_with_user_id": user.id,
            "expiration_time": expiration_time,
            "is_new_share": created
        }, status=status.HTTP_200_OK)
    
# Search Compounds by SMILES or Name
class SearchCompoundView(generics.ListAPIView):
    serializer_class = CompoundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        query = self.request.query_params.get('q', None)

        # Compounds owned by the user
        owned_compounds = Compound.objects.filter(owner=user)

        # Shared compounds
        shared_compound_ids = SharedCompound.objects.filter(
            user=user
        ).exclude(
            expiration_time__isnull=False,
            expiration_time__lte=timezone.now()
        ).values_list('compound_id', flat=True)

        shared_compounds = Compound.objects.filter(id__in=shared_compound_ids)

        if query:
            # Filter by name or SMILES
            owned_compounds = owned_compounds.filter(Q(name__icontains=query) | Q(smiles__icontains=query))
            shared_compounds = shared_compounds.filter(Q(name__icontains=query) | Q(smiles__icontains=query))

        return owned_compounds | shared_compounds