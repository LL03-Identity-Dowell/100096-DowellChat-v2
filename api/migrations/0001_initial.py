# Generated by Django 4.1 on 2023-11-10 07:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50, null=True)),
                ('room_id', models.CharField(max_length=50, null=True)),
                ('message_data', models.TextField(null=True)),
                ('side', models.CharField(max_length=50, null=True)),
                ('author', models.CharField(max_length=250, null=True)),
                ('message_type', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=250, null=True)),
                ('org_id', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
