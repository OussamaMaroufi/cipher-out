from django.test import TestCase
import os,json
from AMIBack.backend.app.FAQ.models import FAQ

# Create your tests here.
with open(os.path.dirname(os.path.abspath(__file__))+'/ami_data2.json') as file:
    data = json.load(file)
for i in data:
    print(i['question'])
    faq=FAQ(content=i['question'])
