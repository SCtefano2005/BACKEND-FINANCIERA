from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrContadorOrGerente(BasePermission):
    """
    Permiso personalizado para permitir acceso a administradores, contadores, y gerentes con diferentes niveles de acceso.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.rol == 'ADMIN':
            return True
        
        # Permisos para Contador
        if request.user.rol == 'CONTADOR':
            if request.method in SAFE_METHODS:  # Permite GET, HEAD, OPTIONS
                return True
            if request.method == 'POST':  # Puede crear nuevos recursos
                return True
            if request.method == 'PUT' or request.method == 'PATCH':  # Puede actualizar recursos existentes
                return True

        # Permisos para Gerente (solo puede listar y ver)
        if request.user.rol == 'GERENTE':
            if request.method in SAFE_METHODS:  # SAFE_METHODS incluye 'GET', 'HEAD', 'OPTIONS'
                return True

        # Si no cumple ninguna condición, deniega el acceso
        return False

    def has_object_permission(self, request, view, obj):
        """
        Define permisos de nivel de objeto si el usuario puede realizar una acción específica sobre un objeto.
        """
        # Administrador tiene permiso completo sobre cualquier objeto
        if request.user.rol == 'ADMIN':
            return True

        # Contador puede actualizar o ver objetos, pero no eliminarlos
        if request.user.rol == 'CONTADOR':
            if request.method in SAFE_METHODS:  # Puede ver el objeto
                return True
            if request.method in ['PUT', 'PATCH']:  # Puede editar el objeto
                return True

        # Gerente solo puede ver objetos, pero no editar ni eliminar
        if request.user.rol == 'GERENTE':
            if request.method in SAFE_METHODS:  # Puede ver el objeto
                return True

        # Si no cumple ninguna condición, deniega el acceso al objeto
        return False
