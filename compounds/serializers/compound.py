from rest_framework import serializers
from compounds.models.compound import Compound, SharedCompound
from django.contrib.auth.models import User
from django.utils import timezone

class SharedCompoundSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    has_expired = serializers.SerializerMethodField()

    class Meta:
        model = SharedCompound
        fields = ['user', 'shared_at', 'expiration_time', 'has_expired']

    def get_has_expired(self, obj):
        return obj.has_expired()

class CompoundSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    shared_with = SharedCompoundSerializer(source='sharedcompound_set', many=True, read_only=True)

    class Meta:
        model = Compound
        fields = ['id', 'name', 'smiles', 'owner', 'shared_with', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']