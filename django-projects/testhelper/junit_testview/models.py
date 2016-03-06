from django.db import models

# Create your models here.


class TestRun(models.Model):
    testsuites = models.ForeignKey(TestSuite, on_delete=models.CASCADE)
    name = models.CharField()
    time = models.FloatField()


class TestSuite(models.Model):
    testrun = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    testitems = models.ForeignKey(TestItem, on_delete=models.CASCADE)
    name = models.CharField()
    hostname = models.CharField()
    errors = models.IntegerField()
    failures = models.IntegerField()
    skipped = models.IntegerField()
    time = models.IntegerField()
    timestamp = models.DateTimeField()


class TestItem(models.Model):
    testsuite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)
    classname = models.CharField()
    name = models.CharField()
    status = models.ForeignKey(TestStatus)
    message = models.CharField()
    output = models.CharField()


class TestStatus(models.Model):
    STATUS_CHOICES = (
        ('pass', 'Passed'),
        ('fail', 'Failed'),
        ('error', 'Had execution error(s)'),
        ('skip', 'Skipped'),
    )
    name = models.CharField(choices=STATUS_CHOICES)

