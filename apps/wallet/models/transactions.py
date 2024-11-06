import uuid
from datetime import time, datetime

from django.db import models

from apps.wallet.models import WalletModel
from super_app import settings


def generate_transaction_id(prefix):
    unique_id = str(uuid.uuid4())[:8]
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    transaction_id = f"{prefix}{unique_id}{current_time}"
    return transaction_id


METHOD_OPTION_CHOICES = (
    ('WalletToCard', 'wallet-to-card'),
    ('WalletToEpos', 'wallet-to-epos'),
    ('EposToWallet', 'epos-to-wallet'),
    ('CardToWallet', 'card-to-wallet')
)


class TransactionsModel(models.Model):

    debit_tr_id = models.CharField(max_length=255, unique=True)
    sender = models.CharField(max_length=255,blank=True,null=True)
    expire = models.CharField(max_length=255, blank=True, null=True)
    db_amount = models.BigIntegerField(null=True,blank=True)
    sender_ext_id = models.CharField(max_length=255, blank=True, null=True)
    sender_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    db_rrn = models.CharField(max_length=255, null=True,blank=True)
    db_state = models.IntegerField(null=True, blank=True)
    db_currency = models.IntegerField(null=True, blank=True)
    debit_currency = models.CharField(max_length=10, blank=True, null=True)
    db_description = models.CharField(max_length=100, blank=True, null=True)
    receiver = models.CharField(max_length=255, blank=True, null=True)
    receiver_owner = models.CharField(max_length=50, blank=True, null=True)
    cr_tr_id = models.CharField(max_length=255, unique=True)
    cr_rrn = models.CharField(max_length=255, null=True, blank=True)
    cr_state = models.IntegerField(blank=True, null=True)
    cr_description = models.CharField(max_length=100, blank=True, null=True)
    cr_ext_id = models.CharField(max_length=255, blank=True, null=True)
    cr_amount = models.BigIntegerField(blank=True, null=True)
    cr_currency  = models.IntegerField(blank=True, null=True)
    card_to_card = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    credit_currency = models.CharField(max_length=10, blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    commision = models.IntegerField(blank=True, null=True)

    payment_type = models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        if not self.debit_tr_id:
            self.debit_tr_id = generate_transaction_id("SUPER-DB-")
        if not self.cr_tr_id:
            self.cr_tr_id = generate_transaction_id("SUPER-CR-")
        super(TransactionsModel, self).save(*args, **kwargs)




class WalletTransactionsModel(models.Model):
    tr_id = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    amount = models.BigIntegerField()
    expire = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.BooleanField(default=False)
    option = models.CharField(choices=METHOD_OPTION_CHOICES, max_length=55)
    context = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.tr_id} - {self.created_at}"

    class Meta:
        ordering = ('-created_at',)


class TransferW2WModel(models.Model):
    t_id = models.CharField(max_length=255)
    sender = models.ForeignKey(WalletModel, on_delete=models.SET_NULL, related_name="sender",
                               null=True, blank=True)
    receiver = models.ForeignKey(WalletModel, on_delete=models.SET_NULL, related_name="receiver",
                                 null=True, blank=True)
    amount = models.PositiveIntegerField()
    wallet_to_epos = models.CharField(max_length=255, null=True, blank=True)
    epos_to_wallet = models.CharField(max_length=255, null=True, blank=True)
    wallet_to_epos_status = models.BooleanField(default=False)
    epos_to_wallet_status = models.BooleanField(default=False)
    wallet_to_epos_id = models.IntegerField(null=True, blank=True)
    epos_to_wallet_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)


class Epos(models.Model):
    terminal_id = models.CharField('Terminal ID', max_length=30)
    merchant_id = models.CharField('Merchant ID', max_length=20)
    state = models.IntegerField('State', default=0)
    type = models.IntegerField(default=0)
    pc_type = models.IntegerField(default=0)
    is_active = models.BooleanField('Epos status', default=True)
    status = models.IntegerField(default=0)
    purpose = models.CharField('Purpose of Usage', max_length=30, null=True)
    account = models.CharField('Account Number ', max_length=45, null=True)
    point_code = models.CharField('Point Code', max_length=30, null=True)
    commission = models.FloatField("Commission for EPOS", default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Commission(models.Model):
    name = models.CharField(max_length=128, null=True)
    in_merchant = models.CharField(max_length=64, null=True)
    in_terminal = models.CharField(max_length=64, null=True)
    in_terminal_account = models.CharField(max_length=128, null=True)
    out_merchant = models.CharField(max_length=64, null=True)
    out_terminal = models.CharField(max_length=64, null=True)
    out_terminal_account = models.CharField(max_length=128, null=True)
    percentage = models.FloatField(max_length=10, null=True, default=0.0)

    def __str__(self):
        return self.name


class PaynetSave(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    category_id = models.IntegerField(null=True)
    provider_id = models.IntegerField(null=True)
    service_id = models.IntegerField(null=True)
    fields = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.category_id} - {self.provider_id} - {self.service_id}"
