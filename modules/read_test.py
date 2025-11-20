from load_django import *
from parser_app.models import *

def main():
    records = TestRecord.objects.all()
    print("Found records:", records.count())
    for record in records:
        print(record)
        
if __name__ == "__main__":
    main()