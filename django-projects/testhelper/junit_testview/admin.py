from django.contrib import admin

from .models import TestRun, TestSuite, TestItem, TestStatus

admin.site.register(TestRun)
admin.site.register(TestSuite)
admin.site.register(TestItem)
admin.site.register(TestStatus)
# Register your models here.
