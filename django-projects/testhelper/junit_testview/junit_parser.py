import xunitparser


ts, tr = xunitparser.parse(open("report.xml"))

for tc in ts:
    print(tc.classname, tc.methodname )

