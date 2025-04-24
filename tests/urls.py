from django.urls import include, path
from tests.views import *
import debug_toolbar

app_name = "tests"

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('students/report/<int:personality_id>/', generate_student_report, name='generate_report'),
    path('create/', create, name="create"),
    path('add_result/<int:test_id>/', add_result, name="add_result"),
    path('add_question/<int:test_id>/', add_question, name="add_question"),
    path('update_question/<int:question_id>/', update_question, name='update_question'),
    path('assign_test/<int:test_id>/', assign_test, name="assign_test"),
    path('show_test/<int:test_id>/', show_test, name="show_test"),
    path('questions_test/<int:test_id>/', questions_test, name="questions_test"),
    path('test_result/<int:test_id>/', test_result, name="test_result"),
    path('personal_type/<int:personality_id>/', personal_type, name="personal_type"),
    path('students_list', students_list, name="students_list"),
    path('test_results_chart', test_results_chart, name="test_results_chart"),
    path("questions_list/<int:test_id>/", questions_list, name="questions_list"),
    path("delete_question/<int:question_id>/", delete_question, name="delete_question")
]
