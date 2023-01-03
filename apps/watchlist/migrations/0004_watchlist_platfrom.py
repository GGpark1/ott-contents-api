# Generated by Django 3.2.16 on 2023-01-01 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0003_auto_20221229_0549'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='platfrom',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='watchlist.streamplatform'),
            preserve_default=False,
        ),
    ]
