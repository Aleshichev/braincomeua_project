"""
A file for loading the Django environment in third-party scripts.
Allows you to use Django models outside the project folder.
"""

import os
import sys
import django

# Get the root directory (parent of modules/)
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the braincomua_project directory to Python path
project_path = os.path.join(root_path, 'braincomua_project')
sys.path.insert(0, project_path)

# Name of Django settings module and project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "braincomua_project.settings")

# Initialize Django
django.setup()
