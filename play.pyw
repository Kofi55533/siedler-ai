import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("SIEDLER_PLAY_UI", "1")

from play_game import main

main()
