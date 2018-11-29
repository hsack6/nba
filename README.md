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

### time_series_graph.csv
上記、カラム+リンクのエンコード情報(value, one-hot等)を有するcsvをyear>nameでソート。  
1950 0 Alex ・・・ リンク情報  
1950 1 Michel ・・・ リンク情報  
1951 0 Alex ・・・ リンク情報  
1951 1 Michel ・・・ リンク情報  
1952 0 Alex ・・・ リンク情報  
1952 1 Michel ・・・ リンク情報  
