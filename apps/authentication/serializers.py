
from rest_framework import serializers
from .models import Agency, CustomUser, Permission, Profile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # N'incluez pas forcément 'username' si vous ne souhaitez pas qu'il soit modifié depuis l'extérieur.
        fields = (
            'first_name',
            'email',
            'phone',
            'type',
            'profile',
            'job',
            'location',
            'agency',
            'picture',
            'reset_pwd',
            'permissions',
            'created_by',
            'country',
            # Ajoutez d'autres champs si nécessaire
        )
        extra_kwargs = {
            # Vous pouvez rendre le champ username en lecture seule pour ne pas le considérer dans les données entrantes
            'username': {'read_only': True},
        }

    def create(self, validated_data):
        # On ignore le username envoyé par le client et on le définit sur la valeur de l'email
        validated_data['username'] = validated_data.get('email')
        return super().create(validated_data)
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'