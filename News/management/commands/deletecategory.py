from unicodedata import category

from django.core.management.base import BaseCommand, CommandError
from News.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет ВСЕ посты выбранной категории'

    def add_arguments(self, parser):
        parser.add_argument('category_name', type=str, help='Имя категории')

    def handle(self, *args, **options):
        confirmation = input(f'Вы действительно хотите удалить все публикации'
                             f'категории "{options['category_name']}"? y/n ')

        if confirmation != 'y':
            self.stdout.write(self.style.ERROR('Удаление отменено'))
            return

        try:
            category = Category.objects.get(category_name=options['category_name'])
            Post.objects.filter(category=category).delete()

            self.stdout.write(self.style.SUCCESS(f'Публикации из категории {category.category_name}'
               
                                                 f'успешно удалены'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категории "{options['category_name']}" не существует'))


