# Generated by Django 4.1.4 on 2023-02-01 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0002_alter_goal_description_alter_goal_due_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удалена')),
            ],
            options={
                'verbose_name': 'Доска',
                'verbose_name_plural': 'Доски',
            },
        ),
        migrations.AddField(
            model_name='goalcategory',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='goals.board', verbose_name='Доска'),
        ),
        migrations.CreateModel(
            name='BoardParticipant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Owner'), (2, 'Writer'), (3, 'Reader')], default=1, verbose_name='Роль')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participants', to='goals.board', verbose_name='Доска')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participants', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Участник',
                'verbose_name_plural': 'Участники',
                'unique_together': {('board', 'user')},
            },
        ),
    ]
