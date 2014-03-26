[main]

name = test three
description = empty test w/o errors but skipped

stop_on_error = True
# skip test with description
skip = ISSUE 42

[setup]

cmd = echo 'test 3'

[teardown]

cmd = echo "ende3"

# ignore output
output = None

[test]

cmd = 
