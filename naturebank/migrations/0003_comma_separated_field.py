import re

import django.core.validators
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("naturebank", "0002_remove_useless_manytomanyfield_options"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="tempdelete",
            managers=[
                ("gis_objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name="geocodeoption",
            name="code",
            field=models.CharField(
                max_length=10,
                primary_key=True,
                serialize=False,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^\\d+(?:\\,\\d+)*\\Z"),
                        code="invalid",
                        message="Enter only digits separated by commas.",
                    )
                ],
            ),
        ),
    ]
