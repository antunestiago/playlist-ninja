# Generated by Django 4.2 on 2023-04-05 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('release_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('duration', models.DurationField()),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlist.album')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlist.author')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlist.author'),
        ),
    ]