[main]

name = test 0ne
description = test w/ error at the setup
# stop current section on error
# note: if an error occour while executing setup, 
# we will not run the 'test' section
stop_on_error = True

[setup]
# write multiple lines with tabs
cmd = echo "foo"
	echo "bar"
	exit 1
	cat unknown_file
	echo "foobar"


[teardown]

cmd = echo "teardown test 1"

[test]


