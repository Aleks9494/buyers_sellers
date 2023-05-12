from django.core.management.base import BaseCommand
import json
from test_shop.models import Deal


class Command(BaseCommand):

    def handle(self, *args, **options):
        deals = Deal.objects.select_related().all()
        result = {
            i.lot.seller.user.username:
                {
                    "buyers": list({j.buyer.user.username for j in deals if i.lot.seller == j.lot.seller}),
                    "all_sum": sum(k.lot.price * k.amount for k in deals if i.lot.seller == k.lot.seller)
                }
            for i in deals
        }
        return json.dumps(result)
