from django.contrib import admin
from .models import Seller, Buyer, Lots, Feedback, Deal


class LotsInlineAdmin(admin.TabularInline):
    model = Lots
    list_display = ('pk', 'flower', "price", "amount", "is_display")


class SellerAdmin(admin.ModelAdmin):
    list_display = ("pk", "user",)
    inlines = [LotsInlineAdmin]


class BuyerAdmin(admin.ModelAdmin):
    list_display = ("pk", "user",)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content_object', "author", "title")


class DealAdmin(admin.ModelAdmin):
    list_display = ("pk", "lot", "buyer", "seller_name")

    @staticmethod
    def seller_name(obj):
        return obj.lot.seller.user.username


admin.site.register(Seller, SellerAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Deal, DealAdmin)
