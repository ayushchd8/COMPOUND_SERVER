from .base import BaseModel
from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
from django.utils import timezone

class Compound(BaseModel):
    name = models.CharField(max_length=255)
    smiles = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='compounds', on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(
        User,
        through='SharedCompound',
        through_fields=('compound', 'user'),
        related_name='shared_compounds',
    )

    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

auditlog.register(Compound)

class SharedCompound(models.Model):
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(null=True, blank=True)

    def has_expired(self):
        if self.expiration_time and timezone.now() > self.expiration_time:
            return True
        return False

    def __str__(self):
        return f'{self.compound.name} shared with {self.user.username}'

auditlog.register(SharedCompound)
