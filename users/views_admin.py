from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from users.forms import UserForm, RoleForm, GroupForm
from users.models import User, Role, UserGroup as Group
import logging

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def admin(request):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Логируем открытие страницы
    logging.info(f"Пользователь '{request.user.username}' открыл страницу администратора")
    return render(request, "users/admin/admin_index.html")

# users
@method_decorator(user_passes_test(is_superuser), name="dispatch")
class UserListView(ListView):
    model = User
    template_name = 'users/admin/users/user_list.html'
    context_object_name = 'users'

    def get(self, request, *args, **kwargs):
        # Логируем открытие страницы
        logging.info(f"Пользователь '{request.user.username}' открыл список пользователей")
        return super().get(request, *args, **kwargs)

@method_decorator(user_passes_test(is_superuser), name="dispatch")
class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/admin/users/user_form.html'
    success_url = reverse_lazy('admin:user_list')

    def form_valid(self, form):
        # Логируем создание пользователя
        logging.info(f"Пользователь '{self.request.user.username}' создал нового пользователя '{form.instance.username}'")
        return super().form_valid(form)

@method_decorator(user_passes_test(is_superuser), name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/admin/users/user_form.html'
    success_url = reverse_lazy('admin:user_list')

    def form_valid(self, form):
        # Логируем обновление пользователя
        logging.info(f"Пользователь '{self.request.user.username}' обновил информацию о пользователе '{form.instance.username}'")
        return super().form_valid(form)

@user_passes_test(is_superuser)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    # Логируем удаление пользователя
    logging.info(f"Пользователь '{request.user.username}' удалил пользователя '{user.username}'")
    user.delete()
    return redirect('admin:user_list')

# roles
@method_decorator(user_passes_test(is_superuser), name="dispatch")
class RoleListView(ListView):
    model = Role
    template_name = 'users/admin/roles/role_list.html'
    context_object_name = 'roles'

    def get(self, request, *args, **kwargs):
        # Логируем открытие страницы
        logging.info(f"Пользователь '{request.user.username}' открыл список ролей")
        return super().get(request, *args, **kwargs)

@method_decorator(user_passes_test(is_superuser), name="dispatch")
class RoleCreateView(CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'users/admin/roles/role_form.html'
    success_url = reverse_lazy('admin:role_list')

    def form_valid(self, form):
        # Логируем создание роли
        logging.info(f"Пользователь '{self.request.user.username}' создал новую роль '{form.instance.name}'")
        return super().form_valid(form)

@method_decorator(user_passes_test(is_superuser), name="dispatch")
class RoleUpdateView(UpdateView):
    model = Role
    form_class = RoleForm
    template_name = 'users/admin/roles/role_form.html'
    success_url = reverse_lazy('admin:role_list')

    def form_valid(self, form):
        # Логируем обновление роли
        logging.info(f"Пользователь '{self.request.user.username}' обновил роль '{form.instance.name}'")
        return super().form_valid(form)

@user_passes_test(is_superuser)
def delete_role(request, pk):
    role = get_object_or_404(Role, pk=pk)
    # Логируем удаление роли
    logging.info(f"Пользователь '{request.user.username}' удалил роль '{role.name}'")
    role.delete()
    return redirect('admin:role_list')

# groups
@method_decorator(user_passes_test(is_superuser), name="dispatch")
class GroupListView(ListView):
    model = Group
    template_name = 'users/admin/groups/group_list.html'
    context_object_name = 'groups'

    def get(self, request, *args, **kwargs):
        # Логируем открытие страницы
        logging.info(f"Пользователь '{request.user.username}' открыл список групп")
        return super().get(request, *args, **kwargs)

@method_decorator(user_passes_test(is_superuser), name="dispatch")
class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'users/admin/groups/group_form.html'
    success_url = reverse_lazy('admin:group_list')

    def form_valid(self, form):
        # Логируем создание группы
        logging.info(f"Пользователь '{self.request.user.username}' создал новую группу '{form.instance.name}'")
        return super().form_valid(form)

@method_decorator(user_passes_test(is_superuser), name="dispatch")
class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'users/admin/groups/group_form.html'
    success_url = reverse_lazy('admin:group_list')

    def form_valid(self, form):
        # Логируем обновление группы
        logging.info(f"Пользователь '{self.request.user.username}' обновил группу '{form.instance.name}'")
        return super().form_valid(form)

@user_passes_test(is_superuser)
def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    # Логируем удаление группы
    logging.info(f"Пользователь '{request.user.username}' удалил группу '{group.name}'")
    group.delete()
    return redirect('admin:group_list')
