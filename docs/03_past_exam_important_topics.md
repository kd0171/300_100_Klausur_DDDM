# 03 Past exam important topics

この文書は、アップロードされた過去問PDFから、試験対策上重要になりうる論点を抽出したものです。過去問は参考資料であり、出題範囲を限定するものではありません。したがって、各トピックでは「過去にどのように出たか」と「過去問に限らず理解すべきこと」を分けています。

## 優先順位の見方

- **最重要**: 複数年度または大問で出題。新しい事例にも適用できる必要がある。
- **重要**: 出題実績があり、講義全体の理解にも関係する。

## トピック別抽出

### 1. Information Model / Decision Model / Aggregation / Disaggregation [最重要]

- 対応講義: Lecture 1, Lecture 2
- 関連する過去問: SS24 Aufgabe 1a, WS23/24 Aufgabe 2, WS23/24 Aufgabe 3, WS22/23 Aufgabe 3
- 何が問われたか: 情報モデル・決定モデル・集約・実装/非集約の役割、および現実世界とのデータフローが複数回問われている。
- 理解すべきこと: 単語を暗記するだけでなく、Real-World -> Aggregation -> Information Model -> Decision Model -> Implementation/Disaggregation -> Real-World のループとして説明する。配送車両や旅行時間の例に当てはめられるようにする。
- 過去問以外も含む試験対策ポイント: 講義スライド上の図をそのまま説明できること。動的意思決定では、このループが一回きりではなく時間とともに繰り返される点も押さえる。

### 2. Business Analyticsの位置づけとプロセス [重要]

- 対応講義: Lecture 2 / Overview
- 関連する過去問: WS22/23 Aufgabe 2, WS22/23 Aufgabe 3, WS23/24 Aufgabe 1
- 何が問われたか: Business Analyticsを構成する学問分野と、その組み合わせによる交差領域が問われた。BAプロセスとORが担う工程も問われた。
- 理解すべきこと: BAは単なるデータ分析ではなく、データ・モデル・意思決定・実装を結びつけるプロセスであることを説明する。
- 過去問以外も含む試験対策ポイント: OR, Statistics, Computer Science/Information Systemsの関係図を答案用に簡潔に描けるようにする。

### 3. 時間依存旅行時間、FIFO条件、Cheapest Insertionの限界 [最重要]

- 対応講義: Lecture 2
- 関連する過去問: WS22/23 Aufgabe 4, WS23/24 Aufgabe 4, WS23/24 Aufgabe 5, SS25 Exercise 2
- 何が問われたか: 時間帯別平均旅行時間の作成、FIFO条件の意味と違反、時間依存旅行時間でCheapest Insertionが悪い結果を生む理由が問われた。
- 理解すべきこと: 出発時刻が遅いにもかかわらず到着時刻が早くなるような矛盾がFIFO違反。時間依存旅行時間では、ある地点への到着時刻が後続区間の旅行時間も変えるため、静的TSPの挿入費用だけでは判断できない。
- 過去問以外も含む試験対策ポイント: 小さな数値例で、局所的な安い挿入が全体で悪くなる状況を説明できるようにする。

### 4. 不確実性: stochastic / quasi-stochastic / robust / regret / Hurwicz [最重要]

- 対応講義: Lecture 3
- 関連する過去問: WS22/23 Aufgabe 5, SS23 Aufgabe 3, WS23/24 Aufgabe 6, WS23/24 Aufgabe 7, WS24/25 Aufgabe 1, WS24/25 Aufgabe 3, SS25 Exercise 4, SS25 Exercise 8
- 何が問われたか: 旅行時間・サービス時間などの不確実性について、確率分布がある場合とない場合、区間ベースモデル、regret、Hurwicz基準、指数分布サンプリングなどが問われた。
- 理解すべきこと: stochasticは分布があり期待値・分散などが扱える場合。quasi-stochasticは確率が不明で、シナリオ・区間・楽観/悲観値などを使う場合。regretは「後から見た最適解との差」を測り、最大後悔を抑える。Hurwiczは楽観と悲観を重み付けする準確率的基準。
- 過去問以外も含む試験対策ポイント: 同じ旅行時間の不確実性でも、平均値モデル・分布モデル・区間モデル・複数シナリオモデルのどれを使うかをデータ状況から説明できるようにする。

### 5. 動的意思決定問題とMDPの構成要素 [最重要]

