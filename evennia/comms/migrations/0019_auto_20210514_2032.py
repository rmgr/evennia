# Generated by Django 2.2.16 on 2021-05-14 20:32

from django.db import migrations


def migrate_channel_aliases(apps, schema_editor):
    """
    Note - this migration uses the contemporary ChannelDB rather than
    the apps.get_model version. This allows for using all the
    helper functionality, but introduces a dependency on current code. So
    We catch errors and warn, since this is not something that will be needed
    after doing the first migration.

    """
    from evennia.comms.models import ChannelDB
    # ChannelDB = apps.get_model("comms", "ChannelDB")

    for channel in ChannelDB.objects.all():
        try:
            chan_key = channel.db_key.lower()
            channel_aliases = [chan_key] + [alias.lower() for alias in channel.aliases.all()]
            for subscriber in channel.subscriptions.all():
                nicktuples = subscriber.nicks.get(category="channel", return_tuple=True, return_list=True)
                all_aliases = channel_aliases + [tup[2] for tup in nicktuples if tup[3].lower() == chan_key]
                for key_or_alias in all_aliases:
                    channel.add_user_channel_alias(subscriber, key_or_alias)
        except Exception as err:
            # we want to continue gracefully here since this is a data-migration from
            # an old to a new version and doesn't involve schema changes
            print("channel-alias data migration 0019_auto_20210514_2032 skipped: {err}")


class Migration(migrations.Migration):

    dependencies = [
        ('comms', '0018_auto_20191025_0831'),
    ]

    operations = [
        migrations.RunPython(migrate_channel_aliases)
    ]
