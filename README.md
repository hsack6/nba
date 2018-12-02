# NBA Players stats since 1950

## データの用意
### ディレクトリ構成

    MakeGraph.py
    original---player_data.csv
             |-Players.csv
             |-Seasons_Stats.csv
    graph---node.csv
          |-time_series_graph.csv

### Player nodeが持つ属性
+ name(c, Players)
+ height(c, Players)
+ weight(c, Players)
+ collage(c, Players)
+ birth_city(c, Players)
+ birth_state(c, Players)
+ born(c, Players)
+ year(x, Seasons_Stats)
+ position(x, Seasons_Stats)
+ Tm(x, Seasons_Stats)
+ Age(= year-bornだけど, Seasons_Stats)
+ all_ohers_Stats(x, Seasons_Stats)

### node.csv
上記、カラムを有するcsvをname>yearでソート。
0 Alex 1950 ・・・  
0 Alex 1951 ・・・  
0 Alex 1952 ・・・  
1 Michel 1950 ・・・  
1 Michel 1951 ・・・  
1 Michel 1952 ・・・  

### 放置
下記、36歳以上切り捨てで一旦回避。欠損値全て切り捨てで一旦回避。
+ Players.csvの記入ミス(Harrison Barnes と Harry Barnes等)
+ Players.csvの同姓同名問題(player_data.csv参照で解決できそう)
+ 一つでもNaNを持つものをdrop
+ 同シーズン複数チームで出場している選手を排除。

### originalの修正
+ Players.csvのHarrison Barnesのborn,collage,height,weightを修正。（Harry Barnesと混同されていた。）
+ player_data.csvのBobby Wilsonのbirth_dateを追加。

### time_series_graph.csv
上記、カラム+リンクのエンコード情報(value, one-hot等)を有するcsvをyear>nameでソート。  
1950 0 Alex ・・・ リンク情報  
1950 1 Michel ・・・ リンク情報  
1951 0 Alex ・・・ リンク情報  
1951 1 Michel ・・・ リンク情報  
1952 0 Alex ・・・ リンク情報  
1952 1 Michel ・・・ リンク情報  
