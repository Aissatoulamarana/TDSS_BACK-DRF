from rest_framework.permissions import BasePermission

class IsAdminOrCanViewAll(BasePermission):
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est un super utilisateur, admin ou TDSS
        if request.user.is_superuser or request.user.profile.type.code == 'ADMIN' or request.user.type.code == 'TDSS':
            return True
        return False

class IsClientOrAgent(BasePermission):
    def has_permission(self, request, view):
        # L'utilisateur peut voir ses propres factures
        if request.user.profile.type.code == 'AGENT' or request.user.profile.type.code == 'CLIENT':
            return True
        return False
