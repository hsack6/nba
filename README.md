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

# NBA Dataset Glossary
https://www.basketball-reference.com/about/glossary.html
+ Year　：　NBAシーズンは2年にまたがっているので、与えられるYearはそのシーズンの後ろの年。 例えば1999-2000シーズンのYearは2000。
+ Pos　：　ポジション
    - G : ガード
    - PG : ポイントガード
    - SG : シューティングガード
    - F : フォワード    
    - SF : スモールフォワード
    - PF : パワーフォワード
    - C : センター
    - G-F : ガードフォワード
    - F-C : フォワードセンター
    - F-G : フォワードガード
    - C-F : センターフォワード
    - PF-C : フォワードセンター
+ Tm　：　チーム
+ G　：　試合数
+ GS　：　先発出場数
+ MP　：　出場時間
+ PER　：　Player Efficiency Rating。 時間あたりの選手の価値。選手が時間あたりに残したスタッツをもとに計算される。平均を15とする偏差値で表す。計算式　http://hoops-stats.hatenablog.com/entry/2018/08/04/151640
+ TS%　：　＝PTS/(2 * TSA)。　True Shooting Percentage。 3ポイントライン外のフィールドゴール(2点), 3ポイントフィールドゴール(3点), フリースローを含めたたシュート効率の指標。
+ PTS　：　得点。
+ TSA　：　＝FGA + 0.44*FTA。　True Shooting Attempts。　
+ FGA　：　2ポイント、3ポイント含むフィールドゴールを試みた回数。Field Goal Attempts。
+ FTA　：　フリースローを試みた回数。
+ 3PAr　：　= (3PA / FGA)。　3-Point attempt rate. Percentage of FG Attempts from 3-point Range.
+ FTr　：　= (FTA / FGA)。　Free Throw Attempt Rate. Number of FT attempts per FG attempts.
+ ORB%　：　＝100 * (ORB * (Tm MP / 5)) / (MP * (Tm ORB + Opp DRB))。　Offensive Rebound Percentage。
+ ORB　：　オフェンシブリバウンド回数。
+ Tm MP　：　チームの出場時間。
+ Tm ORB　：　チームのオフェンシブリバウンド回数。
+ Opp DRB　：　相手チームのディフェンシブリバウンド回数。
+ DRB　：　 ＝100 * (DRB * (Tm MP / 5)) / (MP * (Tm DRB + Opp ORB))。　Defensive Rebound Percentage。
+ DBR　：　ディフェンシブリバウンド回数。
+ Tm DRB　：　チームのディフェンシブリバウンド回数。
+ Opp ORB　：　相手チームのオフェンシブリバウンド回数。
+ TRB%　：　＝100 * (TRB * (Tm MP / 5)) / (MP * (Tm TRB + Opp TRB))。　Total Rebound Percentage。
+ TRB　：　トータルリバウンド回数。
+ Tm TRB　：　チームのトータルリバウンド回数。
+ Opp TRB　：　相手チームのトータルリバウンド回数。
+ AST%　：　＝100 * AST / (((MP / (Tm MP / 5)) * Tm FG) - FG)。 Assist Percentage。
+ AST　：　アシスト回数。
+ FG　：　フィールドゴール回数。
+ Tm FG　：　チームのフィールドゴール回数。
+ STL%　：　＝100 * (STL * (Tm MP / 5)) / (MP * Opp Poss)。
+ STL　：　スティール（ディフェンスがオフェンスから奪った）回数。
+ Opp poss　：　相手チームのPoss。
+ Poss　：　＝0.5 * (  
    (Tm FGA + 0.4 * Tm FTA - 1.07 * (Tm ORB / (Tm ORB + Opp DRB)) * (Tm FGA - Tm FG) + Tm TOV) +   
    (Opp FGA + 0.4 * Opp FTA - 1.07 * (Opp ORB / (Opp ORB + Tm DRB)) * (Opp FGA - Opp FG) + Opp TOV))。
    Posessions。ボールの所有権、攻撃機会。シュート成功、ターンオーバー、ディフェンスリバウンドでポゼッションは相手に移る。オフェンスが終わりディフェンスに切り替わって初めて１回とカウントされる。
    単純な式＝シュート打った数 +（0.44*）フリースローを打った数 - オフェンスリバウンド + ターンオーバー。
+ Opp TOV　：　相手チームのターンオーバー数。
+ TOV　：　ターンオーバー数。オフェンスのミス（シュート除く）。
+ BLK%　：　＝100 * (BLK * (Tm MP / 5)) / (MP * (Opp FGA - Opp 3PA))。 Block Percentage。
+ BLK　：　ブロック数。
+ TOV%　：　＝100 * TOV / (FGA + 0.44 * FTA + TOV)。　Turnover Percentage。
+ USG%　：　＝ 100 * ((FGA + 0.44 * FTA + TOV) * (Tm MP / 5)) / (MP * (Tm FGA + 0.44 * Tm FTA + Tm TOV))。　Usage Percentage。　その選手のシュート/ファール獲得/ターンオーバーで終わったポゼッションの割合。
+ blanl, blank2 : 不明。全部欠損値。
+ OWS　：　オフェンスでどれだけ勝利に貢献したか。計算式　https://www.basketball-reference.com/about/ws.html。http://basketballbbs.com/nba/34756/。
+ DWS　：　ディフェンスでどれだけ勝利に貢献したか。計算式はOWSのリンク参照。
+ WS　：　その選手がどれだけ勝利に貢献したか。計算式OWSのリンク参照。
+ WS/48　：　WS/48minutes。計算式はOWSのリンク参照。
+ OBPM　：　オフェンスのBPM　
+ DBPM　：　ディフェンスのBPM
+ BPM　：　リーグ平均選手上の平均的なチームに変換された、選手が貢献した100ポゼッション当たりの得点の推定値。計算式　https://www.basketball-reference.com/about/bpm.html。
+ VORP　：　[BPM – (-2.0)] * (% of minutes played) * (team games/82). 説明　https://www.basketball-reference.com/about/bpm.html#vorp。
+ FG%　：　＝ FG / FGA。
+ 3P　：　3-ポイントフィールドゴール数。
+ 3PA　：　3-ポイントフィールドゴール試行数。
+ 3P%　：　＝ 3P / 3PA。
+ 2P　：　2-ポイントフィールドゴール数。
+ 2PA　：　2-ポイントフィールドゴール試行数
+ 2P%　：　＝ 2P / 2PA。
+ eFG%　：　＝ (FG + 0.5 * 3P) / FGA。　フィールドゴールの効率性。
+ FT　：　フリースロー入った数。
+ FT%　：　＝ FT / FTA。
+ PF　：　個人のファール数。
