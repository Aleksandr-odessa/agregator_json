# Generated by Django 5.1.1 on 2024-09-13 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('timestamp', models.DateTimeField()),
                ('http_method', models.CharField(max_length=10)),
                ('uri', models.CharField(max_length=300)),
                ('response_code', models.IntegerField()),
                ('response_size', models.IntegerField()),
            ],
        ),
    ]
