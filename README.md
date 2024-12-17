# step_analysis

# 概要
任意の期間の歩数のデータを曜日ごとに分析するコード．
対象となる歩数のデータは，iPhoneのヘルスケアというアプリからエクスポートしたXMLファイルです．

# 説明
## requirements.txt
step_make_graph.pyを実行するために必要なPythonライブラリの一覧です．
以下のコマンドを実行し，必要なライブラリをインストールします．
```bash
pip install -r requirements.txt
```
## step_calc.py
任意の期間の歩数のデータの平均，第一四分位数，中央値，第三四分位数を曜日ごと出力します．
デフォルトでは，10分間のデータをもとに計算を行います．
### 実行結果
![image](https://github.com/user-attachments/assets/9ff05bb6-6a6f-4196-9dab-57fd5d236e1e)
q1は第一四分位数，medianは中央値，q3は第三四分位数，avgは平均を表しています．

## step_make_graph.py
任意の期間の歩数のデータを曜日ごとにグラフとして出力します．
デフォルトでは，今回基礎実験の対象期間であった2024/8/8~2024/10/16の10週間分の期間のデータを参照したグラフを出力します．
プロットは10分間隔です．
1回の実行で1週間分のグラフが出力されます．
### 実行結果
これは出力されるグラフの一例です．
![image](https://github.com/user-attachments/assets/52514d04-8ab5-4908-ad5e-ab352db57a56)


