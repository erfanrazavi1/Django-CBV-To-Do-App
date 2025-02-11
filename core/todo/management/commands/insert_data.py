from django.core.management.base import BaseCommand
from faker import Faker
from todo.models import Task
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = "Inserting dummy data" 
    fake = Faker()
    def handle(self, *args, **options):
        

        user, created = User.objects.get_or_create(username=self.fake.user_name())
        if created:
            user.set_password('pass/@1234567')  # set hashed password
            user.first_name = self.fake.first_name()
            user.last_name = self.fake.last_name()
            user.email = self.fake.email()
            user.save()

        # generate a list of 5 task objects (but not yet saved in the database)
        tasks = [
            Task(user=user, title=self.fake.word().title(), complete=random.choice((True, False)))
            for _ in range(5)
        ] 

        # insert all tasks into the database with a single query (optimized)
        Task.objects.bulk_create(tasks)

        # print success message in green color
        self.stdout.write(self.style.SUCCESS('Dummy data inserted successfully!'))
