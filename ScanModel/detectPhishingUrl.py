import requests
from time import sleep

from user import API_KEY


class VirusTotalScanner:
    def __init__(self, api_key):
        self.api_key = api_key
        self.scan_url_api = 'https://www.virustotal.com/vtapi/v2/url/scan'
        self.report_url_api = 'https://www.virustotal.com/vtapi/v2/url/report'

    def scan_url(self, url):
        params = {'apikey': self.api_key, 'url': url}
        response = requests.post(self.scan_url_api, data=params)

        if response.status_code == 200:
            result = response.json()
            return result.get('scan_id')  # Возвращаем scan_id для использования в get_report
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return None

    def get_report(self, resource, retries=6, delay=5):
        params = {'apikey': self.api_key, 'resource': resource}

        for _ in range(retries):
            response = requests.get(self.report_url_api, params=params)

            if response.status_code == 200:
                data = response.json()

                if data.get('response_code') == 1:  # Проверяем, что отчет готов
                    if data['positives'] > 0:
                        print(f"Количество обнаружений угроз    : {data['positives']}")

                        # Пройтись по сервисам и вывести те, где 'detected' == True
                        for service, result in data['scans'].items():
                            if result['detected']:
                                print(f"{service}: {result['result']}")
                    else:
                        print("Нет угроз, URL чист.")
                    break
                else:
                    print(f"Отчет еще не готов. Ожидание {delay} секунд...")
            elif response.status_code == 204:
                print(f"Превышено количество запросов. Ожидание {delay} секунд перед повторной попыткой...")
            else:
                print(f"Ошибка {response.status_code}: {response.text}")

            sleep(delay)  # Ждем перед повторной попыткой


if __name__ == '__main__':
    url_to_scan = 'https://qrco.de/bfScIv?FvT=Amm6E8rG8d'
    scanner = VirusTotalScanner(API_KEY)

    # Сначала запускаем сканирование URL
    scan_id = scanner.scan_url(url_to_scan)

    if scan_id:
        # Затем получаем отчет с периодической проверкой
        scanner.get_report(scan_id)
