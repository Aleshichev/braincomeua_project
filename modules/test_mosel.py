from load_django import *
from parser_app.models import *

def main():
    obj = TestRecord.objects.create(text="test2")
    print("Wrote to DB:", obj)
    
if __name__ == "__main__":
    main()