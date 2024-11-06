from django.urls import path


from api.wallet.modules.tcb import transfer_callback

from api.wallet.views import *
from api.wallet.views.identification import identification_id
from api.wallet.views.monitoring import *
from api.wallet.views.paynet import *
from api.wallet.views.tcb import services_info, cards_register, transfer_receivers_info, create_transfer, \
    transfer_tcb_callback, card_state_register
from api.wallet.views.visa import visa_login

urlpatterns = [
    # wallet balance
    # path("balance", get_wallet_balance_view),
    # path("card-add-step-one", card_add_step_one),
    # path("card-add-step-two", card_add_step_two),
    # Card management endpoints
    # path("get-cards", get_cards),
    path("card2wallet-create", transfer_to_wallet),
    path("delete_card", delete_card),
    path("card2wallet-confirm", confirm_transfer_to_wallet),

    path("wallet2wallet-create", create_wallet_to_wallet),
    path("wallet2wallet-confirm", confirm_wallet_to_wallet),
    path("history", wallet_history),

    # Card P2P (peer-to-peer) endpoints
    # Initiates the process of adding a new card
    path('card_add_step_one', card_create_add),  # step one send otp to user phone
    path('card_add_step_two', card_uzcard_info),  # card add uzcard
    path('card_add_humo', card_humo_add),  # card add  humo
    path("card_info", card_info),  # card info
    path("card_transfer", card_p2p_transfer),  # card transfer

    path("card_transfer_confirme", transfer_otp_confirme),  # tr ansfer confirme
    path("card_balance", cards_user_get),  # cards balance

    path('create_epos', create_epos),  # epos create
    path('card_blocked', cards_blocked),
    path('card/name/update', card_update_name),

    #paynet
    path('categories', categories_all),  # paynet categories
    path('providers', providers_all),  # paynet providers
    path('services', services_all),  # Paynet services
    path('service_by_category_filter', service_by_category_filter),  # Filter services by category
    path('search_by_service', service_search),  # Search services,
    # path('service_get_provider/',service_get_providers),
    path('check_receiver/', checks_receiver),
    path('payment_create', payment_transfer),
    path('payment_confirme', payment_confirm),

    ################# Monitoring ################################
    # path('monitoring', monitor),
    path('card_monitoring', card_monitor),
    path('card/monitoring', card_all_monitoring),
    path('card/monitoring/check', check_monitoring),
    path('transaction/status',state_transactions),
    path('api/generate_pdf',transfer_pdf),
    ###########   MY_ID
    path('identification', identification_id),
    path('my_id_info', my_id_info),
    path('user_notification',user_notification),
    ##################TCB RF--->UZ #####################################
    path('tcb_service_info/', services_info),
    path('card_tcb_register', cards_register),
    path('callback/card', card_state_register),
    path('transfer_receivers_info', transfer_receivers_info),
    path('transfer_create', create_transfer),
    path('callback/transfer', transfer_tcb_callback),
    ##################TCB UZ--->RF #####################################
    path('receiver/info', transfer_rf_sender_check),
    path('transfer/create', transfer_create_rf),
    path('transfer/confirm', transfer_confirm_rf),
    ################Visa########################
    path('visa/login', visa_login),
    path('visa/card/register', visa_register_card),
    path('visa/card/confirm',visa_card_confirm),
    path('visa/bin/check',visa_card_bin_check),
    path('visa/card/detail',visa_card_token),
    ###############Receiver Info ##############
    path('receiver/create/card',receiver_create),
    path('get_receiver/card',get_receiver_cards)

]
