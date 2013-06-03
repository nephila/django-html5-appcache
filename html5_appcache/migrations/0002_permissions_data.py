# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        from html5_appcache.models import GlobalPermission
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        GlobalPermission.objects.create(name="Can view cache status", codename="can_view_cache_status")
        GlobalPermission.objects.create(name="Can update manifest", codename="can_update_manifest")


    def backwards(self, orm):
        "Write your backwards methods here."
        from html5_appcache.models import GlobalPermission
        GlobalPermission.objects.filter(codename="can_view_cache_status").delete()
        GlobalPermission.objects.filter(codename="can_update_manifest").delete()


    models = {
        
    }

    complete_apps = ['html5_appcache']
    symmetrical = True
