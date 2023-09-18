from store.signals import order_created
from django.dispatch import receiver


@receiver(order_created)
def on_order_created(sender, **kwargs):
    print("Order created")
    print(kwargs['order'])
    print(sender)
    print(kwargs)
