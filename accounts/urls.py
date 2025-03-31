from django.urls import path, include
from .views import sign_up, login_view, logout_view,role_based_redirect, admin_users_view, change_role, delete_user, deactivate_user



# Each entry follows this pattern path('URL_PATTERN/', VIEW_FUNCTION, name='URL_NAME')
# 'URL_PATTERN/' defines the URL endpoint.
# VIEW_FUNCTION is the Python function that handles the request.
# name='URL_NAME' is an optional parameter used for reverse URL lookups in templates.
urlpatterns = [
    path('sign-up/', sign_up, name='sign_up'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Include Django AllAuth URLs (needed for Microsoft login)
    path('accounts/', include('allauth.urls')),

    # Include social authentication URLs for Microsoft login
    path('auth/', include('social_django.urls', namespace='social')),
    path('role_redirect/', role_based_redirect, name='role_redirect'),
    path('admin/users/', admin_users_view, name='admin_users'), # accounts url
    path('staff/users/', admin_users_view, name='staff_users'), # accounts url


    
    path('admin/users/change_role/<int:user_id>/', change_role, name='change_role'),
    path('admin/users/deactivate/<int:user_id>/', deactivate_user, name='deactivate_user'),  # FIX
    path('admin/users/delete/<int:user_id>/', delete_user, name='delete_user'),
]