- 対応講義: Lecture 4, Lecture 5
- 関連する過去問: WS22/23 Aufgabe 6, WS22/23 Aufgabe 7, WS23/24 Aufgabe 8, SS24 Aufgabe 5a, WS24/25 Aufgabe 5a/b, SS25 Exercise 6, SS25 Exercise 7
- 何が問われたか: 動的意思決定プロセスの構成要素、MDPの要素、具体例における状態・決定・費用・後決定状態・外生情報・遷移・目的関数が繰り返し問われた。
- 理解すべきこと: MDPを $S_t, x_t, W_{t+1}, S_{t+1}, C_t/R_t, X_t(S_t)$ などの要素で説明する。抽象定義だけでなく、在庫・配送・ダム・ガス貯蔵に対応付ける。
- 過去問以外も含む試験対策ポイント: 新しいシナリオが出ても、決定時点、状態、決定、外生情報、遷移、目的関数の順に整理して答案を書く練習をする。

### 6. Bellman方程式、Value Function、ADPが必要になる理由 [最重要]

- 対応講義: Lecture 5, Lecture 6
- 関連する過去問: WS22/23 Aufgabe 8, SS24 Aufgabe 3a, SS24 Aufgabe 3c, WS24/25 Aufgabe 2
- 何が問われたか: Bellman方程式、最適政策とGreedy政策の比較、状態・遷移が増えたときにどこが計算不能になるか、動的計画法の後ろ向き再帰が問われた。
- Lecture 6で特に対応する箇所: Markov Decision Processの再掲、Decision Policy、Optimal Solution、Bellman Equation、Value Function、Curses of Dimensionality。Lecture 6では、期待将来報酬を post-decision state の value として捉え、厳密DPが実問題で困難になる理由からADPへ進む流れを押さえる。
- 理解すべきこと: Greedyは現在の報酬だけを見るが、Bellman最適は現在報酬と期待将来価値を同時に見る。Value Functionは「その状態から将来どれだけ良いか」を表す。Curse of dimensionalityは、状態空間・決定空間・情報空間が増えることで厳密な再帰計算が現実的でなくなること。
- 過去問以外も含む試験対策ポイント: Bellman方程式を丸暗記するだけでなく、$S_k$, $x$, $S_k^x$, $R(S_k,x)$, $V(S_k^x)$, $X_k^\pi(S_k)$ の意味を文章で説明できるようにする。新しい事例では、なぜ厳密最適化ではなく近似政策が必要になるのかを書けるようにする。


### 7. Policy classes / ADP method classes [最重要]

- 対応講義: Lecture 6, Lecture 7, Lecture 10
- 関連する過去問: WS22/23 Aufgabe 9, SS23 Aufgabe 2, SS25 Exercise 9
- 何が問われたか: Powellの政策クラス、ADP手法クラス、および各クラスの欠点が問われた。
- Lecture 6で特に対応する箇所: Approximate Dynamic Programmingの定義、Policy Function Approximation、Rolling Horizon Re-Optimization、Cost Function Approximation、Restaurant Meal Deliveryのケース。
- Lecture 7で特に対応する箇所: Policy Classesの整理、Multiple Scenario Approach、Consensus Function、Post-Decision State Rollout。
- 理解すべきこと: Policy Function Approximationは経験則を政策にする。Rolling Horizon Re-Optimizationは現在情報で再最適化するが近視眼的になりやすい。Cost Function Approximationは報酬や制約を調整して柔軟性を誘導する。Look-aheadは将来シナリオを明示的に見る。Value Function Approximationは将来価値を近似する。これらを「何を近似しているか」で区別する。
- 過去問以外も含む試験対策ポイント: 各手法について「何をする手法か」「強み」「弱み」「どの問題で使いやすいか」を1セットで覚える。未知の事例で、PFA/CFA/VFA/Look-aheadのどれを選ぶかを理由付きで説明できるようにする。


### 8. Rollout, Post-Decision Rollout, simulation horizon [重要]

- 対応講義: Lecture 7, Lecture 8
- 関連する過去問: WS22/23 Aufgabe 10, WS22/23 Aufgabe 12, SS23 Aufgabe 1, SS23 Aufgabe 4, WS24/25 Aufgabe 4
- 何が問われたか: Rollout/VFAで未来期間をどこまでシミュレーションするか、Post-Decision Rolloutの欠点が問われた。
- Lecture 7で特に対応する箇所: Look-ahead Methods、Multiple Scenario Approach、Post-Decision State Rollout。特に、サンプルされた将来情報を用いてMIPを解く方法、複数シナリオから代表解を選ぶ方法、post-decision stateから将来をロールアウトする方法の違いを押さえる。
- 理解すべきこと: 長期的な終端効果が重要な問題では全ホライズンが必要。一方、近い将来だけが現在決定に効く場合や計算負荷が大きい場合は短いホライズンが合理的。Post-Decision Rolloutでは、現在決定後の状態から将来政策をシミュレーションして、現在決定の良し悪しを評価する。
- 過去問以外も含む試験対策ポイント: 例として在庫・ダム・配送を使い分け、長期/短期ホライズンの理由を具体的に説明する。計算時間、将来情報の信頼性、終端効果、近視眼性の観点から比較できるようにする。


