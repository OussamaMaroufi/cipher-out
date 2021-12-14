
from django.core.management.base import BaseCommand, CommandError
import json,os
from AMIBack.backend.app.FAQ.models import FAQ

class Command(BaseCommand):
    help = 'load all the data'

    def handle(self, *args, **options):
        self.stdout.write('Started lading FAQ')
        self.stdout.write(
            "Started adding data. This may take few minutes, please don't interupt the commmand")
        with open(os.path.dirname(os.path.abspath(__file__))+'/ami_data2.json') as file:
            data = json.load(file)
            for i in data:
                print(i['question'])
                faq = FAQ(content=i['question'])
                faq.save()
        self.stdout.write('Successfully loaded all the data')
