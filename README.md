# change3

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
+ name(c)
+ height(c)
+ weight(c)
+ collage(c)
+ birth_city(c)
+ birth_state(c)
+ position(x)
+ Tm(x)
+ Age(= year-bornだけど)
+ year(x:year_start〜year_end)
+ born(c)
+ all_Stats(x)

### node.csv
上記、カラムを有するcsvをname>yearでソート。同姓同名がいるのでplayerごとにユニークなIDを付与。  
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
