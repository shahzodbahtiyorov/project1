import uuid
from .dragon import basic_fire
from django.core.cache import cache


def days_to_seconds(days):
    return days * 86400


def categories():
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "services.categories",
        "params": {}
    }
    return basic_fire(payload)


def get_cached_categories():
    category = cache.get('categories')
    if not category:
        category = categories()
        if category:
            cache.set('categories', category, timeout=days_to_seconds(1))
    return category


def providers(category_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "services.providers",
        "params": {
            "category_id": category_id
        }
    }
    return basic_fire(payload)


def get_cached_providers(category_id):
    cache_key = f'providers_{category_id}'
    provider = cache.get(cache_key)
    if not provider:
        provider = providers(category_id)
        if provider:
            cache.set(cache_key, provider, timeout=days_to_seconds(7))
    return provider


def services(provider_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "services.get.provider",
        "params": {
            "provider_id": provider_id
        }
    }
    return basic_fire(payload)


def get_cached_services(provider_id):
    cache_key = f'services_{provider_id}'
    service = cache.get(cache_key)
    if not service:
        service = services(provider_id)
        if service:
            cache.set(cache_key, service, timeout=days_to_seconds(7))

    return service


def services_filter_by_category(category_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "services.filter.by.category",
        "params": {
            "category_id": category_id
        }
    }
    return basic_fire(payload)


def get_cached_services_filter_by_category(category_id):
    cache_key = f'services_filter_by_category_{category_id}'
    service = cache.get(cache_key)
    if not service:
        service = services_filter_by_category(category_id)
        if service:
            cache.set(cache_key, service, timeout=days_to_seconds(7))
    return service


def services_search_by_category(search_text):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "services.search",
        "params": {
            "search_text": search_text
        }
    }

    return basic_fire(payload)


def get_cashed_search_by_category(search_text):
    cache_key = f'search_by_category_{search_text}'
    search = cache.get(cache_key)
    if not search:
        search = services_search_by_category(search_text)
        if search:
            cache.set(cache_key, search, timeout=days_to_seconds(7))
    return search


def check_receiver(field, service_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "paynet.receiver.check",
        "params": {
            "service_id": service_id,
            "fields": field
        }
    }
    return basic_fire(payload)


def create_transaction(field, service_id, ext_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "paynet.create",
        "params": {
            "ext_id": f"Superapp_{ext_id}",
            "confirm_service": service_id,
            "fields":field

        }
    }
    return basic_fire(payload)


def transaction_confirm(ext_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "paynet.confirm",
        "params": {
            "ext_id": ext_id
        }
    }
    return basic_fire(payload)
