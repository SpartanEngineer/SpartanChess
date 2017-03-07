import os, sys

rootDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, rootDir + '/src')
exec(open(rootDir + '/src/SpartanChess.py').read())
