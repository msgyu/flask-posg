# Pythonの公式イメージを使用
FROM python:3.9

# 作業ディレクトリを設定
WORKDIR /app

# 依存パッケージをインストール
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# アプリケーションコードをコピー
COPY app/ .

# アプリケーションを起動
CMD ["python", "app.py"]

