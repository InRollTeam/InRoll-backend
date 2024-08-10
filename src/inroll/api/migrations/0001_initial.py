# Generated by Django 5.0.7 on 2024-08-08 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.PositiveBigIntegerField(unique=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OpenEndedQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.PositiveBigIntegerField(unique=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('company_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('is_true', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='api.multiplechoicequestion')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='made_submissions', to='api.candidate')),
            ],
        ),
        migrations.CreateModel(
            name='OpenEndedAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.openendedquestion')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='open_ended_answers', to='api.submission')),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.multiplechoicequestion')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choice_answers', to='api.submission')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DurationField()),
                ('until_date', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tests', to='api.recruiter')),
            ],
        ),
        migrations.AddField(
            model_name='submission',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.test'),
        ),
        migrations.AddField(
            model_name='openendedquestion',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='open_ended_questions', to='api.test'),
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multiple_choice_questions', to='api.test'),
        ),
        migrations.CreateModel(
            name='UserTestMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DurationField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tests', to='api.candidate')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='api.test')),
            ],
        ),
    ]
