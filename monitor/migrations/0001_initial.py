# Generated by Django 4.2 on 2023-05-01 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContractRequestLogger',
            fields=[
                ('created', models.DateTimeField(auto_created=True, editable=False)),
                ('target', models.CharField(editable=False, max_length=265)),
                ('origin', models.CharField(editable=False, max_length=265)),
                ('request_id', models.CharField(max_length=80, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddIndex(
            model_name='contractrequestlogger',
            index=models.Index(fields=['target', 'origin'], name='monitor_con_target_5eaeca_idx'),
        ),
    ]
