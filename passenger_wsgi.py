import sys, os

INTERP = os.environ['HOME'] + '/repositories/Django-ContactManager/venv/bin/python'
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

from core.wsgi import application