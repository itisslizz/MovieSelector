# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieselector', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movieinselection',
            old_name='added_by',
            new_name='owner',
        ),
    ]
