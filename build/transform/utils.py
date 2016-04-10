import subprocess
import os

def execute(cmdline, env=os.environ):
	p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, env=env)
	s = []
	for line in iter(p.stdout.readline, b''):
		line = line.strip()
		print line
		s.append(line)
	p.wait()
	return p.returncode, s
