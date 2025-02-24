from django.core.management.base import BaseCommand
from django.apps import apps
import pandas as pd
## just make sure that you write the name correctly hhahahahaha its management 
class Command(BaseCommand):
    help = "Import Data CSV into Django Models"
    usage = """
    python manage.py import_courses --path data.csv
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            help="file path",
            default="udemy_courses.csv",
        )

    def handle(self, *args, **options):
        file_path = options["path"]
        model = apps.get_model("app", "Course")
        df = pd.read_csv(file_path)
        df_records = df.to_dict("records")
        model_instances = [
            model(
                course_id=record["course_id"],
                course_title=record["course_title"],
                url=record["url"],
                is_paid=record["is_paid"],
                price=record["price"],
                num_subscribers=record["num_subscribers"],
                num_lectures=record["num_lectures"],
                num_reviews=record["num_reviews"],
                level=record["level"],
                content_duration=record["content_duration"],
                subject=record["subject"],
                published_timestamp=record["published_timestamp"],
            )
            for record in df_records
        ]

        model.objects.bulk_create(model_instances)  # Bulk insert data
        self.stdout.write(self.style.SUCCESS("Finished Importing Data"))