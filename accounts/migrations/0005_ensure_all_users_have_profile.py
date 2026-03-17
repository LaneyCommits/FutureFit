from django.db import migrations


def create_missing_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('accounts', 'Profile')
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user, defaults={'email_verified': True})


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_major_key_profile_min_salary_and_more'),
    ]

    operations = [
        migrations.RunPython(create_missing_profiles, migrations.RunPython.noop),
    ]
