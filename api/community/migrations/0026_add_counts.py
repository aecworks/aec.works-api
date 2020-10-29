# Generated by Django 2.2.13 on 2020-10-29 02:05

from django.db import migrations, models


def up(apps, schema_editor):
    orphan_tree_ids = set()
    # Backfill Thread Id
    Comment = apps.get_model("community", "Comment")
    for comment in Comment.objects.all():
        if comment.thread_id:
            # Is already root or somehow already has thread id
            continue

        root = Comment.objects.filter(tree_id=comment.tree_id).order_by("level").first()

        # Root does not have thread id, delete entire comment tree since it's malformed
        if not root.thread_id:
            orphan_tree_ids.add(comment.tree_id)
            continue

        comment.thread_id = root.thread_id
        comment.save()

    if orphan_tree_ids:
        print(f"comment trees are orphan, deleting: {orphan_tree_ids}")
        Comment.objects.filter(tree_id__in=orphan_tree_ids).delete()


def down(apps, schema_editor):
    # Only Root had thread id
    Comment = apps.get_model("community", "Comment")
    for comment in Comment.objects.all():
        if comment.level != 0:
            comment.thread_id = None
            comment.save()


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0025_remove_image_url_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="clap_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="company",
            name="clap_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="company",
            name="thread_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="post",
            name="clap_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="post",
            name="thread_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(up, down),
    ]
