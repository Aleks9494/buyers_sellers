from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if Seller.objects.filter(user=self.user).exists():
            raise ValidationError('Пользователь является продавцом')
        return super().save()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Feedback(models.Model):
    title = models.CharField(max_length=50, blank=True, verbose_name='Тема')
    text = models.TextField(verbose_name='Текст отзыва')
    content_type = models.ForeignKey(
        ContentType, limit_choices_to={
            'model__in': (
                'seller',
                'lots',
            )
        }, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='feedbacks', verbose_name='Автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    feedback = GenericRelation(Feedback)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class Lots(models.Model):
    CHOICES = (
        (
            'Красный', (
                ('light-red', 'светло-красный'),
                ('dark-red', 'темно-красный'),
            )
        ),
        (
            'Оранжевый', (
                ('light-orange', 'светло-оранжевый'),
                ('dark-orange', 'темно-оранжевый'),
            )
        ),
    )
    flower = models.CharField(max_length=50, verbose_name='Вид цветка')
    colour = models.CharField(max_length=30, choices=CHOICES, blank=True, verbose_name='Оттенок')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    amount = models.PositiveIntegerField(default=0, verbose_name='Количество')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='lots', verbose_name='Продавец')
    is_display = models.BooleanField(default=True, verbose_name='Отображение')
    feedback = GenericRelation(Feedback)

    def __str__(self):
        return self.flower

    class Meta:
        verbose_name = 'Лот'
        verbose_name_plural = 'Лоты'


class Deal(models.Model):
    lot = models.ForeignKey(Lots, on_delete=models.CASCADE, related_name='deals', verbose_name='Лот')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='deals', verbose_name='Покупатель')
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
