from rest_framework import permissions

class IsOwnerOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 읽기 권한 요청이 들어오면 허용
        if obj.owner == request.user:
            return True
        
        # 요청자(request.user)가 객체의 user와 동일한지 확인
        else:
            PermissionError
    