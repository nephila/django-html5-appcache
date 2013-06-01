# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from html5_appcache.cache import clear_cache_manifest


class Command(BaseCommand):
    help = 'Clear appcache manifest cache.'

    def handle(self, *args, **options):
        clear_cache_manifest()