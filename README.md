# 国会会議録からのキーフレーズ抽出


## 会議録ダウンロード
```
curl -o {minid}.json  "https://kokkai.ndl.go.jp/api/meeting?issueID={minid}&recordPacking=json"
```
- minid: 119804319X00920190508
	- minId in the url like https://kokkai.ndl.go.jp/#/detail?minId=119804319X00920190508&spkNum=0

### JSON format
```
{
  "numberOfRecords": 総結果件数 ,
  "numberOfReturn": 返戻件数 ,
  "startRecord": 開始位置 ,
  "nextRecordPosition": 次開始位置 ,
  "meetingRecord":[
    {
      "issueID": 会議録ID ,
      "imageKind": イメージ種別（会議録・目次・索引・附録・追録） ,
      "searchObject": 検索対象箇所（議事冒頭・本文） ,
      "session": 国会回次 ,
      "nameOfHouse": 院名 ,
      "nameOfMeeting": 会議名 ,
      "issue": 号数 ,
      "date": 開催日付 ,
      "closing": 閉会中フラグ ,
      "speechRecord":[
        {
          "speechID": 発言ID ,
          "speechOrder": 発言番号 ,
          "speaker": 発言者名 ,
          "speakerYomi": 発言者よみ（※会議単位出力のみ） ,
          "speakerGroup": 発言者所属会派（※会議単位出力のみ） ,
          "speakerPosition": 発言者肩書き（※会議単位出力のみ） ,
          "speakerRole": 発言者役割（※会議単位出力のみ） ,
          "speech": 発言（※会議単位出力のみ） ,
          "startPage": 発言が掲載されている開始ページ（※会議単位出力のみ） ,
          "createTime": レコード登録日時（※会議単位出力のみ） ,
          "updateTime": レコード更新日時（※会議単位出力のみ） ,
          "speechURL": 発言URL ,
        },
        {
          （次の発言情報）
        }
      ],
      "meetingURL": 会議録テキスト表示画面のURL ,
      "pdfURL": 会議録PDF表示画面のURL（※存在する場合のみ） ,
    },
    {
      （次の会議録情報）
    }
  ]
}

```


## 関連ライブラリ
- spacy
- ginza
- pke (https://github.com/boudinfl/pke)

### Install
```
python -m pip install spacy ginza ja_ginza 
pip install git+https://github.com/boudinfl/pke.git
```
