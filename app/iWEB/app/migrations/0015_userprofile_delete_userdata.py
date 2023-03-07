# Generated by Django 4.1.5 on 2023-03-07 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0014_remove_userdata_id_alter_userdata_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streak', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('current_template', models.CharField(default='default', max_length=50)),
                ('owned_templates', models.CharField(default='default', max_length=150)),
                ('challenge_done', models.BooleanField(default=False)),
                ('current_challenge', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.challenge')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserData',
        ),
    ]
