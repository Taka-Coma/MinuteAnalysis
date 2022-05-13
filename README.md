# 国会会議録からのキーフレーズ抽出


## 会議録ダウンロード
```
curl -o {minid}.json  "https://kokkai.ndl.go.jp/api/meeting?issueID={minid}&recordPacking=json"
```
- minid: 119804319X00920190508
	- minId in the url like https://kokkai.ndl.go.jp/#/detail?minId=119804319X00920190508&spkNum=0
