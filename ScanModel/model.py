import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib


class ModelTrain:
    def __init__(self, csv_dataset, model_name):
        self.svm_model = None
        self.csvDataset = csv_dataset
        self.modelName = model_name
        self.data = self.loadData()
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.vectorizer = None
        self.X_train_tfidf, self.X_test_tfidf = None, None
        self.y_pred = None

    def loadData(self):
        return pd.read_csv(self.csvDataset)

    def trainModel(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data['text'],
                                                                                self.data['type'],
                                                                                test_size=0.2,
                                                                                random_state=42)

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2),
                                          max_df=0.9,
                                          min_df=5,
                                          max_features=5000)
        self.X_train_tfidf = self.vectorizer.fit_transform(self.X_train)
        self.X_test_tfidf = self.vectorizer.transform(self.X_test)

        self.svm_model = SVC(kernel='linear', C=1.0)
        self.svm_model.fit(self.X_train_tfidf, self.y_train)

        joblib.dump(self.svm_model, f'{self.modelName}.pkl')
        joblib.dump(self.vectorizer, 'tfidf_vectorizer.pkl')

    def checkAccuracy(self):
        self.y_pred = self.svm_model.predict(self.X_test_tfidf)
        return accuracy_score(self.y_test, self.y_pred)

    def classificationReport(self):
        return classification_report(self.y_test, self.y_pred)


if __name__ == '__main__':
    train = ModelTrain('sms_spam.csv', 'spam_model')
    train.trainModel()
    print(train.checkAccuracy())
    print(train.classificationReport())
