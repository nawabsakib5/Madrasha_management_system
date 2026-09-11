from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('full_name', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('role', models.CharField(
                    choices=[
                        ('super_admin', 'Super Admin'),
                        ('admin', 'Admin'),
                        ('accountant', 'Accountant'),
                        ('teacher', 'Teacher'),
                        ('student', 'Student'),
                        ('parent', 'Parent'),
                    ],
                    default='student',
                    max_length=20,
                )),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profiles/')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('must_change_password', models.BooleanField(default=True)),
                ('two_factor_enabled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(
                    blank=True,
                    related_name='custom_user_set',
                    to='auth.group',
                )),
                ('user_permissions', models.ManyToManyField(
                    blank=True,
                    related_name='custom_user_permissions_set',
                    to='auth.permission',
                )),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]