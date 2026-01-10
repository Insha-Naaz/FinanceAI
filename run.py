import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ""))

import streamlit.web.bootstrap as bootstrap

bootstrap.run("app/main.py", "", [], [])
