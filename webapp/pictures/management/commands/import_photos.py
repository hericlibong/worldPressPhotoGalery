import os
import json
from django.core.management.base import BaseCommand, CommandError
from pictures.models import PhotoGallery


class Command(BaseCommand):
    """
    Importe les items photo depuis tous les fichiers .json présents dans un répertoire,
    en mettant à jour ou créant dans PhotoGallery selon (caption, picture).
    """

    help = "Import photos from all .json files in the specified directory (batch mode only)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            required=True,
            help="Path to the directory containing .json files exported by Scrapy."
        )

    def handle(self, *args, **options):
        dir_path = options["dir"]
        if not os.path.isdir(dir_path):
            raise CommandError(f"Not a directory: {dir_path}")

        # Lister les fichiers .json dans le dossier
        files = sorted(f for f in os.listdir(dir_path) if f.lower().endswith(".json"))
        if not files:
            self.stderr.write(self.style.WARNING(f"No .json files found in {dir_path}"))
            return

        # Parcourir chaque .json et importer les items
        total_created = 0
        total_updated = 0
        for filename in files:
            full_path = os.path.join(dir_path, filename)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    items = json.load(f)
            except json.JSONDecodeError as e:
                self.stderr.write(self.style.ERROR(
                    f"JSON parse error in {filename}: {e}"
                ))
                continue

            created, updated = self.process_items(items)
            total_created += created
            total_updated += updated

            self.stdout.write(
                self.style.SUCCESS(
                    f"[{filename}] Imported: {created} created, {updated} updated."
                )
            )

        # Bilan global
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Total: {total_created} created, {total_updated} updated across all files."
            )
        )

    def process_items(self, items):
        """
        Traite une liste d'items (déjà parsés depuis un fichier JSON)
        et les insère ou met à jour dans PhotoGallery, respectant
        unique_together = (caption, picture).
        Retourne (nb_created, nb_updated).
        """
        count_created = 0
        count_updated = 0

        for item in items:
            caption = item.get("caption")
            picture = item.get("picture")

            # Vérifier la présence des champs requis
            if not caption or not picture:
                self.stderr.write(
                    self.style.WARNING(
                        f"Skipping item with missing caption/picture: {item}"
                    )
                )
                continue

            # update_or_create sur (caption, picture)
            obj, created = PhotoGallery.objects.update_or_create(
                caption=caption,
                picture=picture,
                defaults={
                    "media": item.get("media", ""),
                    "sectionTitle": item.get("sectionTitle", ""),
                    "pubDate": item.get("pubDate", None),
                    "pageUrl": item.get("pageUrl", ""),
                    "location": item.get("location", ""),
                    "author": item.get("author", ""),
                    "credits": item.get("credits", ""),
                    "pictureEditor": item.get("pictureEditor", ""),
                }
            )
            if created:
                count_created += 1
            else:
                count_updated += 1

        return count_created, count_updated
