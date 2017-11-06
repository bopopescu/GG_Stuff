import subprocess
get_jobs = subprocess.Popen(['C:/Program Files/Thinkbox/Deadline7/bin/deadlinecommand.exe'], stdout=subprocess.PIPE,
        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
jobs = get_jobs.communicate()
for each in jobs:
	print each