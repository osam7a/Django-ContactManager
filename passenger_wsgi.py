import sys, os

INTERP = os.environ.get('PYTHON_INTERPRETER', 0)
if INTERP == 0: sys.stderr.write("No PYTHON_INTERPRETER found\n"); sys.exit(1)
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

from core.wsgi import application