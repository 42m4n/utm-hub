import logging
from django.core.cache import cache
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from common.conf import UTM

logger = logging.getLogger(__name__)


class UTMHandler:
    def __init__(self, utm_name):
        self.utm_name = utm_name
        self.utm_token = next((_['UTM_TOKEN'] for _ in UTM.utms if _['UTM_NAME'] == utm_name), None)
        self.utm_path = next((_['UTM_ADDRESS'] for _ in UTM.utms if _['UTM_NAME'] == utm_name), None)
        self.headers = {
            'Authorization': f'Bearer {self.utm_token}',
            'Content-Type': 'application/json'
        }
        self.interfaces_url = f'https://{self.utm_path}/{UTM.utm_interfaces_api}'
        self.services_url = f'https://{self.utm_path}/{UTM.utm_services_api}'
        self.timeout = 20

    def get_services(self, search_field=None):

        cache_key = f'utm_services_{search_field.lower()}' if search_field else 'utm_services'
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info('Get UTM services from cache')

            return cached_data
        else:
            try:
                logger.info('Get services from UTM')
                response = requests.get(self.services_url, headers=self.headers, verify=False, timeout=self.timeout)
                response = response.json()
                services = response.get('results')
                result = []
                for i, obj in enumerate(services, start=1):
                    new_obj = {"name": obj["name"], "id": i}
                    result.append(new_obj)
                if search_field:
                    result = [i for i in result if
                              i['name'].lower().startswith(search_field.lower()) or (
                                      len(search_field) >= 3 and search_field.lower() in i['name'].lower())]
                    cache.set(f'utm_services_{search_field}', result)
                else:
                    cache.set('utm_services', result)
                return result
            except requests.exceptions.Timeout:
                logger.error(f'Request to {self.utm_name} on {self.utm_path} timed out')
            except Exception as e:
                logger.error(f'Error at getting utm services: {e}')

    def get_interfaces(self, search_field=None):
        cache_key = f'utm_interfaces_{search_field.lower()}' if search_field else 'utm_interfaces'
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info('Get UTM interfaces from cache')
            return cached_data
        else:
            try:
                logger.info('Get interfaces from UTM')
                response = requests.get(self.interfaces_url, headers=self.headers, verify=False, timeout=self.timeout)
                response = response.json()
                services = response.get('results')
                result = [{"name": "any", "id": 1}]
                for i, obj in enumerate(services, start=2):
                    new_obj = {"name": obj["name"], "id": i}
                    result.append(new_obj)
                if search_field:

                    result = [i for i in result if
                              i['name'].lower().startswith(search_field.lower()) or (
                                      len(search_field) >= 3 and search_field.lower() in i['name'].lower())]
                    cache.set(f'utm_interfaces_{search_field}', result)
                else:
                    cache.set('utm_interfaces', result)
                return result
            except requests.exceptions.Timeout:
                logger.error(f'Request to {self.utm_name} on {self.utm_path} timed out')
            except Exception as e:
                logger.error(f'Error at getting utm interfaces: {e}')
