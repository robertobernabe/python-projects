from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the junit-testview index.")


def testrun(request, testrun_id):
    return HttpResponse("You're looking at testrun %s." % testrun_id)


def testsuite(request, testrun_id, testsuite_id):
    response = "You're looking at the results of testrun %s and testsuite %s"
    return HttpResponse(response % (testrun_id, testsuite_id))


def testitem(request, testrun_id, testsuite_id, testitem_id):
    return HttpResponse("You're voting on question %s." % testrun_id)

