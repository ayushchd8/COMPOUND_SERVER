from django.contrib import admin
from compounds.models.compound import Compound, SharedCompound

@admin.register(Compound)
class CompoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    search_fields = ('name', 'owner__username')

@admin.register(SharedCompound)
class SharedCompoundAdmin(admin.ModelAdmin):
    list_display = ('compound', 'user', 'shared_at', 'expiration_time')
    search_fields = ('compound__name', 'user__username')