from django.db import models
from users.models import User
from products.models import Product
from django.db.models.signals import pre_save, m2m_changed, post_save
import uuid


class CartShop(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, 
                               unique=True)
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProducts')
    subtotal = models.DecimalField(default=0.0, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=9, decimal_places=2)
    crated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart User {} {}".format(self.user, self.cart_id)

    def products_related(self):
        return self.cartproducts_set.select_related('product')

    def update_totals(self):
        self.update_subtotal()
        self.update_total() 
        if self.order:
            self.order.update_total()

    def update_subtotal(self):
        self.subtotal = sum([cp.product.price * cp.quantity for cp in self.products_related()])
        self.save()

    def update_total(self):
        self.total = self.subtotal
        self.save()

    @property
    def order(self):
        return self.order_set.first()


class CartProductsManager(models.Manager):
    def set_quantity(self, cartshop, product, quantity=1):
        cp, created = self.get_or_create(cart=cartshop, product=product)

        if not created:
            quantity = cp.quantity + quantity
        cp.update_quantity(quantity)
        return cp


class CartProducts(models.Model):
    cart = models.ForeignKey(CartShop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    objects = CartProductsManager()

    def update_quantity(self, quantity=1):
        self.quantity = quantity
        self.save()


def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())


def update_totals(sender, instance, action, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.update_totals()


def post_save_update_totals(sender, instance, *args, **kwargs):
    instance.cart.update_totals()


pre_save.connect(set_cart_id, sender=CartShop)
post_save.connect(post_save_update_totals, sender=CartProducts)
m2m_changed.connect(update_totals, sender=CartShop.products.through)
