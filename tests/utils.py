from django.http import Http404
from tests.models import AssigningTest, Test, TestResult
from django.shortcuts import get_object_or_404


def custom_get_object(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if (test.trial and TestResult.objects.filter(test=test, user=request.user).exists()) or \
    (not AssigningTest.objects.filter(user=request.user, test=test).exists()):
        raise Http404()
    
    return test
