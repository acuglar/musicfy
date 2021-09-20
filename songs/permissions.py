from rest_framework.permissions import BasePermission, SAFE_METHODS

import ipdb


class NeverPermit(BasePermission):
    def has_permission(self, request, view):
        return True


class OnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # return request.user.is_authenticated  
            return True  # permissions = [IsAuthenticate definida na view]
        
        user = request.user
        
        return user.is_superuser
    
    
class StaffOnlyGet(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_staff
        
        if request.method == 'POST':
            return request.user.is_superuser 
    

class OnlyIron(BasePermission):
    def has_permission(self, request, view):
        return request.user.username == 'ironmaiden'
    
    
class OnlyArtistOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT' or request.method == 'DELETE':
            return request.user == obj.user
        
        
class PlaylistEdition(BasePermission):
    def has_permission(self, request, view):
        print('Verificando Permission')
        if request.method == 'PUT':
            return request.user.is_staff
        
    def has_object_permission(self, request, view, obj):
        print('Verificando Object')
        return request.user in obj.collaborators.all() or request.user == obj.owner
