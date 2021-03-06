# Generated by Django 3.0.7 on 2020-12-03 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20)),
                ('email', models.CharField(blank=True, max_length=60)),
                ('subject', models.CharField(blank=True, max_length=55)),
                ('message', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('New', 'New'), ('Read', 'Read'), ('Closed', 'Closed')], default='New', max_length=6)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('note', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='settings',
            name='smtpemail',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='settings',
            name='smtpserver',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
