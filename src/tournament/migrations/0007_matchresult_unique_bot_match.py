# Generated by Django 4.2.2 on 2023-07-08 15:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tournament", "0006_alter_user_is_npc"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="matchresult",
            constraint=models.UniqueConstraint(
                fields=("bot", "match"), name="unique_bot_match"
            ),
        ),
    ]
