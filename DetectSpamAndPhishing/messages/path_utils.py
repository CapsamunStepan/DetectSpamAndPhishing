from pathlib import Path


def get_app_root():
    return Path(__file__).resolve().parent  # папка в которой находится файл


def get_path2model():
    app_path = get_app_root()
    model = app_path.parent.parent / 'ScanModel' / 'spam_model.pkl'
    vectorizer = app_path.parent.parent / 'ScanModel' / 'tfidf_vectorizer.pkl'
    return {"model": model, "vectorizer": vectorizer}


def get_path2file_getMessages():
    app_path = get_app_root()
    return app_path.parent.parent / 'ScanModel' / 'getMessages'


if __name__ == '__main__':
    print(get_path2file_getMessages())
