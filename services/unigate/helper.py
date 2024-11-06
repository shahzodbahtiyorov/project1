



def expire_date_format(expire_raw):
    string = expire_raw.split('/')

    date = [int(num) for num in string]

    if date[1] > 12:
        result = expire_raw[3:] + expire_raw[:2]

        return result


def transform_date_format(date_str):
    month, day = date_str.split('/')

    transformed_date = day + month

    return transformed_date

def mask_card_number(card_number):
    card_number_str = str(card_number)

    length = len(card_number_str)

    if length <= 8:
        return card_number_str

    masked_part = '*' * (length - 8)

    return card_number_str[:4] + masked_part + card_number_str[-4:]