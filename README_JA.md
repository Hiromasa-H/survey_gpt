# Survey GPT

キーワードのリストまたは論文タイトルのリストから、シンプルな調査スライドを生成します:

![](img3.png)

## セットアップ
1. このリポジトリをクローンしてください: `git clone https://github.com/Hiromasa-H/survey_gpt.git`
2. survey_gptディレクトリに移動してください: `cd survey_gpt`
3. 必要なパッケージをインストールしてください: `pip install -r requirements.txt`
4. 環境ファイルを追加してください: `touch .env`
5. OpenAI APIキーを追加してください: `echo OPENAI_API_KEY ="ここにAPIキーを入力" >> .env`

## 使い方
1. アプリを実行してください: `python app.py`
2. ブラウザでlocalhostに移動してください: `http://127.0.0.1:5000`（ポートはお使いのマシンによって異なる場合があります）
3. キーワードまたはコンマで区切られたキーワードのリストを入力し、「PDFを生成」をクリックしてください
![](img1.png)
1. PDFスライドの生成を待ってください
2. 結果が生成されたら、ダウンロードしてPDFファイルを保存してください
   - または、--に移動してPDFにアクセスしてください。なお、次回PDFを生成する際にはこのPDFが上書きされます。
   ![](img2.png)
