# Generated by Django 4.1.3 on 2023-02-13 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_data_upload_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='subscribers',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
