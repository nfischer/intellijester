import os.path,subprocess
from subprocess import STDOUT,PIPE

def execute_java():
    #java_class,ext = os.path.splitext('target/intelligester-1.0.jar')
    cmd = ['java', '-jar', 'target/intelligester-1.0.jar']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out = proc.stdout.read()
    print (out)

execute_java()