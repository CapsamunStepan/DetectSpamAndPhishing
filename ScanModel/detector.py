import joblib


class DetectSpamOrPhishing:
    def __init__(self, svm_model_path, vectorizer_path):
        self.svm_model = joblib.load(f"{svm_model_path}")
        self.vectorizer = joblib.load(f"{vectorizer_path}")

    def predict(self, message):
        message = self.vectorizer.transform([message])
        prediction = self.svm_model.predict(message)
        return prediction[0]


if __name__ == "__main__":
    detector = DetectSpamOrPhishing(svm_model_path="spam_model.pkl", vectorizer_path="tfidf_vectorizer.pkl")
    message2check = "Sure thing big man. i have hockey elections at 6, shouldn€˜t go on longer than an hour though"

    print(f"Результат предсказания: {detector.predict(message2check)}")
