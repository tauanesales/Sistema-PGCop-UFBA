import os
import sys

current_dir = os.path.join(os.getcwd())
sys.path.append(current_dir)

from src.api.app import get_app
app = get_app()