import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from SerializersApp.models import Books


class Command(BaseCommand):
    help = "initialize the default data for application"

    def create_group(self, **kwargs):
        objs = ("Admin", "Super Admin","User",)
        for obj in objs:
            Group.objects.get_or_create(name=obj)

        print("Group Created")
    def create_books(self, **kwargs):
        objs = {
            "name": ["Midnight's Children", "The God of Small Things", "A Suitable Boy", "The White Tiger", "The Guide"],
            "author_name": ["Salman Rushdie", "Arundhati Roy", "Vikram Seth", "Aravind Adiga", "R.K. Narayan"]
        }
        for name, author_name in zip(objs["name"], objs["author_name"]):
            book, created = Books.objects.get_or_create(name=name, author_name=author_name)


    def handle(self, *args, **options):
        self.create_group()
        self.create_books()