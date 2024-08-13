from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_routes(request):
    routes = {
        "Auth Endpoints": {
            "User Registration": "/api/v1/auth/users/",
            "User Login (JWT)": "/api/v1/auth/jwt/create/",
            "User Logout (JWT)": "/api/v1/auth/token/blacklist/",
            "Token Refresh": "/api/v1/auth/jwt/refresh/",
            "User Activation": "/api/v1/auth/users/activation/",
            "Password Reset": "/api/v1/auth/users/reset_password/",
            "Password Reset Confirm": "/api/v1/auth/users/reset_password_confirm/",
            "Resend Activation": "/api/v1/auth/users/resend_activation/",
            "Set New Password": "/api/v1/auth/users/set_password/",
            "User Profile": "/api/v1/auth/users/me/",
            "Delete User": "/api/v1/auth/users/{id}/",
            "User List (Admin)": "/api/v1/auth/users/",
            "User Detail (Admin)": "/api/v1/auth/users/{id}/",
        }
    }
    return Response(routes)