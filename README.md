# GCGNN
GCGNNのアーキテクチャ詳細。

## InputGraph
GCGNNへの入力グラフを生成する。入力グラフは、過去Mステップで観測されたノード集合とリンク集合、将来Hステップで出現を予測されたノード集合とリンク集合を含む。

### 欲しい機能
+ 未知ノード数と復帰ノード数の取得。
    - PredictNodeNum関数の修正。
        + modeをunknown, return, lostの3つにする。
    - new_node()からGetNewNode()に名前変更。
    - loss_node()からGetLostNode()に名前変更。
    - 得られたnew_nodeをreturn_nodeとunknown_nodeに振り分ける。
        + GetUnknownNode(new_node, GetObservedNodeSet(M))
        + GetReturnNode(new_node, GetObservedNodeSet(M))
    - GetObservedNodeSet(M) の作成。過去Mステップで観測されたノード集合を返す。






# EDA と Feature Engineering

NBAデータセットのEDAとFeature Engineeringに関するメモ。

## データの用意
NBA Players stats since 1950 https://www.kaggle.com/drgilermo/nba-players-stats

## ディレクトリ構成
上記URLからDLしてきたファイル（original/以下）を修正し、EDA/に保存する。

    EDA.py
    original---player_data.csv
             |-Players.csv
             |-Seasons_Stats.csv
    EDA---player_data.csv
         |-Players.csv
         |-Seasons_Stats.csv
         |-EDA.csv

## originalの修正
+ Players.csvのHarrison Barnesのborn,collage,height,weightを修正。（Harry Barnesと混同されていた。）
    - EDA.pyの中に修正コードを置いたのでおそらく変更せずとも動く。
+ player_data.csvのBobby Wilsonのbirth_dateが抜けていたので追加。
+ player_data.csvのJohn LucasをJohn Lucas 0に,John Lucas ⅢをJohn Lucas 1に変更。

## NBAデータセット用語
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
+ Tm　：　チーム。データセットに含まれるチーム数はTOT含めて69。2018現在、activeなチーム数は30。
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

# データ分析のプロセス
EDAとFeature Engineeringについては何も考えずに始めると作業を深堀しすぎたり、抜け漏れが起こるためここにやることをまとめておく。
データ分析のプロセスとして大まかに
+ データの理解(EDA)
+ データの準備(Feature Engineering)
+ モデリング
に分けれられる。機械学習を扱うとなると、モデリングに注目しがちであるが、実際の作業量としては、それより前のステップであるデータの理解とデータの準備のステップが大半を占める。

## データの理解（EDA）
EDAを行う目的としては、データの特徴や構造を理解することが挙げられる。データの理解を怠れば、この後のデータの準備ステップで適切な前処理やFeature Engineeringを行うことはできない。
### やることリスト
+ データの各特徴名とその意味の確認
+ データの大きさの確認(pandasの.shape)
+ 表の一部分表示(pandasの.dtypes())
+ 特徴量ごとの平均値、最大値、最小値などの統計量確認(pandasの.describe())
+ 欠損値チェック(pandasの.isnull().sum())
+ ヒストグラムによる分布の可視化
+ 散布図や箱ひげ図を用いた目的変数と、説明変数の関係の可視化
+ 時系列データであれば、時系列トレンドの可視化
+ 外れ値の確認
+ 次元削減による可視化(PCA, T-SNE, UMAP)
+ 複数のカテゴリ特徴で分割したときの傾向確認(数が膨大になるため、仮定を置いてから実行)

### 便利ツール
+ pandas-profiling
+ missingno
+ seaborn.heatmap

## データの準備(Feature Engineering、前処理)

### やることリスト
+ 外れ値の除去
+ 欠損値の補完または除去
+ 数値型特徴の対数化
+ 数値型特徴のカテゴリ化
+ 数値型特徴の正規化
+ カテゴリ型特徴のダミー変数化
+ カテゴリ型特徴の集約
+ カテゴリ型特徴の組み合わせ特徴生成
+ 多項式特徴量の作成

### 便利ツール
+ sklearn.preprocessing
+ featuretools(特徴量を自動で生成してくれるツール)
+ automl系のライブラリ(前処理とモデリングを含めて最適化してくれるツール)
    - auto-sklearn
    - TPOT

## モデリング
特徴量の重要度を求めることで、重要となる特徴量や不要である特徴量が何であるかを考察することができる。この結果を受けて、特徴量の作成をし直したり、モデル解釈の補助をすることができる。
###　やることリスト
+ 目的変数と説明変数間の相関係数
+ ラッソ回帰やリッジ回帰による抽出
+ 決定木ベースのモデルによる重要度抽出(Random Forest, XGBoost, LightGBM)
+ 学習モデル解釈の手法(LIME, SHAP)
+ 決定木の可視化(dtreeviz)

### 便利ツール
+ sklearn.feature_selection.SelectKBest
+ sklearn.feature_selection.RFE
+ sklearn.feature_selection.SelectFromModel
+ mlflow(モデルの管理をしてくれるツール)

## 参考
https://qiita.com/masa26hiro/items/ce5f60e2950e072a0910


# Player nodeが持つ属性
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

# node.csv
上記、カラムを有するcsvをname>yearでソート。
0 Alex 1950 ・・・  
0 Alex 1951 ・・・  
0 Alex 1952 ・・・  
1 Michel 1950 ・・・  
1 Michel 1951 ・・・  
1 Michel 1952 ・・・  

# 放置
下記、36歳以上切り捨てで一旦回避。欠損値全て切り捨てで一旦回避。
+ Players.csvの記入ミス(Harrison Barnes と Harry Barnes等)
+ Players.csvの同姓同名問題(player_data.csv参照で解決できそう)
+ 一つでもNaNを持つものをdrop
+ 同シーズン複数チームで出場している選手を排除。

# time_series_graph.csv
上記、カラム+リンクのエンコード情報(value, one-hot等)を有するcsvをyear>nameでソート。  
1950 0 Alex ・・・ リンク情報  
1950 1 Michel ・・・ リンク情報  
1951 0 Alex ・・・ リンク情報  
1951 1 Michel ・・・ リンク情報  
1952 0 Alex ・・・ リンク情報  
1952 1 Michel ・・・ リンク情報  
