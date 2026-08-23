from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(
            settings.AUTH_USER_MODEL
        ),
        (
            "engagement",
            "0001_initial"
        ),
    ]

    operations = [

        # Remove the old Follow constraint
        migrations.RemoveConstraint(
            model_name="follow",
            name="engagement_unique_follow",
        ),

        # Update follower relationship
        migrations.AlterField(
            model_name="follow",
            name="follower",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="engagement_following",
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # Update following relationship
        migrations.AlterField(
            model_name="follow",
            name="following",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="engagement_followers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # Add the new unique constraint
        migrations.AddConstraint(
            model_name="follow",
            constraint=models.UniqueConstraint(
                fields=("follower", "following"),
                name="unique_engagement_follow",
            ),
        ),

        # Delete old engagement models
        migrations.DeleteModel(
            name="Comment",
        ),

        migrations.DeleteModel(
            name="MusicLike",
        ),
    ]