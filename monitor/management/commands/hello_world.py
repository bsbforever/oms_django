#coding=utf-8
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from monitor.models import oraclelist
class Command(BaseCommand):
    def handle(self, *args, **options):
	print 'hello world'
