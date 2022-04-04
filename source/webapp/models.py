from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Quote(models.Model):
    text = models.TextField(max_length=2000, null=False, blank=False, verbose_name='Текст цитаты')
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Имя автора')
    email = models.EmailField()
    rate = models.PositiveIntegerField(default=0, null=False, blank=False, verbose_name='Рейтинг')
    is_status = models.BooleanField(default=False, null=False, blank=False, verbose_name='Модерированная цитата')
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='Дата создания')

    class Meta:
        db_table = 'Quotes'
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"

    def __str__(self) -> str:
        return f"{self.text}"