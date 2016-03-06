from django.db import models

# Create your models here.


class TestStatus(models.Model):
    STATUS_CHOICES = (
        ('pass', 'Passed'),
        ('fail', 'Failed'),
        ('error', 'Had execution error(s)'),
        ('skip', 'Skipped'),
    )
    name = models.CharField(choices=STATUS_CHOICES, max_length=250)

    def __str__(self):
        return self.name


class TestItem(models.Model):
    classname = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    status = models.ForeignKey(TestStatus)
    message = models.TextField()
    output = models.TextField()

    def __str__(self):
        return self.name


class TestSuite(models.Model):
    testitems = models.ForeignKey(TestItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    hostname = models.CharField(max_length=250)
    errors = models.IntegerField()
    failures = models.IntegerField()
    skipped = models.IntegerField()
    time = models.IntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.name

class TestRun(models.Model):
    testsuites = models.ForeignKey(TestSuite, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    time = models.FloatField()

    def __str__(self):
        return self.name



