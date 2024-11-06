from services.unigate import methods as Gwmethods

def get_card_info(card_number, expire):
    """Retrieve card information from the humo_register method."""
    try:
        card_info = Gwmethods.humo_register(number=card_number, expire=expire)
        if 'result' in card_info:
            return card_info
        else:
            return None  # or raise an exception
    except Exception as e:
        raise ValueError("Error retrieving card info: " + str(e))