### 9. Value Function Approximationと特徴量設計 [最重要]

- 対応講義: Lecture 8, Lecture 9
- 関連する過去問: WS22/23 Aufgabe 11, SS24 Aufgabe 3b, SS24 Aufgabe 5b/c, SS23 Aufgabe 6g/h, WS24/25 Aufgabe 5c/d, SS25 Exercise 5
- 何が問われたか: 後決定状態の特徴量集約、VFAによる意思決定、VFAの結果、特徴選択と次元削減の違いが問われた。
- 理解すべきこと: VFAは全状態を厳密に保存せず、価値を特徴量ベースで近似する。重要なのは、将来価値を説明する特徴を選ぶこと。feature selectionは既存特徴の選択、dimensionality reductionは新しい低次元表現への変換。
- 過去問以外も含む試験対策ポイント: 具体問題ごとに有効な特徴量を提案し、その理由を言えるようにする。

### 10. Multiple Scenario ApproachとConsensus Function [重要]

- 対応講義: Lecture 7
- 関連する過去問: SS24 Aufgabe 4
- 何が問われたか: MSAの一般的な考え方と、Vehicle Routingで解の一致度を測るConsensus Functionが問われた。
- 理解すべきこと: 複数の将来シナリオを生成し、各シナリオに対する解を求め、その解の共通部分から現在の決定を選ぶ。VRPでは同じ顧客ペアが同じルートに入る、同じ次訪問先を選ぶ、同じ顧客集合を運ぶなどで一致を測れる。
- 過去問以外も含む試験対策ポイント: 単に定義を覚えるだけでなく、Consensusをどう測るかを問題構造に合わせて提案できるようにする。

### 11. 現実シナリオのMDP/VFA化: 在庫、ガス、ダム、配送、Food Delivery [最重要]

- 対応講義: Lecture 5, Lecture 8, Lecture 11
- 関連する過去問: SS23 Aufgabe 5, SS23 Aufgabe 6, WS23/24 Aufgabe 9, WS23/24 Aufgabe 10, SS24 Aufgabe 5, WS24/25 Aufgabe 5, SS25 Exercise 3, SS25 Exercise 6
- 何が問われたか: UNIPERガス貯蔵、Harzダム、パッケージ配送、レストラン配送など、現実問題をMDPやVFA/PFA/CFAとして設計する大問が繰り返し出た。
- 理解すべきこと: 新規シナリオを見たら、まず状態・決定・外生情報・遷移・費用/報酬・目的を切り分ける。次に、VFAなら将来価値を説明する特徴量、CFAなら現在費用に加える近似ペナルティ、PFAならルールを設計する。
- 過去問以外も含む試験対策ポイント: 過去問のシナリオを暗記するのではなく、未知のシナリオでも同じ設計手順で答えられるようにする。

### 12. Combined Methods [重要]

- 対応講義: Lecture 10
- 関連する過去問: SS25 Exercise 10
- 何が問われたか: ADP手法を2つずつ組み合わせ、期待される利点を説明する設問が出た。
- 理解すべきこと: 例: PFA + VFA, CFA + Lookahead, Rollout + VFAなど。組み合わせは、片方の弱点をもう片方が補う形で説明する。
- 過去問以外も含む試験対策ポイント: 5つのADPクラスを単体で理解したうえで、計算量、将来考慮、解釈可能性、学習可能性の観点から組み合わせを設計する。

## ノート作成時に各スライドへ書くべき過去問関連の例

```md
### 過去問との関連

- SS24 Aufgabe 1a と関連。
  - 関連点: Information Model, Decision Model, Aggregation, Disaggregationの機能説明が問われた。
  - 必要理解: 図の各要素を定義し、Real WorldからDecision Modelへ情報が流れ、実装によって現実へ戻るループを説明できること。

- WS23/24 Aufgabe 3 と関連。
  - 関連点: 同じ構造を配送車両のツアープランニングに適用する設問。
  - 必要理解: 抽象概念を具体例へ対応付けられること。
```

## 過去問にとらわれすぎないための一般方針

1. 定義問題だけでなく、未知の事例をMDPやADPとして設計する練習をする。
2. 旅行時間・配送・在庫・ダム・ガス貯蔵など、文脈が変わっても同じ構成要素で整理する。
3. 手法名だけでなく、どの情報を近似しているのか、どの弱点があるのかを説明する。
4. 数式は暗記ではなく、各記号が何を意味するかを説明できるようにする。
5. 過去問の大問では、問題文から状態・決定・外生情報・遷移・目的関数を抽出する力が重視されている。
