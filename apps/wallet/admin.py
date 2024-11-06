from django.contrib import admin

from apps.wallet.models import WalletModel, CardModel, TransactionsModel, TransferW2WModel, \
    WalletTransactionsModel, \
    Epos, BalanceModel, Commission, Identification, ReceiverCardModel

from .models.paynet import Category,Providers
# Register your models here.

admin.site.register(WalletModel)
admin.site.register(CardModel)
admin.site.register(WalletTransactionsModel)
admin.site.register(TransferW2WModel)
admin.site.register(TransactionsModel)
admin.site.register(Epos)
admin.site.register(BalanceModel)
admin.site.register(Commission)
admin.site.register(Category)
admin.site.register(Providers)
admin.site.register(Identification)
admin.site.register(ReceiverCardModel)

