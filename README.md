# Simple utility to conduct failover tests
How this works:

When the tester is armed, it starts checking if network adresses are reacheable.

When all IPs are unreachable, test starts recording the time

When IPs become reachable again, test records time to a file

