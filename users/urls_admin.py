import debug_toolbar
from django.urls import include, path
from users.views_admin import *


app_name = "admin"

urlpatterns = [
    path('', admin, name="index"),
    path('__debug__/', include(debug_toolbar.urls)),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name="user_create"),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', delete_user, name='user_delete'),
    
    path('roles/', RoleListView.as_view(), name='role_list'),
    path('roles/create/', RoleCreateView.as_view(), name="role_create"),
    path('roles/<int:pk>/update/', RoleUpdateView.as_view(), name='role_update'),
    path('roles/<int:pk>/delete/', delete_role, name='role_delete'),
    
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create/', GroupCreateView.as_view(), name="group_create"),
    path('groups/<int:pk>/update/', GroupUpdateView.as_view(), name='group_update'),
    path('groups/<int:pk>/delete/', delete_group, name='group_delete'),
]
