import os
from django.core.files import File
from django.core.management.base import BaseCommand

from apps.wallet.models.paynet import Category,Providers


class Command(BaseCommand):
    help = 'Import images from the images directory and attach them to categories based on category_id'

    def handle(self, *args, **kwargs):
        images_dir = os.path.join(os.path.dirname(__file__), 'images')

        for filename in os.listdir(images_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.svg')):
                category_id_str = filename.split('.')[0]
                try:
                    category_id = int(category_id_str)

                    category = Category.objects.get(category_id=category_id)
                    image_path = os.path.join(images_dir, filename)

                    with open(image_path, 'rb') as image_file:
                        category.image.save(filename, File(image_file), save=True)
                        self.stdout.write(self.style.SUCCESS(
                            f'Image {filename} added to category {category_id}.'))

                except Category.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'Category with id {category_id} does not exist.'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing file {filename}: {e}'))
