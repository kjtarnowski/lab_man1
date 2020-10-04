# Generated by Django 2.2 on 2020-10-04 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('lab_name', models.CharField(max_length=50, unique=True)),
                ('lab_email', models.EmailField(max_length=254)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Aparat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aparat_name', models.CharField(max_length=25)),
                ('slug', models.SlugField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Compound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compound_name', models.CharField(max_length=25)),
                ('compound_mass', models.FloatField()),
                ('slug', models.SlugField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_name', models.CharField(max_length=25)),
                ('slug', models.SlugField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=25)),
                ('slug', models.SlugField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(default='-')),
                ('appointed', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('progress', models.CharField(choices=[('TBD', 'ONGOING'), ('UC', 'DONE')], default='TBD', max_length=10)),
                ('result1', models.FloatField(default=0.0)),
                ('result2', models.FloatField(default=0.0)),
                ('result3', models.FloatField(default=0.0)),
                ('final', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=250)),
                ('aparat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiments_on_this_aparat', to=settings.AUTH_USER_MODEL)),
                ('compound', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiments_for_compounds', to='experiments.Compound')),
                ('experiment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiments_of_this_type', to='experiments.ExperimentType')),
                ('lab_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiments_of_person', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='compound',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compounds', to='experiments.Project'),
        ),
    ]
