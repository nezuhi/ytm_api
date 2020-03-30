# CSV REQUEST GENERATOR FOR YTM API
The sample code of the command-line tool written in Python which reads the data from the CSV file and sends HTTP requests to Yahoo Tag Manager API endpoints. You can check the usage by running the program with --help option (e.g. "csv_request_generator.py --help").

## Summary
このスクリプトはCSVファイルのヘッダーとカラムのデータを取得してYTMのAPIへ送信します。ターミナルなどから対象のCSVファイルのパスをオプションの引数に入れて実行することで、ファイルの内容を読み取って指定したYTMのサイトID、APIイベントへ向けて送信します。ログファイルのオプションを指定しない場合は画面にレスポンスや送信内容などが表示されます。

### REQUIREMENTS
Python 3の実行環境が必要です。
データソースとなるCSVファイルはUTF-8であること、ヘッダー行が含まれていることが必須です。CSVファイルから取得したヘッダー行とカラムのデータはキーバリューペアとしてhttpリクエストのクエリパラメータにセットされるためヘッダー行のカラムの文字列はYTMで設定したデータバインディングの変数と一致している必要があります。

### USAGE
    usage: csv_request_generator [-h] -f CSVFILE -s SITEID -r REFERRER
                                 [-t [{1,2,3,4,5,6,7,8,9,10}]] [-l [LOGFILE]]
                                 [-m [{preview,diagnostic}]] [-p [{http,https}]]
                                 [-v]

    -h, --help            ヘルプを表示します。

    -f CSVFILE, --file CSVFILE
                          CSVファイルのパスを指定します。
    -s SITEID, --siteid SITEID
                          SITEIDにはYTMのサイトIDを指定してください。
    -r REFERRER, --referrer REFERRER
                          REFERRERにはYTMのAPIイベントのIDを指定してください。
    -t [{1,2,3,4,5,6,7,8,9,10}], --thread [{1,2,3,4,5,6,7,8,9,10}]
                          同時送信数を指定します。このオプションを指定しない場合は[1]、引数を省略した場合は[2]がデフォルト値となります。同時送信数は5以下を指定するようにしてください。
    -l [LOGFILE], --logfile [LOGFILE]
                          このオプションを有効にするとログファイルに[HTTP_CODE,RESPONSE,URL]が記録されます。オプション引数を省略して[-l]を指定した場合はカレントディレクトリに「csv_request_YYYYMMDD-HHMMSS.log」という形式で保存されます。[-l Path]のようにオプションの引数にログファイルのパスを指定することもできます。
    -m [{preview,diagnostic}], --mode [{preview,diagnostic}]
                          プレビューモードで送信する場合に[-m preview]を指定してください。[-m]だけ指定した場合は「preview」がデフォルト値になります。
    -p [{http,https}], --protocol [{http,https}]
                          プロトコルを明示的に指定する場合はこのオプションを有効にします。選択できるプロトコルは「http」もしくは「https」です。このオプションを指定しない場合のデフォルトは「http」です。引数を省略した場合は「https」でリクエストが送信されます。
    -v, --version         バージョンを表示します。

    実行例：
    python csv_request_generator.py -f '/path to file.csv' -s 'abc1234' -r 'api:sample' -t 2 -l

### LIMITATIONS
UTF-8以外の文字コードについてはテストしていません。

### NOTES
スレッド数は送信先のエンドポイントのキャパシティを考慮して常識の範囲内でご指定ください。
