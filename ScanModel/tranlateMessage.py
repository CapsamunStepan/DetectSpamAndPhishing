from googletrans import Translator


class TranslatorService:
    def __init__(self):
        self.translator = Translator()

    def translateFromRu2En(self, text):
        translated = self.translator.translate(text, src='ru', dest='en')
        return translated.text

    def translateFromEn2Ru(self, text):
        translated = self.translator.translate(text, src='en', dest='ru')
        return translated.text

    def translateAny2Any(self, text, src, dest):
        translated = self.translator.translate(text, src=src, dest=dest)
        return translated.text

    def detectLanguage(self, text):
        detected = self.translator.detect(text)
        return detected.lang


if __name__ == "__main__":
    translator = TranslatorService()
    print(translator.translateFromRu2En("Привет, мир"))
    print(translator.translateFromEn2Ru("lets go home"))
    print(translator.detectLanguage("Hola amigos"))
    print(translator.detectLanguage("Ola amiga"))
