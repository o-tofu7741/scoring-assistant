# Scoring-Assistant
## 概要
manabaで提出されたjavaとjarの課題を実行して、実行結果を取得するツール

## 利用環境
- `java`コマンド
- `python=3.11`

## 使い方
1. 以下の構造のディレクトリを対象にし、対象内に各種情報を記載した`settings.json`を配置する
    ```
    report-12345/
    ├── user-01
    │   ├── Arith.java
    │   └── PhoneNumbers.java
    ├── user-02
    │   ├── Arith.java
    │   └── PhoneNumbers.java
    ├── phones.csv              // (任意)
    └── settings.json
    ```
2. main.pyを実行する。\
```python main.py [path-to-target-directory]```
3. `[path-to-target-directory]`の直下に`result.txt`が出力される

## `settings.json`について
基本は`json-schema.json`を確認
|名前|型|説明|必須|
|----|----|----|----|
|tasks|array|各種課題|○|
|tasks/name|string|ファイル名|○|
|tasks/lang|string|ファイルの言語|○|
|tasks/inputs|array|標準入力たち||
|tasks/inputs/input|string|標準入力を文字列で記述、改行スペース可|△|
|tasks/args|array|実行時引数たち||
|tasks/args/arg|array[string]|実行時引数を配列で記述|△|


