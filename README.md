# Scoring-Assistant
## 概要
manabaで提出されたjavaとjar、cの課題を実行して、実行結果を取得するツール

## 利用環境
- `java`コマンド
- `gcc`
- `python=3.11`
  - `astyle_py`
  - `chardet`
  - `jsonschema`
  - `pathlib`

## 使い方
1. report-12345のような構造のディレクトリを対象にし、対象内に各種情報を記載した`settings.json`を配置する
    ```
    test/
    ├── report-12345
    │   ├── result.txt
    │   ├── settings.json
    │   ├── user-01
    │   │   ├── Arith.java
    │   │   ├── InputLoop.java
    │   │   ├── ListLibArray.jar
    │   │   ├── ListSample.java
    │   │   ├── PhoneNumbers.java
    │   │   ├── report02-1.c
    │   │   └── report02-2.c
    │   └── user-02
    │       ├── Arith.java
    │       ├── InputLoop.java
    │       ├── ListLibArray.jar
    │       ├── ListSample.java
    │       ├── PhoneNumbers.java
    │       ├── report02-1.c
    │       └── report02-2.c
    └── share
        ├── Cell.java
        └── phones.csv
    ```
2. main.pyを実行する。\
```python main.py ./test/report-12345```
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


