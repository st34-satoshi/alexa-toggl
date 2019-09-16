# alexa-toggl
## Description
alexa skill lambda function  

- 「アレクサ，トグルで{プロジェクト}の{タイトル}を開始して」で[toggl](https://toggl.com/)のタイマーを開始する．  
- 「アレクサ，トグルで時間を止めて」で[toggl](https://toggl.com/)のタイマーを停止する．  

## Usage  
### toggl api token の設定
- lambda_function.pyのtokenを設定する．トークンは [Toggl My Profile](https://www.toggl.com/app/profile)で確認できる

### AWS lambda にアプロードするlambda.zipファイルの作成  
- `pip install -r requirements.txt -t skill_env`  
- `cp -r lambda/* skill_env/`  
- `cd skill_env/`
- `zip -r9 ../lambda.zip .`  


## Reference
