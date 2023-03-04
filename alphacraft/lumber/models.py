from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Supplier(TimeStampedModel):
    """
    Log/Lumber suppliers
    """

    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    contact_number = models.CharField(max_length=100, blank=True)
    email = models.EmailField(null=True)

    def __str__(self) -> str:
        return self.name


class PurchaseOrder(TimeStampedModel):
    """
    Transaction with a supplier
    """

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    date = models.DateField()

    paid = models.BooleanField(default=False)
    date_paid = models.DateField(null=True)
    mode_of_payment = models.CharField(max_length=50, blank=True)
    payment_details = models.TextField(blank=True)

    delivered = models.BooleanField(default=False)
    date_delivered = models.DateField(null=True)


class PurchaseItem(TimeStampedModel):
    """
    The item that has been purchased
    """

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items",
    )
    price = models.FloatField()
    item_type = models.CharField(max_length=10)  # log/lumber

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="purchase_items",
    )
    object_id = models.PositiveBigIntegerField()
    item = GenericForeignKey("content_type", "object_id")


class LumberClient(TimeStampedModel):
    """
    Log/Lumber buyers
    """

    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    contact_number = models.CharField(max_length=100, blank=True)
    email = models.EmailField(null=True)

    def __str__(self) -> str:
        return self.name


class Order(TimeStampedModel):
    """
    Client order transaction data
    """

    client = models.ForeignKey(
        LumberClient,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
    )
    date = models.DateField()

    paid = models.BooleanField(default=False)
    date_paid = models.DateField(null=True)
    mode_of_payment = models.CharField(max_length=50, blank=True)
    payment_details = models.TextField(blank=True)

    delivered = models.BooleanField(default=False)
    date_delivered = models.DateField(null=True)


class OrderItem(TimeStampedModel):
    """
    The item that has been sold to the lumber client
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    price = models.FloatField()
    item_type = models.CharField(max_length=10)  # log/lumber

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    object_id = models.PositiveBigIntegerField()
    item = GenericForeignKey("content_type", "object_id")


class Log(TimeStampedModel):
    id = models.PositiveBigIntegerField(primary_key=True)
    thickness = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()
    length = models.PositiveSmallIntegerField()
    source = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

    purchase = GenericRelation(PurchaseItem)
    sale = GenericRelation(OrderItem)  # sold as log

    @property
    def volume(self):
        return (self.thickness * self.width * self.width) / 12

    def __str__(self) -> str:
        return f"<Log {self.id}: {self.thickness} x {self.width} x {self.length} : {int(self.volume)} bdft>"


class Lumber(TimeStampedModel):
    id = models.PositiveBigIntegerField(primary_key=True)
    thickness = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()
    length = models.PositiveSmallIntegerField()
    log = models.ForeignKey(Log, on_delete=models.SET_NULL, null=True)

    # bought directly from source
    purchase = GenericRelation(PurchaseItem)
    sale = GenericRelation(OrderItem)

    @property
    def volume(self):
        return (self.thickness * self.width * self.width) / 12

    def __str__(self) -> str:
        return f"<Lumber: {self.thickness} x {self.width} x {self.length} : {int(self.volume)} bdft>"
