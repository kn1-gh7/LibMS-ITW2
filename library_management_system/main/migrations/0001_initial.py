# Generated by Django 4.2.7 on 2023-11-05 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('ISBN', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(blank=True, max_length=50, null=True)),
                ('year_published', models.IntegerField(blank=True, null=True)),
                ('description_text', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('label', models.IntegerField(primary_key=True, serialize=False)),
                ('categories', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionTypes',
            fields=[
                ('t_type', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('t_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryDB',
            fields=[
                ('book_isbn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.books')),
                ('total_count', models.IntegerField(default=0)),
                ('issued_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_time', models.DateTimeField()),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.books')),
                ('the_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
                ('trans_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.transactiontypes')),
            ],
        ),
        migrations.CreateModel(
            name='BooksAndUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.books')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
            ],
        ),
        migrations.CreateModel(
            name='BookGenres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_ISBN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.books')),
                ('genres', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.genres')),
            ],
        ),
        migrations.AddConstraint(
            model_name='librarydb',
            constraint=models.CheckConstraint(check=models.Q(('total_count__gt', models.F('issued_count')), ('issued_count__gte', 0)), name='not_more_books_issued', violation_error_message='ERROR: Either trying to return a book which was not issued, or trying to issue more books that available!'),
        ),
    ]
