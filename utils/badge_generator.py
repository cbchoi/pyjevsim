import subprocess
import string

score = 0
with subprocess.Popen(["pylint","pyjevsim"], stdout=subprocess.PIPE) as proc:
    tokens = str(proc.stdout.read()).split(':')
    score = tokens[-1].split(',')[0][1:-3]
    
subprocess.Popen(["anybadge", f"--value={score}", "--file=utils/pylint.svg", "pylint"], stdout=subprocess.PIPE)