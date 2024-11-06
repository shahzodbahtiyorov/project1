import os
from django.core.files import File
from django.core.management.base import BaseCommand
from apps.wallet.models.paynet import Providers


class Command(BaseCommand):
    help = 'Import images for Providers based on provider_id'

    def handle(self, *args, **kwargs):
        images_dir = os.path.join(os.path.dirname(__file__), 'providers_images')

        for filename in os.listdir(images_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.svg')):
                provider_id_str = filename.split('.')[0]
                try:
                    provider_id = int(provider_id_str)

                    provider = Providers.objects.get(provider_id=provider_id)
                    image_path = os.path.join(images_dir, filename)

                    with open(image_path, 'rb') as image_file:
                        provider.image.save(filename, File(image_file), save=True)
                        self.stdout.write(self.style.SUCCESS(
                            f'Image {filename} added to provider {provider_id}.'))

                except Providers.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'Provider with id {provider_id} does not exist.'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing file {filename}: {e}'))
