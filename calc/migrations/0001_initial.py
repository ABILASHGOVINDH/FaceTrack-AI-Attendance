# Generated by Django 5.0.3 on 2024-04-26 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Enter_Your_Id', models.IntegerField(default=100)),
                ('Name', models.CharField(default='', max_length=100)),
                ('Password', models.CharField(default='', max_length=123)),
            ],
        ),
    ]

