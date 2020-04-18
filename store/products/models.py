from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=False, blank=False, unique=True)
    image = models.ImageField(upload_to='products/', null=False, blank=False)

    def __str__(self):
        return self.title


def set_slug(sender, instance, *args, **kwargs):
    if not instance.slug and instance.title:
        slug = slugify(instance.title)

        while Product.objects.filter(slug=slug).exists():
            slug = slugify('{}-{}'.format(
                instance.title, str(uuid.uuid4())[:5]))
        instance.slug = slug


pre_save.connect(set_slug, sender=Product)
