from load_django import *
from braincomua_project.parser_app.models import TestRecord

def main():
    obj = TestRecord.objects.create(text="test")
    print("Wrote to DB:", obj)
    
if __name__ == "__main__":
    main()