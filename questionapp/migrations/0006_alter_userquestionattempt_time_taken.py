# Generated by Django 4.2.8 on 2024-01-03 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionapp', '0005_alter_testattempt_score_alter_testattempt_timetaken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquestionattempt',
            name='time_taken',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
