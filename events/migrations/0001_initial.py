# Generated by Django 2.0.13 on 2020-02-24 04:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SacramentMeeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateField()),
                ('topic', models.CharField(blank=True, max_length=150, null=True)),
                ('time_range', models.CharField(blank=True, max_length=10, null=True)),
                ('reference_materials', models.TextField(blank=True, null=True, verbose_name='Reference Materials')),
                ('bishopric', models.TextField(default='Kelly Ericson\nJames McDonald\nWilliam Clayton', verbose_name='Bishopric')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Speaker Order')),
                ('speaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Member')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
