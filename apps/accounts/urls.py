from django.urls import path, include

app_name = 'accounts'

urlpatterns = [
    path('v1/', include(('apps.accounts.api.v1.urls', 'v1'), namespace='v1')),
    # Add v2 when it's ready
    # path('v2/', include(('apps.accounts.api.v2.urls', 'v2'), namespace='v2')),
]