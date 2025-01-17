# Generated by Django 4.2.8 on 2023-12-27 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testattempt',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_attempts', to='questionapp.test'),
        ),
        migrations.AlterField(
            model_name='userquestionattempt',
            name='test_attempt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions_attempt', to='questionapp.testattempt'),
        ),
    ]
