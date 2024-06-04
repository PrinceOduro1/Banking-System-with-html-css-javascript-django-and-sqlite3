# Generated by Django 5.0 on 2024-05-26 22:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('bank_user', models.ForeignKey(db_column='username', on_delete=django.db.models.deletion.CASCADE, to='bank.bankuser')),
            ],
        ),
    ]
