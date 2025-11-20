"""
A file for loading the Django environment in third-party scripts.
Allows you to use Django models outside the project folder.
"""

import os
import sys
import django

# Path to Django project
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# Name of Django settings module and  project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "braincomua_project.settings")

# Initialize Django
django.setup()
