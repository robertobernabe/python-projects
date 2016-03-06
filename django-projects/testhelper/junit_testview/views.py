from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import TestRun
# Create your views here.


def index(request):
    testruns = TestRun.objects.order_by('-time')[:5]
    template = loader.get_template('testruns.html')
    context = {
        'testruns': testruns,
    }

    return HttpResponse(template.render(context, request))


def testrun(request, testrun_id):
    return HttpResponse("You're looking at testrun %s." % testrun_id)


def testsuite(request, testrun_id, testsuite_id):
    response = "You're looking at the results of testrun %s and testsuite %s"
    return HttpResponse(response % (testrun_id, testsuite_id))


def testitem(request, testrun_id, testsuite_id, testitem_id):
    return HttpResponse("You're voting on question %s." % testrun_id)

