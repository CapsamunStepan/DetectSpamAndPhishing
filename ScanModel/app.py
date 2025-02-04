from detector import DetectSpamOrPhishing
from tranlateMessage import TranslatorService
from findUrlsInText import extract_urls
from detectPhishingUrl import VirusTotalScanner
from user import API_KEY


if __name__ == "__main__":
    sms = """Notificare poștală:
    Coletul dumneavoastră a ajuns la depozitul nostru și nu poate fi trimis din cauza informațiilor greșite despre adresă, vă rugăm să completați din nou informațiile exacte despre adresă, îl vom trimite în termen de 24 de ore.

    https://qrco.de/bfScIv?FvT=Amm6E8rG8d"""

    extractUrls = extract_urls(sms)

    scanner = VirusTotalScanner(API_KEY)
    translator = TranslatorService()
    detectedLang = translator.detectLanguage(sms)

    if detectedLang != "en":
        sms = translator.translateAny2Any(sms, detectedLang, 'en')
        # print(f"Переведенное сообщение: {sms}")

    detector = DetectSpamOrPhishing(svm_model_path="spam_model.pkl", vectorizer_path="tfidf_vectorizer.pkl")
    print(f"Результат предсказания: {detector.predict(sms)}")

    if extractUrls:
        for url in extractUrls:
            print(f'Найдена ссылка в тексте: {url}')
            scan_id = scanner.scan_url(url)
            if scan_id:
                scanner.get_report(scan_id)
