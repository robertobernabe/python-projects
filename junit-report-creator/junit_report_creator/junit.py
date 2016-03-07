"""
junit.rnc:
#----------------------------------------------------------------------------------
start = testsuite

property = element property {
   attribute name {text},
   attribute value {text}
}

properties = element properties {
   property*
}

failure = element failure {
   attribute message {text},
   attribute type {text},
   text
}

testcase = element testcase {
   attribute classname {text},
   attribute name {text},
   attribute time {text},
   failure?
}

testsuite = element testsuite {
   attribute errors {xsd:integer},
   attribute failures {xsd:integer},
   attribute hostname {text},
   attribute name {text},
   attribute tests {xsd:integer},
   attribute time {xsd:double},
   attribute timestamp {xsd:dateTime},
   properties,
   testcase*,
   element system-out {text},
   element system-err {text}
}
#----------------------------------------------------------------------------------


and junitreport.rnc
#----------------------------------------------------------------------------------
include "junit.rnc" {
   start = testsuites
   testsuite = element testsuite {
      attribute errors {xsd:integer},
      attribute failures {xsd:integer},
      attribute hostname {text},
      attribute name {text},
      attribute tests {xsd:integer},
      attribute time {xsd:double},
      attribute timestamp {xsd:dateTime},
      attribute id {text},
      attribute package {text},
      properties,
      testcase*,
      element system-out {text},
      element system-err {text}
   }
}

testsuites = element testsuites {
   testsuite*
}
"""
import math
from datetime import timedelta
from xml.etree import ElementTree
import logging


log = logging.getLogger()


def to_timedelta(val):
    if val is None:
        return None

    secs = float(val)
    if math.isnan(secs):
        return None

    return timedelta(seconds=secs)




class TestCase(object):
    """
    testcase = element testcase {
    attribute classname {text},
    attribute name {text},
    attribute time {text},
    failure?
    }

    """

    def __init__(self, classname, name):
        self.classname = classname
        self.name = name
        self.failure = None
        self.skipped = None
        self.error = None

    def __str__(self):
        result = ""
        if self.failure:
            result = "FAILED"
        if self.skipped:
            result = "SKIPPED"
        if self.error:
            result = "ERROR"

        return "%s %s" % (self.name, result)




class TestSuite(object):
    """
    testsuite = element testsuite {
       attribute errors {xsd:integer},
       attribute failures {xsd:integer},
       attribute hostname {text},
       attribute name {text},
       attribute tests {xsd:integer},
       attribute time {xsd:double},
       attribute timestamp {xsd:dateTime},
       properties,
       testcase*,
       element system-out {text},
       element system-err {text}
    }
    """
    def __init__(self, *args, **kwargs):
        self.errors = 0
        self.failures = 0
        self.tests = 0
        self.time = 0.0
        self.timestamp = None
        self.hostname = 'localhost'
        self.name = None
        self.properties = {}
        self.stdout = None
        self.stderr = None
        self.testcase = []

    def __str__(self):
        return "Testsuite name: {0} ".format(self.name)

    def addTestcase(self, testcase):
        self.testcase.append(testcase)



class Parser(object):

    def parse(self, source):
        xml = ElementTree.parse(source)
        root = xml.getroot()
        return self.parse_root(root)

    def parse_root(self, root):
        testsuites = []
        if root.tag == 'testsuites':
            for subroot in root:
                ts = self.parse_testsuite(subroot)
                testsuites.append(ts)
        else:
            ts = self.parse_testsuite(root)
            testsuites.append(ts)

        # tr = ts.run(self.TR_CLASS())

        # tr.time = to_timedelta(root.attrib.get('time'))

        # check totals if they are in the root XML element
        # if 'errors' in root.attrib:
        #     assert len(tr.errors) == int(root.attrib['errors'])
        # if 'failures' in root.attrib:
        #     assert len(tr.failures) == int(root.attrib['failures'])
        # if 'skip' in root.attrib:
        #     assert len(tr.skipped) == int(root.attrib['skip'])
        if 'tests' in root.attrib:
            testsCount = len(list(ts.testcase))
            testsCountAttrib = int(root.attrib['tests'])
            log.debug("Attrib tests %s doesnt match count of testcases %s", testsCountAttrib, testsCount)
            # assert len(list(ts)) == int(root.attrib['tests']), "Attrib tests doesnt match amount of testcases"

        return testsuites

    def parse_testsuite(self, root):
        assert root.tag == 'testsuite'
        ts = TestSuite()
        ts.name = root.attrib.get('name')
        ts.package = root.attrib.get('package')
        ts.errors = root.attrib.get('errors')
        ts.skipped = root.attrib.get('skipped')
        ts.tests = root.attrib.get('tests')
        ts.failures = root.attrib.get('failures')
        ts.time = root.attrib.get('time')
        ts.timestamp = root.attrib.get('timestamp')

        for el in root:
            if el.tag == 'testcase':
                self.parse_testcase(el, ts)
            if el.tag == 'properties':
                self.parse_properties(el, ts)
            if el.tag == 'system-out' and el.text:
                ts.stdout = el.text.strip()
            if el.tag == 'system-err' and el.text:
                ts.stderr = el.text.strip()
        return ts

    def parse_testcase(self, el, ts):
        tc_classname = el.attrib.get('classname') or ts.name
        tc = TestCase(tc_classname, el.attrib['name'])
        tc.time = to_timedelta(el.attrib.get('time'))
        message = None
        text = None
        for e in el:
            # error takes over failure in JUnit 4
            if e.tag in ('failure', 'error', 'skipped'):
                tc = TestCase(tc_classname, el.attrib['name'])
                result = e.tag
                typename = e.attrib.get('type')

                # reuse old if empty
                message = e.attrib.get('message') or message
                text = e.text or text

                setattr(tc, result, {'message': message,
                                     'type': typename,
                                     'text': text})

                # tc.seed(result, typename, message, text)
                tc.time = to_timedelta(el.attrib.get('time'))
            if e.tag == 'system-out' and e.text:
                tc.stdout = e.text.strip()
            if e.tag == 'system-err' and e.text:
                tc.stderr = e.text.strip()

        # add either the original "success" tc or a tc created by elements
        ts.addTestcase(tc)

    def parse_properties(self, el, ts):
        for e in el:
            if e.tag == 'property':
                assert e.attrib['name'] not in ts.properties
                ts.properties[e.attrib['name']] = e.attrib['value']


def parse(source):
    return Parser().parse(source)


if __name__ == '__main__':
    testsuites = parse("junit4_jenkins.xsd.xml")
    for testsuite in testsuites:
        for tc in testsuite.testcase:
            print(tc)