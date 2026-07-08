# Lecture 1-3 過去問ベース重要論点レビュー用メモ

この文書は、Lecture 1-3 のノート作成に際して、過去問で繰り返し問われた論点を抽出したレビュー用メモです。過去問は参考であり、試験対策では未知の事例へ適用できる理解を優先します。

## 1. Information Model / Decision Model / Aggregation / Implementation

- 主な対応箇所: Lecture 1 Slide 16-17, Lecture 2 Slide 4-9, Slide 42
- 関連過去問: SS24 Aufgabe 1a, WS23/24 Aufgabe 2, WS23/24 Aufgabe 3, WS22/23 Aufgabe 3
- 必要理解: Real-World -> Aggregation -> Information Model -> Decision Model -> Implementation -> Real-World のループを説明する。Information Modelは意思決定に使う情報表現、Decision Modelは決定空間・目的・制約・評価の定式化である。
- 過去問以外の対策: 配送以外の医師訪問、タクシー、food deliveryなどに同じ枠組みを当てはめる。

## 2. Business Analytics / OR / IDA / PMT の関係

- 主な対応箇所: Lecture 1 Slide 18-22, Lecture 2 Slide 5-8
- 関連過去問: WS22/23 Aufgabe 2-3, WS23/24 Aufgabe 1-3
- 必要理解: Business Analyticsは、データを分析するだけでなく、意思決定モデルを作り、解を現実に実装するプロセスである。ORはモデル化・最適化・解法で中心的役割を持つ。
- 過去問以外の対策: OR, Statistics, Computer Science/Information Systemsの役割を図なしでも文章で説明できるようにする。

## 3. 時間依存旅行時間とTSP/VRP

- 主な対応箇所: Lecture 2 Slide 11-13, 29-40
- 関連過去問: WS22/23 Aufgabe 1, WS22/23 Aufgabe 4, WS23/24 Aufgabe 4-5, SS25 Exercise 2
- 必要理解: 静的なtravel time matrixではなく、出発時刻に依存する \(d_{ij}(t)\) や \(\tau_{ij}(t)\) を用いる。時間依存性があると、挿入や経路選択により後続の到着時刻も変わる。
- 過去問以外の対策: 平均値モデル、時間帯別モデル、時間依存Dijkstra、ヒューリスティックの違いを一続きで説明する。

## 4. FIFO条件

- 主な対応箇所: Lecture 2 Slide 32
- 関連過去問: WS23/24 Aufgabe 4, SS25 Exercise 2
- 必要理解: 遅く出発した車両が早く到着するようなモデルは現実に反する。時間帯境界で旅行時間を急に切り替えるとFIFO違反が起こるため、ブレークポイントの平滑化などが必要になる。
- 過去問以外の対策: 小さな数値例を自分で作り、出発時刻と到着時刻の単調性を説明できるようにする。

## 5. Stochastic / Quasi-stochastic / Deterministic の区別

- 主な対応箇所: Lecture 3 Slide 9, 16-20, 24
- 関連過去問: WS22/23 Aufgabe 5, WS23/24 Aufgabe 7, WS24/25 Aufgabe 3
- 必要理解: stochasticは確率分布があり期待値・分散を扱える場合。quasi-stochasticは確率が不明で、シナリオや区間、最悪/最良ケースなどを使う場合。
- 過去問以外の対策: データ量が十分か、分布仮定が妥当か、解釈可能性が必要かという観点でモデルを選ぶ。

## 6. 確率分布・サンプリング・期待値分散

- 主な対応箇所: Lecture 3 Slide 10-15, 25-27, 34
- 関連過去問: WS23/24 Aufgabe 6, SS24 Aufgabe 2b, SS25 Exercise 4
- 必要理解: 確率変数、実現値、確率、期待値、分散、分布フィッティング、Monte Carlo samplingを説明する。\(x\) は決定、\(\xi\) は決定後に分かるランダム情報である。
- 過去問以外の対策: 期待値だけでなく分散やリスク姿勢が意思決定に影響する例を説明する。

## 7. Hurwicz基準とMinmax Regret

- 主な対応箇所: Lecture 3 Slide 28-29, 35-37
- 関連過去問: SS23 Aufgabe 3, WS24/25 Aufgabe 1, SS25 Exercise 8
- 必要理解: Hurwiczは最悪ケースと最良ケースを楽観係数で重み付けする。Minmax regretは各シナリオで完全情報の最良決定との差を後悔として測り、最大後悔を抑える。
- 過去問以外の対策: 旅行時間区間 \([l,u]\) を使い、平均・最悪・regretのどれを選ぶと何が起こるかを説明できるようにする。
