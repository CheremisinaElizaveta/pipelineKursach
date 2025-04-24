# from django.contrib import admin
# from django.utils.translation import gettext_lazy as _
# from tests.models import Activity, Category, QuestionType, Test
# from users.models import Tendency, Personality


# class PsychologistAdminSite(admin.AdminSite):
#     site_header = _('Панель психолога')

#     def has_permission(self, request):
#         return request.user.is_active and request.user.role.name.lower() in ['психолог', 'админ']
    
# psychologist_admin_site = PsychologistAdminSite(name='psychologist_admin')
    

# class FullAccessModelAdmin(admin.ModelAdmin):
#     def has_module_permission(self, request):
#         return True

#     def has_view_permission(self, request, obj=None):
#         return True

#     def has_add_permission(self, request):
#         return True

#     def has_change_permission(self, request, obj=None):
#         return True

#     def has_delete_permission(self, request, obj=None):
#         return True

#     def get_model_perms(self, request):
#         return {
#             'add': True,
#             'change': True,
#             'delete': True,
#             'view': True,
#         }
    

# @admin.register(Activity, site=psychologist_admin_site)
# class ActivityAdmin(FullAccessModelAdmin): pass
# @admin.register(Category, site=psychologist_admin_site)
# class CategoryAdmin(FullAccessModelAdmin): pass
# @admin.register(Tendency, site=psychologist_admin_site)
# class TendencyAdmin(FullAccessModelAdmin): pass
# @admin.register(Personality, site=psychologist_admin_site)
# class PersonalityAdmin(FullAccessModelAdmin): pass
# @admin.register(QuestionType, site=psychologist_admin_site)
# class QuestionTypeAdmin(FullAccessModelAdmin): pass
# @admin.register(Test, site=psychologist_admin_site)
# class TestAdmin(FullAccessModelAdmin): pass
