#!/usr/bin/env python
from __future__ import annotations

import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
MAT = ROOT / 'Materials' / '2026'
NOTES = ROOT / 'notes'
LATEX_SEC = ROOT / 'latex' / 'sections'
OUT_DOCS = ROOT / 'docs'

lectures = [
    {
        'id': '3dm_01_overview_ss26',
        'no': 1,
        'title': 'Overview',
        'pdf': '3DM_01_Overview_SS26.pdf',
        'md': '3dm_01_overview_ss26.md',
        'tex': 'l01_overview.tex',
    },
    {
        'id': '3dm_02_information_decision_modeling_ss26',
        'no': 2,
        'title': 'Information and Decision Modeling',
        'pdf': '3DM_02_Information-and-Decision-Modeling_SS26.pdf',
        'md': '3dm_02_information_decision_modeling_ss26.md',
        'tex': 'l02_information_decision_modeling.tex',
    },
    {
        'id': '3dm_03_uncertainty_ss26',
        'no': 3,
        'title': 'Uncertainty',
        'pdf': '3DM_03_Uncertainty_SS26.pdf',
        'md': '3dm_03_uncertainty_ss26.md',
        'tex': 'l03_uncertainty.tex',
    },
]

# Important exam references. These are based on the project question index.
EXAM = {
    'imdm_loop': 'SS24 Aufgabe 1a, WS23/24 Aufgabe 2, WS23/24 Aufgabe 3',
    'ba_process': 'WS22/23 Aufgabe 2-3, WS23/24 Aufgabe 1-3',
    'tsp_static': 'WS22/23 Aufgabe 1, WS23/24 Aufgabe 3',
    'time_dep_tt': 'WS22/23 Aufgabe 4, WS23/24 Aufgabe 4-5, SS25 Exercise 2',
    'info_complexity': 'SS24 Aufgabe 1b',
    'uncertainty_general': 'WS22/23 Aufgabe 5, SS24 Aufgabe 2a, WS24/25 Aufgabe 3',
    'distribution': 'WS23/24 Aufgabe 6, SS24 Aufgabe 2b, SS25 Exercise 4',
    'quasi': 'SS23 Aufgabe 3, WS23/24 Aufgabe 7, WS24/25 Aufgabe 1, WS24/25 Aufgabe 3',
    'hurwicz': 'SS25 Exercise 8, WS24/25 Aufgabe 3',
    'regret': 'SS23 Aufgabe 3, WS24/25 Aufgabe 1',
}

L1 = {
1: ('表紙。Data Driven Decision Making 第1回は、講義全体の目的と位置づけを確認する回である。', 'ここでは詳細理論より、以後の講義が「データに基づく動的な意思決定」を扱うことを把握する。', '用語として DDDM, stochasticity, dynamism が後続講義の軸になる。', '直接の計算問題ではないが、講義全体の入口。過去問では第1問で概念整理が問われやすい。', 'DDDM は単なるデータ分析ではなく何を決めるための講義か。'),
2: ('担当教員、TA、Decision Support オフィス、Webサイトの連絡先。試験日程もWebで確認する。', '事務情報。試験前に公式Webの試験日時・教室情報を確認する場所として重要。', '理論点ではない。メール前にWebを確認するという運用面を押さえる。', '過去問との直接関連は薄い。', '試験情報はどこで確認するか。'),
3: ('Decision Support 分野では、基礎科目から専門科目、演習、セミナー、修士論文へ進む。DDDMは専門科目側に位置づく。', 'DDDMは、Intelligent Data Analysisのようなデータ分析と、Planning系の意思決定モデルをつなぐ位置にある。', '講義の位置づけを理解し、データ分析だけでも最適化だけでもない点を意識する。', '過去問では直接ではなく、Business Analytics/Decision Supportの全体像を説明する設問の背景になる。', 'DDDMはどのような前提科目・分野とつながっているか。'),
4: ('講義名は以前のモビリティ情報システム系から変化し、情報システムの描写ではなく、情報システム内の自動意思決定へ焦点が移っている。Uber, Lime, Amazonのようなデジタルビジネスモデルとも関係する。', '中心は「情報を表示するシステム」ではなく「情報に基づいて決めるシステム」。PMTは意思決定、IDAはデータ分析に焦点を当て、DDDMはその接続を扱う。', 'データを持つだけでは不十分で、それを意思決定モデルに入れて実行可能な行動に変換する点を説明できること。', f'{EXAM["ba_process"]} と関連。Business Analytics/Decision Supportの構成要素を説明する際の導入になる。', '情報システムの depiction と automated decisions の違いを説明せよ。'),
5: ('目標は、確率性と動的性質の理解、確率的・動的意思決定問題のモデル化、方法論の強み・弱みの理解、デジタル経済の問題理解、試験合格、研究準備である。', '講義の本体は、stochasticity と dynamism を含む意思決定問題をどうモデル化し、どう解くかである。', '「確率的」と「動的」を定義できること。特に、確率性は情報が不確実であること、動的性は時間とともに状態や情報が変わり再意思決定が必要になること。', f'{EXAM["uncertainty_general"]} および後続のMDP/ADP問題と関連。', 'stochasticity と dynamism の違いを一文ずつ説明せよ。'),
6: ('全11回の構成。情報・意思決定モデル、確率性、動的性、MDP、ADP、Look-ahead、VFA、Combined Methods、Food Deliveryへ進む。', '講義は、まずモデル化、次に不確実性と動的性、最後に近似政策と応用へ進む。', '試験勉強では講義1-3を基礎、講義4-5を定式化、講義6以降を解法・近似手法として整理する。', '過去問は Lecture 2/3/5/7/8 に多く分散するため、スケジュールを論点索引として使う。', '講義全体を「モデル化」「不確実性」「動的性」「近似解法」に分類せよ。'),
7: ('主要文献は Warren Powell の研究と、TU Braunschweig の Ulmer らとの共同研究。交通・モビリティに合わせて発展している。', 'PowellはADP/Sequential Decision Analyticsの基礎として重要。Ulmerらの文献は車両ルーティングやprescriptive analyticsの応用に関係する。', '試験では文献名暗記より、なぜ交通・モビリティ問題がDDDMの例として適しているかを理解する。', '直接の出題対象というより、ADPやstochastic dynamic vehicle routingの背景。', '交通・モビリティ問題がDDDMで典型例になる理由は何か。'),
8: ('演習は専門Decision SupportのStudienleistungで、Trucks and Bargesという serious gaming application を使って意思決定状況を練習する。', '演習は理論を具体的な逐次意思決定として体験する場。複数日にわたる輸送モード選択は動的意思決定の直感を作る。', '理論ページではないが、意思決定、状態変化、将来情報の不確実性をゲームで観察する発想は重要。', '過去問との直接関連は薄いが、後のMDP/ADP問題で具体例を作る助けになる。', 'Trucks and Bargesでは何が「逐次的な意思決定」になっているか。'),
9: ('試験会場・時刻はDecision SupportのWebサイトで確認する。日程は早め、教室は直前に出る。', '事務ページ。情報がWebにある場合はメールで問い合わせない。', '試験準備として、教材だけでなく公式のPruefungenページを確認する。', '過去問との直接関連はない。', '試験教室はいつ頃確定するか。'),
10: ('過去問は印刷版またはWebで入手できる。ただし過去問演習だけでは十分ではなく、全講義内容が試験対象である。解答例は提供されない。', 'このプロジェクトでは過去問を「頻出論点の発見」に使い、出題範囲を狭める材料にはしない。', '過去問で聞かれた論点は強化するが、新しい事例に応用できる理解を優先する。', '全過去問関連。特に同じ概念が別事例で繰り返し出る傾向を意識する。', '過去問を使う目的と限界を説明せよ。'),
11: ('今回の本編アジェンダは、Motivation、Operations Research & Business Analyticsの復習、今後のモデリング概要である。', '第1回は理論の細部ではなく、なぜDDDMが必要なのかを流れとして示す。', 'Motivation -> OR/BA -> Modeling という順序を押さえる。', '過去問ではBAのプロセスや情報/意思決定モデルの説明につながる。', '第1回の3つの大項目を答えよ。'),
12: ('新しいビジネス概念は、より速く、個別化され、リアルタイム化している。即時配送、受注生産、予約スケジューリングなどが例。共通テーマはstochasticityとdynamismであり、確率的動的意思決定プロセスにつながる。', 'リアルタイム型サービスでは需要・交通・リソースが変わるため、事前計画だけでは不十分。新情報に応じて計画を更新する必要がある。', 'stochasticityは情報変化や不確実性、dynamismは情報変化に応じた計画更新。両者を合わせて stochastic dynamic decision processes になる。', f'{EXAM["uncertainty_general"]} と後のMDP構成要素問題の導入。', '即時配送を例に、何が確率的で何が動的か説明せよ。'),
13: ('交通の例として、same-day配送、ピックアップ、ドローン、食品配送などが示される。', 'これらは「どこへ、いつ、どの手段で行くか」を、変動する情報の下で決める問題である。', '具体例を見たら、需要、移動時間、リソース、制約、目的関数に分解する練習をする。', 'SS24 Aufgabe 2aの不確実性カテゴリや、後の配送MDP/VFA問題の具体例になる。', '交通例に含まれる不確実性を3つ挙げよ。'),
14: ('モビリティ・サービスの例として、自転車シェア、dial-a-ride、医師訪問、エレベーター保守、タクシー、救急などが挙げられる。', 'サービス業では顧客到着、サービス時間、移動時間、担当者の位置・可用性が変わる。', '配送以外のサービスでも同じモデル化フレームを適用できることを理解する。', 'SS24 Aufgabe 2aや将来の未知シナリオ型問題に対応する背景。', '医師訪問サービスを状態・決定・外生情報に分けると何か。'),
15: ('サービスプロセスは時間の中で進む。需要、リクエスト、交通、ドライバー、電池残量、要件などの新情報が入り、計画更新が必要になる。反応が遅すぎる場合があるため、期待される将来を予測し柔軟性を保つ必要がある。', 'DDDMの核心は、現在だけでなく「あとで起こりそうなこと」を考えて今の決定を選ぶこと。柔軟性は将来状態に対する備えである。', 'anticipation と flexibility を説明できること。近視眼的な決定がなぜ危険かを例示する。', '後のADP/Look-ahead/VFAの基礎。SS25 Exercise 9の手法欠点説明にもつながる。', 'なぜ現在最短の決定が将来悪い決定になりうるか。'),
16: ('意思決定ループ。現実世界で行動が実行され状態が観測される。Aggregationは現実データを情報モデルの次元に移す。Information Modelは情報を凝縮して表現する。Decision Modelは決定空間を定義し評価する。Implementationは解を現実の行動へ戻す。', 'Real-World -> Aggregation -> Information Model -> Decision Model -> Implementation -> Real-World の流れを説明できることが最重要。', 'AggregationとImplementationを混同しない。情報モデルは「何を知っているか」、決定モデルは「何を選び、どう評価するか」。', f'{EXAM["imdm_loop"]} と強く関連。SS24 Aufgabe 1aでは各機能の説明が問われた。', 'Aggregation, Information Model, Decision Model, Implementationをそれぞれ定義せよ。'),
17: ('DDDMでは情報モデルだけ、最適化モデルだけを個別に見るのではなく、現実世界を含むループ全体を扱う。時間とともにシステムをモデル化する必要があり、それがdynamicである。外部効果により現実が変化するためstochasticである。実装された決定がすでに変化した現実と衝突する可能性もある。', 'Lecture 1の最重要ページ。DDDMが従来の静的ORや単なるデータ分析から広がる点を示す。', '動的意思決定では、一度計画して終わりではなく、観測・更新・再計画のループを前提にする。', f'{EXAM["imdm_loop"]}、WS22/23 Aufgabe 3と関連。後のLecture 4/5のMDP定式化につながる。', 'なぜDDDMでは現実世界をループに含める必要があるか。'),
18: ('アジェンダの2番目、Operations Research & Business Analyticsの復習へ移る。', 'ここからTSP例を使って、現実問題を情報モデル・決定モデルへ変換する流れを確認する。', 'BA/ORの復習は過去問で頻出。図や用語を答案化できるようにする。', f'{EXAM["ba_process"]} と関連。', 'ORはBAプロセスのどこで重要になるか。'),
19: ('ブラウンシュヴァイクの荷物配送例。車両、デポ、顧客住所、時間、道路ネットワークがあり、配送順序を決める問題である。', '現実問題をTSPに単純化する入り口。全ての現実情報を使うのではなく、意思決定に必要な情報だけを抽象化する。', '顧客、デポ、移動時間、ツアー順序、目的関数を識別する。', f'{EXAM["tsp_static"]} と関連。WS23/24 Aufgabe 3では配送計画へのBA適用が問われた。', 'この例で情報モデルと決定モデルに入るものを分けよ。'),
20: ('TSPモデル化。道路ネットワークを顧客間アークへ、速度を移動時間へ変換し、重み付きグラフまたは移動時間行列を作る。その上で全顧客を訪問し総移動時間を最小化する。', '情報モデルはtravel time matrix、決定モデルはTSPの目的関数・制約・決定変数である。', '現実の道路から行列へ変換する過程を説明する。TSPの基本制約、全顧客訪問、サブツアー排除を押さえる。', f'{EXAM["tsp_static"]} と関連。WS22/23 Aufgabe 1ではTSPモデル化が問われた。', 'TSPでtravel time matrixは情報モデルか決定モデルか。'),
21: ('モデルは解空間を張り、解を評価する。解は最適化やヒューリスティックで得られ、結果を実行する必要がある。', 'モデルを作るだけでなく、解を探索し現実へ戻すまでがOR/BAプロセス。', 'solution space, evaluation, optimization/heuristics, implementationの関係を説明する。', f'{EXAM["ba_process"]} と関連。', 'モデルがsolution spaceを定義するとはどういう意味か。'),
22: ('Operations Researchの三段階は、Problem definition、Modeling、Solution。情報と意思決定を扱い、さらにImplementationが重要になる。', 'ORは現実問題を数理モデルにし、解くための方法論。DDDMではこれにデータ取得・実装・更新が加わる。', 'Problem definition, modeling, solution, implementationの順序を答案に書けるようにする。', f'{EXAM["ba_process"]} と関連。WS22/23 Aufgabe 3でBA適用プロセスとORの位置づけが問われた。', 'ORの三段階を配送例に対応させよ。'),
23: ('アジェンダの3番目、Modeling and Outline of the Lecturesへ移る。', 'ここから、同じ現実問題でも情報モデルや決定モデルを変えると見える問題が変わることを示す。', '静的平均モデルから時間依存・不確実・動的モデルへ拡張される流れを押さえる。', 'Lecture 2/3/4への橋渡し。', 'TSPの情報モデルをより現実的にすると何が増えるか。'),
24: ('異なる現実問題でも同じモデルを共有できる一方、情報モデルの精度が十分か、決定モデルが適切かを検討する必要がある。', 'モデル化は一度決めて終わりではない。観測される現象に応じて情報モデル・決定モデルを修正する。', '同じTSP/VRP構造が配送・技術者訪問などに使えること、ただしデータと目的に合わせた拡張が必要なこと。', f'{EXAM["info_complexity"]} と関連。詳細モデルを常に選ばない理由も説明できるようにする。', '同じ決定モデルを別の現実問題に使うときの注意点は何か。'),
25: ('代替情報モデルの例。旅行時間には日内変動があり、7-9時、9-15時など時間帯別に移動時間を考える必要がある。', '静的な平均旅行時間行列では、ピーク時間や道路ごとの速度差を表せない。時間依存travel time matrixが必要になる。', '時間依存旅行時間はLecture 2の中心。平均値モデルとの違い、データ集約、FIFO条件へつながる。', f'{EXAM["time_dep_tt"]}, {EXAM["info_complexity"]} と関連。', '平均旅行時間行列と時間帯別旅行時間行列の違いは何か。'),
26: ('代替決定モデルの例。解は実行可能に見えても、旅行時間の不確実性により残業が発生することがある。', '情報モデルが「不確実性」を持つなら、決定モデルも期待値・分散・ロバスト性などを考える必要がある。', '不確実性は目的関数だけでなく制約の満たし方にも影響する。', f'{EXAM["uncertainty_general"]}, SS24 Aufgabe 1b と関連。Lecture 3への導入。', '旅行時間が不確実なとき、決定モデル側で何を変える必要があるか。'),
27: ('動的性の例。情報モデルが時間とともに変わり、変化に反応できる。これがLecture 4のテーマである。', '動的問題では、事前計画だけでなく、途中で観測した情報に基づいて再意思決定する。', 'reactive planning と anticipatory planning の違いを意識する。', 'Lecture 4/5のMDP問題への導入。WS23/24 Aufgabe 8などに関係。', '情報モデルが時間とともに変わるとは具体的に何か。'),
28: ('今後はBusiness Analytics、情報・意思決定モデル、不確実性、動的性へ進む。', '第1回は後続講義の地図である。試験対策では、概念を後の数式・事例に接続することが重要。', 'Lecture 1は用語の出発点。以後、Lecture 2で情報/決定モデル、Lecture 3で不確実性を具体化する。', '過去問の多くはLecture 1の概念を具体例へ適用させる形で出る。', '第1回の内容がLecture 2/3/4へどうつながるか説明せよ。'),
}

L2 = {
1: ('表紙。第2回はInformation Modeling and Decision Modelingを扱う。', '第1回の意思決定ループを具体化し、現実データをどのような情報モデルにし、どのような決定モデルで解くかを学ぶ。', 'Lecture 2は過去問頻出。特にBAプロセス、時間依存旅行時間、FIFO、ヒューリスティックが重要。', f'{EXAM["imdm_loop"]}, {EXAM["time_dep_tt"]} と広く関連。', '情報モデルと決定モデルの違いを一文で説明せよ。'),
2: ('本日の目標は、Business Analyticsのプロセス、情報・意思決定モデル、時間依存旅行時間付きTSP、TSP解法を理解すること。', '講義前半は概念、後半は移動時間データを使ったケーススタディ。', 'データ収集から意思決定までの流れを、TSP例で具体化できるようにする。', f'{EXAM["ba_process"]}, {EXAM["time_dep_tt"]} と関連。', '今日の講義の中心的なケーススタディは何か。'),
3: ('アジェンダは、Information/Decision Modelingと、時間依存旅行時間付きTSPのケーススタディ。', '抽象フレームを先に学び、その後で都市交通データへの適用を見る。', '試験では定義だけでなく、ケースへ対応付ける力が問われる。', f'{EXAM["ba_process"]}, WS23/24 Aufgabe 3 と関連。', '抽象モデルとケーススタディの関係を説明せよ。'),
4: L1[16],
5: ('情報モデルと決定モデルは初期仮説に基づいて設計される。仮説は現実問題の観察やデータから生まれ、分析結果により仮説が確認・修正される。', 'モデル化は固定的なものではなく、descriptive analyticsで現実を観察し、prescriptive analyticsで意思決定へつなぐ反復プロセスである。', '情報モデルの選択は仮説依存。例えば「旅行時間は一定」という仮説が崩れれば時間依存モデルへ変える。', f'{EXAM["ba_process"]}, {EXAM["info_complexity"]} と関連。', '観測データが初期仮説を否定した場合、モデル化では何をするか。'),
6: ('タスク、問題構造、記録データ、探索、対象データの関係を示す図。', '現実問題の構造を理解し、記録されたデータから意思決定に必要なデータを探す流れを表す。', 'データはそのまま意思決定に使えるとは限らず、構造理解と抽出・変換が必要。', f'{EXAM["ba_process"]} と関連。BAプロセス図の説明に使える。', 'recorded data と target data の違いは何か。'),
7: ('現実の意思決定問題は数理モデル化に合わせて単純化される。単純化の過程で情報の構造と外見を切り分ける。', 'Meisel/Mattfeldの視点では、ORとData Mining/IDAは現実問題の構造化とデータ活用で相補的に働く。', 'どの情報を残し、どの情報を捨てるかが情報モデル設計の中心。', f'{EXAM["ba_process"]}, WS23/24 Aufgabe 1 と関連。', '数理モデル化のために現実問題を単純化する利点と危険は何か。'),
8: ('IDAとPMTの統一ビュー。goal, problem, structure, search, decision という流れで、データ分析と意思決定を接続する。', 'IDAはデータからパターンや構造を抽出し、PMT/ORはそれを使って意思決定をモデル化・解決する。', 'Business Analyticsを「データ分析」「統計」「OR/意思決定」の接続として説明できるようにする。', f'{EXAM["ba_process"]} と強く関連。WS22/23 Aufgabe 2, WS23/24 Aufgabe 1でBA分野が問われた。', 'IDAとPMTはBusiness Analyticsの中でどう接続するか。'),
9: ('TSP例。仮説は旅行時間が一定であること。情報モデルは旅行時間行列、決定モデルはTSP。出力は顧客訪問順序である。', 'このページは情報モデルと決定モデルの最小例。後に時間依存・不確実性・動的性を加える基準点になる。', 'travel time matrixとTSPモデルを区別する。仮説が変わると情報モデルも決定モデルも変わる可能性がある。', f'{EXAM["tsp_static"]}, SS24 Aufgabe 1b と関連。', 'TSP例で、仮説・情報モデル・決定モデル・出力を対応させよ。'),
10: ('ケーススタディへ移る。対象は時間依存旅行時間をもつTSPである。', '静的TSPから、出発時刻により移動時間が変わるTSPへ拡張する。', '時間依存性があると、移動コストはアークだけでなく出発時刻にも依存する。', f'{EXAM["time_dep_tt"]} と関連。', '時間依存TSPではコスト関数は何に依存するか。'),
11: ('サービスルーティングでは高価な運転時間を節約し、顧客サービスを改善し、資源を効率的に使うことが重要である。', '交通・配送では少しの移動時間改善がコストやサービス品質へ大きく影響する。', '目的関数は総移動時間だけでなく、遅延・サービス品質・資源利用も関係しうる。', f'{EXAM["tsp_static"]}, SS24 Aufgabe 1b と関連。', 'サービスルーティングで移動時間が重要な理由を説明せよ。'),
12: ('旅行時間は時間と空間で変動する。道路セグメントごとに異なる旅行時間があり、天候、事故、曜日、時間帯などで変わる。', '時間依存旅行時間の情報モデルは、単なる顧客間距離ではなく、道路セグメント・時間帯・速度/移動時間を含む。', '時間変動と空間変動を分けて説明する。', f'{EXAM["time_dep_tt"]} と関連。', '旅行時間が時間と空間で変動するとはどういう意味か。'),
13: ('情報モデルは、顧客間の時間依存旅行時間、時間依存旅行時間行列または複数行列。決定モデルは旅行時間最小化、全顧客訪問、ルーティング制約、時刻に依存する顧客間移動決定変数を含む。', '時間依存性を入れると、同じiからjへの移動でも出発時刻でコストが変わる。', '情報モデルと決定モデルの要素を答案で列挙できること。', f'{EXAM["time_dep_tt"]}, WS22/23 Aufgabe 1 と関連。', '時間依存旅行時間TSPの情報モデルと決定モデルを分けて書け。'),
14: ('Floating Car Dataは、時間・道路セグメントごとの旅行時間を得るデータである。十分なデータ量が必要で、オンデマンド型の情報として活用される。', 'FCDはタクシーや車両から得られる移動観測データ。生データから速度・リンク・時間帯を推定して情報モデルを作る。', 'データ収集 -> クリーニング -> 集約 -> 一般化という流れを説明する。', f'WS22/23 Aufgabe 4 と関連。過去交通観測から時間帯別平均旅行時間を作る手順が問われた。', 'FCDから旅行時間行列を作るにはどの処理が必要か。'),
15: ('FCDの収集と利用には、タクシーフリート、ディスパッチャ、公共交通管理、プロバイダ、インターネットなどが関係する。', 'データは複数主体を通じて集まる。データの粒度や欠損は後のモデル品質に影響する。', '誰がデータを持ち、どの形で意思決定に使えるかを考える。', 'WS22/23 Aufgabe 4のデータ取得手順の背景。', 'FCDのデータ提供者と利用者を挙げよ。'),
16: ('タクシーデータはそのまま道路、方向、速度を与えないため、必要な手順としてデータの位置合わせ、リンクへの割付、方向判定、速度計算が必要である。', '生GPSデータは情報モデルではない。地図マッチングと速度推定を通じて道路セグメント別データになる。', '生データと意思決定用データの違いを説明する。', f'WS22/23 Aufgabe 4 と関連。観測値から旅行時間を作る手順。', 'Taxi GPSデータをなぜそのまま旅行時間行列にできないか。'),
17: ('リンク、時刻、速度の表。観測データを道路リンク単位・時間単位に整理している。', 'この表はAggregationの中間成果。個別車両の観測をリンク別速度へ変換する。', '列の意味を理解し、後の時間帯別平均やクラスターに接続する。', f'WS22/23 Aufgabe 4 と関連。', 'link, time, speed は情報モデルのどの段階か。'),
18: ('速度パターンは日内で変わり、同じ日・同じ時刻でも変動がある。仮説が確認される一方で、ばらつきも存在する。', '平均だけでなくばらつきがあるため、Lecture 3の不確実性へつながる。', '日内変動と確率的ばらつきを区別する。', f'{EXAM["time_dep_tt"]}, {EXAM["uncertainty_general"]} と関連。', '同じ時間帯でも速度がばらつく場合、どの講義テーマにつながるか。'),
19: ('速度、最大速度、混雑率などを持つデータ。道路リンクごとの交通品質を算出できる。', '最大速度に対する実際の速度比などを使い、セグメント間で比較可能な指標にする。', '正規化や交通品質指標の意味を理解する。', 'WS22/23 Aufgabe 4の集約・平均化手順に関連。', 'maxspeedを使うと何を比較しやすくなるか。'),
20: ('観測数が少ない道路と多い道路がある。空間分布を可視化し、データの偏りを確認する。', 'データ量が少ない場所では推定値が不安定。モデル化には補完や一般化が必要になる。', 'データ量の偏りが情報モデルの信頼性へ影響することを説明する。', f'{EXAM["info_complexity"]}, {EXAM["distribution"]} と関連。', '観測数が少ないリンクをそのまま使う危険は何か。'),
21: ('リンクID、時刻、速度などからなるデータ例。個別観測を集約対象として整理している。', 'このページも、現実データを情報モデルへ入れる前のデータ構造を示す。', 'データ項目が後の集約単位になることを押さえる。', 'WS22/23 Aufgabe 4に関連。', 'この表から時間帯別旅行時間を作るには何を集約するか。'),
22: ('一般化。集約結果は膨大な値になり、一部は少数観測に基づく。そこで類似パターンを使って一般化する必要がある。', '情報モデルは詳細すぎると扱いにくく、観測不足にも弱い。一般化で安定性と扱いやすさを得る。', '詳細性と安定性のトレードオフを説明する。', f'{EXAM["info_complexity"]}, SS24 Aufgabe 1b と関連。', 'なぜ全リンク・全時間帯をそのまま詳細に使うだけでは不十分か。'),
23: ('正規化。道路によって絶対速度は異なるが、日内変動パターンは似ている場合がある。制限速度30/50などの差をならす。', '正規化により、絶対値ではなく相対的な交通品質パターンを比較できる。', 'クラスタリング前処理としての正規化の役割を理解する。', 'WS22/23 Aufgabe 4とSS24 Aufgabe 1bに関連。', '正規化すると何が比較可能になるか。'),
24: ('クラスタリング。類似する日内交通変化をグループ化し、6クラスターにまとめる。0は悪い交通品質で長い旅行時間、1は良い交通品質で短い旅行時間を表す。', 'クラスタリングは一般化の方法。道路ごとに個別モデルを作らず、似たパターンを共有する。', 'クラスタリングの目的は次元削減・補完・解釈可能な情報モデル化。', f'WS22/23 Aufgabe 4, SS24 Aufgabe 1b と関連。後のfeature/dimensionality reductionの背景にもなる。', '交通パターンをクラスタ化する利点を2つ挙げよ。'),
25: ('空間的検証。クラスターはピーク挙動が異なり、中心部、商業地域、高速道路など異なる道路タイプを表す。', 'クラスタが単なる数学的分類ではなく、実際の道路タイプと対応しているか検証する。', 'モデルの妥当性確認では、結果が現実解釈可能かを確認する。', 'BAプロセスのvalidationとして重要。', 'クラスタリング結果を空間的に検証する目的は何か。'),
26: ('時間的検証。1日の交通品質がAからFの水準で変わる様子を確認する。', '時間帯による混雑変化が情報モデルに反映されているかを見る。', 'ピーク時間と非ピーク時間の違いをモデルが捉える必要がある。', f'{EXAM["time_dep_tt"]} と関連。', '時間的検証で確認すべきことは何か。'),
27: ('月曜3-4時は90%のセグメントがfree trafficである。', '深夜の交通状態は良好で、時間依存モデルでは短い旅行時間が期待される。', '同じ道路でも時間帯により旅行時間が変わる例として使う。', f'{EXAM["time_dep_tt"]} と関連。', 'このスライドは時間依存性のどの側面を示しているか。'),
28: ('月曜17-18時は30%が混雑しており、ラッシュアワーを示す。', 'ピーク時間には旅行時間が増え、最短経路や最適ツアーが変わりうる。', '出発時刻によってコストが変わるため、静的TSPでは不十分。', f'{EXAM["time_dep_tt"]} と関連。', 'ラッシュアワーがTSP解に与える影響を説明せよ。'),
29: ('情報モデルの結論。道路セグメント・各時間について旅行時間行列を持つ。時間帯により長い/短い旅行時間が現れる。次はこの情報でどうルーティングするかが問題になる。', 'データ分析の結果は、決定モデルで使える形の時間依存travel time matrixになる。', '情報モデルを作った後、決定モデルへ接続する必要がある。', f'WS22/23 Aufgabe 4, WS23/24 Aufgabe 4-5 と関連。', '時間依存旅行時間行列を作った後、決定モデル側で何が変わるか。'),
30: ('顧客間には複数経路があり、最短経路はDijkstraで計算される。時間依存性を考慮するには、time-dependent shortest pathsが必要。', '顧客間の直接移動時間は道路セグメントの組み合わせから作られる。時間によって最短経路自体が変わりうる。', 'セグメントレベルから顧客間パスへのAggregationを理解する。', f'{EXAM["time_dep_tt"]} と関連。', '通常のDijkstraと時間依存Dijkstraの違いは何か。'),
31: ('出発時刻が違うと、選ぶ道路セグメントも変わる可能性がある。time-dependent Dijkstraはこれを考慮する。', '最短経路は固定ではなく、出発時刻tの関数になる。', '旅行時間関数 \\(\\tau_{ij}(t)\\) の直感を説明できるようにする。', f'{EXAM["time_dep_tt"]} と関連。', 'なぜ出発時刻が違うと最短経路も変わりうるか。'),
32: ('行列の不連続な切替は奇妙な遷移を生む。FIFO条件により、遅く出発した車が早く到着して追い越すことを避ける必要がある。ブレークポイントを線形結合で平滑化する。', 'Lecture 2の最重要ページ。時間帯境界で旅行時間を急に変えると、物理的に不合理な到着時刻が出る。FIFOは時間依存経路問題の整合性条件。', 'FIFO: 出発時刻が遅いなら到着時刻も遅いか同じであるべき。違反例と補正方法を説明できること。', f'{EXAM["time_dep_tt"]} と非常に強く関連。WS23/24 Aufgabe 4, SS25 Exercise 2で問われた。', 'FIFO条件を言葉と小さな数値例で説明せよ。'),
33: ('時間依存TSPの再整理。情報モデルは時間依存旅行時間行列、決定モデルは旅行時間最小化、全顧客訪問、ルーティング制約、時刻付き移動決定変数を含む。', '情報モデルと決定モデルをまとめて答案化するためのページ。', '変数が「iからjへ行く」だけでなく「いつ行くか」を含む点が重要。', f'WS22/23 Aufgabe 1, WS23/24 Aufgabe 5 と関連。', '時間依存決定変数にはどの情報が含まれるか。'),
34: ('時間依存決定変数の例。各アークの移動時間が時間帯ごとに異なる。', '同じA-Bでも時間帯で値が異なるため、経路選択と出発時刻が相互に影響する。', '静的な \\(d_{ij}\\) ではなく、時間帯付きの \\(d_{ij}(t)\\) として考える。', f'{EXAM["time_dep_tt"]} と関連。', '静的な距離行列と時間依存距離行列の違いを説明せよ。'),
35: ('時間依存決定変数の拡張例。複数ノード・複数時間帯のネットワークで、到着時刻に応じて次の選択肢が変わる。', '時間を含めたネットワークでは、同じ場所でも時点が違えば別状態として扱うことに近い。', '動的/時空間ネットワークの直感をつかむ。', '後のMDPや動的意思決定の理解にもつながる。', '同じノードAでも時刻が違うと何が変わるか。'),
36: ('最適計算は難しく、ヒューリスティックが必要。LANTIME、Nearest Neighbor、Cheapest Insertion、Savings、平均値TSPなどを比較する。', '時間依存TSPは計算が難しいため、近似・ヒューリスティックを使う。', '各ヒューリスティックの発想と限界を説明できるようにする。', f'WS23/24 Aufgabe 5, SS25 Exercise 2 と関連。', 'なぜ時間依存TSPではヒューリスティックが必要になるか。'),
37: ('Nearest Neighborは現在位置から最も近い顧客を選ぶ。時間依存性に対応できるが、最後に長い移動が残りやすい。', '貪欲法の典型。局所的に良い選択が全体最適とは限らない。', '近視眼的 heuristic の利点と欠点を説明する。', 'WS23/24 Aufgabe 5のCheapest Insertion問題と同じく、局所基準の限界に関係。', 'Nearest Neighborが最後に悪い移動を残しやすい理由は何か。'),
38: ('Cheapest Insertionは空ツアーから始め、最も安い顧客を順に挿入する。ただし時間依存では、顧客がずれることで過去の決定が無効になり、旅行時間が変わる。', '過去問頻出。静的TSPでは挿入コストが比較的安定するが、時間依存では挿入により到着時刻が変わり、後続アークのコストも変わる。', '「局所的に安い挿入」が「全体で安い」とは限らない理由を説明できること。', f'WS23/24 Aufgabe 5 と強く関連。', '時間依存旅行時間でCheapest Insertionが難しい理由を説明せよ。'),
39: ('Savingsは直接配送ツアーから始め、最小コストでツアーを結合する。時間依存性は評価しにくいが、後のステップである程度暗黙に考慮される。', 'Savingsも静的VRPでよく使われるが、時間依存では結合による時刻変化が評価を難しくする。', 'Nearest Neighbor, Cheapest Insertion, Savingsの違いと限界を比較する。', '時間依存TSP/VRPのヒューリスティック比較として重要。', 'Savingsの基本発想と時間依存での難しさを説明せよ。'),
40: ('結果。出発時刻によって旅行時間が変わり、静的モデルは過大評価・過小評価を起こす。', '時間依存モデルを使う理由を実証的に示すページ。平均値TSPではピーク/オフピークの違いを捉えられない。', '結果グラフを読むときは、出発時刻、曜日、手法、旅行時間の関係を説明する。', f'{EXAM["time_dep_tt"]}, SS24 Aufgabe 1b と関連。', '静的モデルが過大・過小評価するとはどういう意味か。'),
41: ('実装例。月曜正午出発では、最初に中心部を避け郊外を先に回る。', '時間依存モデルは単に移動時間を変えるだけでなく、訪問順序・ルート形状を変える。', '意思決定結果が現実行動へImplementationされる点を理解する。', f'{EXAM["imdm_loop"]}, WS23/24 Aufgabe 3 と関連。', 'なぜ正午出発では中心部を避ける戦略が合理的か。'),
42: ('まとめ。問題とデータを真剣に扱うには多くの作業が必要。情報モデルではデータ収集・分析・構造化・集約・一般化、決定モデルでは目的・制約・変数・解法が必要になる。', 'Lecture 2全体の総括。現実データから意思決定までの工程を通しで説明できるようにする。', '情報モデル作成と決定モデル作成の作業項目を分けて列挙できること。', f'{EXAM["ba_process"]}, {EXAM["time_dep_tt"]} と関連。', '情報モデル構築に必要な作業を5つ挙げよ。'),
43: ('次回は不確実性と、それが情報モデル・決定モデルへ与える影響を扱う。', '時間依存性だけでは、同じ時間帯内のばらつきや予測不可能な変動は扱いきれない。', 'Lecture 3ではdeterministic, stochastic, quasi-stochasticの違いを学ぶ。', f'{EXAM["uncertainty_general"]} と関連。', '時間依存性と不確実性の違いを説明せよ。'),
}

L3 = {
1: ('表紙。第3回はUncertaintyを扱う。', '第2回の時間依存旅行時間に加え、観測値のばらつき・確率分布・シナリオ・ロバスト性を学ぶ。', '過去問ではLecture 3は非常に頻出。stochastic/quasi-stochastic, distribution, Hurwicz, regretを重点化する。', f'{EXAM["uncertainty_general"]}, {EXAM["quasi"]} と関連。', '不確実性は情報モデルと決定モデルのどちらに影響するか。'),
2: ('前回の復習としてBusiness Analytics全体、情報・意思決定モデル、時間依存旅行時間を確認し、今回は不確実性へ進む。', 'Lecture 2の時間依存性は「規則的な変化」、Lecture 3は「不確実なばらつき」の扱いへ進む。', '時間依存モデルと不確実性モデルを区別する。', f'{EXAM["time_dep_tt"]}, {EXAM["uncertainty_general"]} と関連。', '時間依存と不確実性は同じか、違うか。'),
3: ('アジェンダは、不確実性、Uncertaintyのモデリング、不確実性下の意思決定、都市物流のロバストVRPケーススタディ。', 'Lecture 3は「不確実性をどう表すか」と「それを使ってどう決めるか」の二段構成。', 'Modeling uncertainty と decision making under uncertainty を区別する。', f'{EXAM["uncertainty_general"]} と関連。', '不確実性のモデリングと不確実性下の意思決定の違いは何か。'),
4: ('不確実性の例として、株式市場、需要、交通などがある。', '不確実性とは、決定時点では未来の情報が完全には分からないこと。', '何が不確実かを、需要、移動時間、サービス時間、リソースなどに分類する。', f'SS24 Aufgabe 2a, {EXAM["uncertainty_general"]} と関連。', '同じ配送問題で不確実な要素を3つ挙げよ。'),
5: ('モビリティ・物流では、顧客リクエスト、需要量、サービス時間、可用性、行動、ドライバー、車両、交通、天候など多くの不確実性がある。', '不確実性は顧客側、リソース側、環境側に分けると答案を書きやすい。', 'カテゴリ別に具体例を挙げる能力が重要。', f'SS24 Aufgabe 2a と強く関連。Same-Day配送の不確実性カテゴリが問われた。', '顧客・リソース・環境の不確実性を各1つ挙げよ。'),
6: ('旅行時間の不確実性。天候、事故、道路工事、交通量などが影響し、連続的・予測可能/不可能な変化を含む。', '旅行時間は時間帯で変わるだけでなく、同じ時間帯でも確率的にばらつく。', '時間依存性と確率分布/シナリオの組み合わせとして理解する。', f'{EXAM["distribution"]}, {EXAM["quasi"]} と関連。', '旅行時間の不確実性を確率分布で表せる場合と表せない場合の違いは何か。'),
7: ('不確実性の結果として、活動のキャンセル、配送失敗、職場アクセス不能、遅延、追加コストなどが生じる。', '不確実性は単なるデータ誤差ではなく、制約違反やサービス品質低下につながる。', '目的関数だけでなく制約の実行可能性にも影響することを理解する。', f'SS24 Aufgabe 2a/b, {EXAM["uncertainty_general"]} と関連。', '不確実性が制約に影響する例を挙げよ。'),
8: ('アジェンダ。次は不確実性のモデリングへ進む。', 'ここから deterministic, stochastic, quasi-stochastic の区別を学ぶ。', '講義3で最も重要な分類が始まる。', f'WS24/25 Aufgabe 3 と関連。', '3つの不確実性モデル分類を予想して書け。'),
9: ('不確実性モデルの選択は情報レベルに依存する。Deterministicは全情報が既知。Stochasticは実現値の確率が既知。Quasi-stochasticは確率は不明だが有限シナリオなどで考える。', 'Lecture 3の中心分類。データ量・分布の有無・確率の信頼性によりモデルを選ぶ。', 'deterministic/stochastic/quasi-stochasticを定義し、どの状況で使うか説明する。', f'{EXAM["uncertainty_general"]}, {EXAM["quasi"]} と強く関連。WS24/25 Aufgabe 3で問われた。', 'stochastic と quasi-stochastic の違いを説明せよ。'),
10: ('基礎。確率分布は離散または連続。確率変数Xの実現値と確率があり、期待値は \\(\\mu=E[X]=\\sum_i p_i x_i\\) で表される。', '確率的モデリングでは、ばらつきを確率変数として扱い、期待値・分散などで評価する。', '期待値、分散、離散/連続分布、実現値、確率を説明できること。', f'{EXAM["distribution"]} と関連。', '期待値 \\(E[X]\\) は何を意味するか。'),
11: ('確率分布の決定。理論分布を仮定しパラメータを設定する方法、または既存データに分布をフィットする方法がある。例は一様分布、正規分布、指数分布。', '分布選択はデータと現象に依存する。サービス時間や到着間隔では非負・右裾の分布が自然な場合が多い。', 'どの分布が適切か、パラメータをどう決めるかを説明する。', f'{EXAM["distribution"]}, SS25 Exercise 4 と関連。', '理論分布を仮定する方法とデータにフィットする方法の違いは何か。'),
12: ('理論的な確率密度関数の例。分布によって形状、裾、対称性、非負制約が異なる。', 'PDFの形から、現象に合うかを判断する。サービス時間や旅行時間は非負で右裾を持つことが多い。', '分布の形状を解釈できること。', 'SS24 Aufgabe 2b と関連。サービス時間分布の典型的性質が問われた。', 'サービス時間PDFが負の値を持つのは自然か。'),
13: ('都市旅行時間分布の例。1つの道路区間の旅行時間観測を頻度として可視化している。', '観測ヒストグラムから分布形を見て、確率モデルを選ぶ。', 'ヒストグラム、頻度、旅行時間のばらつきを読み取る。', f'{EXAM["distribution"]} と関連。', 'ヒストグラムから何を見て分布候補を判断するか。'),
14: ('分布フィッティングにはPythonライブラリやEasyFitなどのソフトウェアが使える。', '確率モデルは手計算だけでなく、データに対して推定・検証する。', 'ツール名より、フィッティングの目的を理解する。', 'WS23/24 Aufgabe 6の観測値から分布を近似する問題に関連。', '分布フィッティングの目的は何か。'),
15: ('都市旅行時間分布の例2。観測頻度と推定密度を比較し、分布がデータに合うかを見る。', 'フィットした分布を意思決定モデルで使うには、現実のばらつきを十分表している必要がある。', '分布の適合度と過度な単純化の危険を理解する。', f'{EXAM["distribution"]} と関連。', '分布が観測データに合わない場合、意思決定にどんな問題が起こるか。'),
16: ('確率的モデリングの問題点。データが得られない、記録不足、システム変化、道路工事、新しい概念などにより、確率分布を信頼して推定できない場合がある。', 'ここでquasi-stochasticへつながる。確率が分からないときは、シナリオや区間、ロバスト基準を使う。', 'なぜ確率分布を常に使えるわけではないかを説明できること。', f'WS23/24 Aufgabe 7, {EXAM["quasi"]} と強く関連。', '確率分布を近似できない条件を3つ挙げよ。'),
17: ('準確率的モデリング。複数のシナリオを作り、有限個の可能な実現値としてWhat-If分析を行う。', '確率が不明でも、最良・最悪・中間などのシナリオで意思決定の頑健性を評価できる。', 'quasi-stochastic = probability unknown but scenarios/intervals known と覚える。', f'{EXAM["quasi"]} と関連。', 'quasi-stochastic modelingでは確率を使うか。'),
18: ('データからシナリオを作る例。月曜16-17時のHildesheimer Strasseの旅行時間観測20個を用いる。', '限られた観測から、可能な旅行時間ケースを構成する。', '観測値からシナリオを作る手順を説明する。', f'WS24/25 Aufgabe 1, SS23 Aufgabe 3 と関連。', '20個の観測から5シナリオを作るならどう選ぶか。'),
19: ('シナリオ構築方法。シナリオ数を決める、極端シナリオを選ぶ、間のシナリオを選ぶ、分布を利用するなどの方法がある。', 'シナリオは代表的な可能世界。多すぎると計算負荷、少なすぎると代表性不足。', 'シナリオ数・極端値・中間値の選び方を説明できること。', f'{EXAM["quasi"]}, WS24/25 Aufgabe 1 と関連。', 'シナリオ数を増やす利点と欠点は何か。'),
20: ('データから区間を決める。上限を90%分位、下限を10%分位などにし、悲観的なら悪い方向へシフトする。', '区間モデルは、確率を明示せずに可能範囲を表す。楽観/悲観の調整でリスク姿勢を入れる。', '分位点、上限/下限、悲観/楽観調整を説明する。', f'SS23 Aufgabe 3, WS24/25 Aufgabe 1 と関連。', 'なぜ最小値・最大値ではなく10%/90%分位を使うことがあるか。'),
21: ('アジェンダ。不確実性下の意思決定へ進む。ここからprescriptive analyticsの観点になる。', 'これまで作った不確実性モデルを、どう意思決定基準に入れるかが問題になる。', 'stochastic decision making と quasi-stochastic decision makingを分ける。', f'WS24/25 Aufgabe 3 と関連。', '不確実性をモデル化した後、意思決定では何を最適化するか。'),
22: ('ナップサック問題の例。泥棒が価値と重量を持つ物を選び、容量制約内で価値を最大化する。', '不確実性下の意思決定基準を説明するための単純例。決定、目的、制約が分かりやすい。', '基本的な決定問題として、選択変数・目的・制約を認識する。', '後のstochastic/quasi-stochastic基準説明の前提。', 'ナップサック問題の決定変数・目的・制約を答えよ。'),
23: ('確率的環境では、売却価格や重量などが不確実になりうる。目的関数または制約が不確実性の影響を受ける。', '不確実性が目的にある場合は価値が変わり、制約にある場合は実行可能性が変わる。', 'objective uncertainty と constraint uncertaintyを区別する。', f'{EXAM["uncertainty_general"]}, SS24 Aufgabe 2a と関連。', '不確実性が目的関数にある例と制約にある例を挙げよ。'),
24: ('stochastic decision makingとquasi-stochastic decision makingは異なる。不確実性は目的関数または制約に影響し、実現値は決定後に明らかになる。stochasticでは期待値・偏差が既知、quasi-stochasticでは未知である。', '決定時点で未来情報は不明なので、直接 \\(F(x,\\xi)\\) を最小化できない。モデルに応じて期待値、分散、最悪ケース、regretなどを使う。', '「決定後に実現値が明らかになる」という順序を説明できること。', f'WS24/25 Aufgabe 3 と強く関連。', '決定前に未知で決定後に明らかになる情報を何と呼ぶか。'),
25: ('確率的意思決定。実行可能決定集合 \\(\\mathcal{X}\\)、具体的決定 \\(x\\)、決定後に分かるランダム情報 \\(\\xi\\)、コスト \\(F(x,\\xi)\\) を考える。直接最適化できないため期待値 \\(\\mathbb{E}[F(x,\\xi)]\\) を最小化する。', '確率分布がある場合、目的関数は期待コストになる。最適値 \\(\\zeta^*\\) と最適決定集合 \\(\\mathcal{S}^*\\) を定義できる。', '記号の意味を文章で説明できること。数式暗記だけでは不十分。', f'{EXAM["distribution"]}, WS24/25 Aufgabe 3 と関連。', '\\(x\\) と \\(\\xi\\) の違いを説明せよ。'),
26: ('Monte Carlo Sampling。\\(n\\)個のシナリオ \\(\\xi_i\\) をサンプルし、期待値 \\(\\mathbb{E}[F(x,\\xi)]\\) を標本平均 \\(\\frac{1}{n}\\sum_i F(x,\\xi_i)\\) で近似する。', '分布が分かる場合、ランダムサンプルで期待コストを近似できる。サンプル数が増えるほど近似は安定するが計算量も増える。', 'サンプリング手順、標本平均、決定問題への利用を説明する。', f'SS25 Exercise 4, {EXAM["distribution"]} と関連。指数分布などから遷移をサンプリングする論点。', 'Monte Carloで期待値を近似する式と手順を説明せよ。'),
27: ('期待値・分散原理。決定 \\(x\\) を期待値と分散を使う選好関数で評価する。分散を重み \\(q\\) で入れ、\\(\\mu(x)+q\\sigma^2(x)\\) のように扱う。\\(q=-1\\)はリスク志向、0は中立、1はリスク回避。', '期待値だけではリスクを表せない。分散を入れることで安定性/リスク姿勢を反映する。', 'リスク志向・中立・回避の違いと、分散が意思決定に与える影響を説明する。', f'WS24/25 Aufgabe 3 と関連。stochastic手法例として説明できる。', '期待値が同じ2案で分散が違う場合、リスク回避ならどちらを選ぶか。'),
28: ('Hurwicz基準。最悪実現と最良実現を考え、楽観係数 \\(\\lambda\\in[0,1]\\) により \\((1-\\lambda)\\cdot worst + \\lambda\\cdot best\\) を評価する。', 'quasi-stochasticで確率が不明なときの基準。\\(\\lambda\\) が大きいほど楽観的、小さいほど悲観的。', 'Hurwiczの式、\\(\\lambda\\) の意味、適用条件を説明できること。', f'{EXAM["hurwicz"]} と強く関連。SS25 Exercise 8で機能と適用条件が問われた。', '\\(\\lambda=0\\) と \\(\\lambda=1\\) はそれぞれ何を意味するか。'),
29: ('Minmax-Regret基準。各シナリオで完全情報があった場合の最良決定と、選んだ決定の差をregretとし、最大regretを小さくする。', '確率が不明でも「後から見てどれだけ後悔するか」を抑える。ロバストルーティングで重要。', 'regretの定義、best possible decisionとの比較、最大後悔最小化を説明する。', f'{EXAM["regret"]} と強く関連。SS23 Aufgabe 3, WS24/25 Aufgabe 1で問われた。', 'regretは何と何の差か。'),
30: ('ケーススタディへ移る。不確実性下の都市物流ルーティングを扱う。', 'ここから区間旅行時間とminmax regretを実際のVRP/TSPに適用する。', '理論基準を具体的な配送問題へ接続する。', f'SS23 Aufgabe 3, WS24/25 Aufgabe 1 と関連。', 'なぜ都市物流でロバストルーティングが必要か。'),
31: ('都市物流の課題。高需要・コスト圧力・高い顧客期待、交通混雑、変動する旅行時間があり、旅行時間不確実性をルーティングへ統合する必要がある。', 'ケーススタディの動機。都市配送ではサービスレベルと効率の両立が必要。', '不確実性が顧客サービスと運用コストへ与える影響を説明する。', f'SS23 Aufgabe 3, SS24 Aufgabe 2a と関連。', '都市物流で旅行時間不確実性が重要な理由を2つ挙げよ。'),
32: ('都市物流の役割。Shipping companyは顧客とサービスレベルを持ち、logistic service providerは車両を運用し事前配送計画を立てる。サービスレベルは旅行時間に影響されるため、計画段階で不確実性情報を考慮する必要がある。', '意思決定主体と目的を分ける。荷主はサービス水準、物流業者は運行計画とコストを重視する。', 'シナリオ型問題で主体、状態、決定、目的を切り分ける練習になる。', '未知シナリオ型過去問への応用に有用。', 'Shipping companyとlogistic service providerの関心はどう違うか。'),
33: ('準確率的モデルは区間 \\([l,u]\\) で旅行時間を表し、小さい観測数でも扱いやすい。一方、確率的モデルは期待値 \\(\\mu\\) と分散 \\(\\sigma^2\\) や分布を用いるが、大量データと分布選択が必要で抽象的になる。都市物流では区間旅行時間が適切とされる。', 'Lecture 3の重要比較表。データ要件、解釈性、集約方法、モデル複雑性でstochasticとquasi-stochasticを比較する。', 'どちらが常に優れているのではなく、データ状況と用途で選ぶ。', f'{EXAM["quasi"]}, WS23/24 Aufgabe 7, WS24/25 Aufgabe 3 と強く関連。', 'データが少ない場合に区間旅行時間が適する理由は何か。'),
34: ('情報モデルデータ生成。Shifted Gamma分布、平均旅行時間、変動係数を使い、500観測をランダムに生成する。', 'ケースでは確率分布から観測を作り、そこから区間やシナリオを構成している。', '分布パラメータ、変動係数、サンプリングの意味を理解する。', f'{EXAM["distribution"]}, SS25 Exercise 4 と関連。', '変動係数が大きいと分布はどう変わるか。'),
35: ('情報モデルは2つの旅行時間行列からなる。\\(U\\)は上限でピーク交通の95%分位、\\(L\\)は下限でオフピーク交通の5%分位。常に \\(l_{ij}\\le u_{ij}\\)。', '区間旅行時間を行列として表すことで、ロバストTSP/VRPの入力になる。', '上限/下限行列、分位点、区間制約を説明できること。', f'{EXAM["regret"]}, WS24/25 Aufgabe 1 と関連。', '\\(L\\) と \\(U\\) はそれぞれ何を表すか。'),
36: ('Minmax regret基準を用いたロバストTSP。ツアーで使う辺と使わない辺を考え、旅行時間区間のもとで後悔を最小化する。', 'ツアーは全シナリオで同じでも、各シナリオでの最適ツアーとの差がregretになる。', 'ロバスト解は平均最短ではなく、悪いシナリオでの後悔を抑える。', f'{EXAM["regret"]} と強く関連。', 'ロバストTSPでregretを最小化する目的は何か。'),
37: ('目標は多くの交通速度シナリオで実装可能なルートを見つけること。効率性と punctuality/reliability のトレードオフがある。最良ケースだけは実行可能性を壊し、最悪ケースだけは効率が悪い。regretベースがバランスを取ることを期待する。', 'ロバスト性の直感を説明するページ。平均、最良、最悪のいずれかだけでは不十分な理由を理解する。', '効率性、信頼性、earliness/lateness、deviationを使って評価する。', f'SS23 Aufgabe 3, WS24/25 Aufgabe 1 と関連。', '最良ケースだけで計画すると何が危険か。'),
38: ('問題設定はTwo-Tier Delivery network。サテライトを中継点とし、デポからサテライトへ車両で配送し、サテライトから最終配送を行う。目的は移動時間とサテライト待ち時間の最小化。', '複雑な物流ネットワークでも、情報モデルと決定モデルを分けて整理できる。', '配送ネットワーク、決定、目的関数、待ち時間を識別する。', '未知シナリオ型のモデル化問題への練習。', 'Two-Tier配送でサテライトは何の役割を持つか。'),
39: ('結果。minmax regret基準とメタヒューリスティックを用い、AVG, UB, ITTを比較する。評価基準は車両数、総旅行時間、サテライト到着の平均ずれ。', 'ロバスト手法を評価するには、平均だけでなく最悪ケースや区間モデルでの実行品質を見る。', '結果表は、手法名より評価軸を読み取ることが重要。', f'{EXAM["regret"]} と関連。', 'ロバストルートを評価するとき、総旅行時間以外に何を見るべきか。'),
40: ('まとめ。不確実性は情報モデルと決定モデルの両方で考慮すべきで、意思決定に大きな影響を与える。適切な不確実性モデルが、意思決定関連データを有効に使う条件である。', 'Lecture 3の結論。分布があるかないかに応じて、stochastic/quasi-stochastic手法を選ぶ。', '試験では、不確実性の種類、モデル選択、意思決定基準、具体例への適用を一体で説明する。', f'{EXAM["uncertainty_general"]}, {EXAM["quasi"]}, {EXAM["regret"]} と関連。', 'Lecture 3の最重要論点を3つ挙げよ。'),
41: ('今後の問い。変化に反応できるか。例として、現在の交通情報に基づいてTSPを再計画する。', 'これはLecture 4のdynamismへの橋渡し。不確実性を事前に織り込むだけでなく、新情報に反応する段階へ進む。', 'uncertainty と dynamism の接続を理解する。', 'Lecture 4/5の動的意思決定問題と関連。', '事前ロバスト計画と再計画の違いを説明せよ。'),
}

NOTES_MAP = {1: L1, 2: L2, 3: L3}


def clean_lines(text: str) -> list[str]:
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    out = []
    for l in lines:
        if l.startswith('Data Driven Decision Making') or l.startswith('©'):
            continue
        if l in {'•', ''}:
            continue
        out.append(l)
    return out


def slide_title(doc, idx):
    lines = clean_lines(doc[idx].get_text('text'))
    return lines[0] if lines else f'Slide {idx+1}'


def default_note(lecture_no, page_no, title):
    if lecture_no == 1:
        return (f'このスライドは第1回Overviewの「{title}」に関するページである。', '講義全体の導入として、後続講義の概念を位置づける。', '後続の情報モデル、不確実性、動的意思決定へどう接続するかを把握する。', '過去問との直接対応は限定的だが、概念説明問題の背景になる。', f'{title} の役割を一文で説明せよ。')
    if lecture_no == 2:
        return (f'このスライドは情報モデル・決定モデルの「{title}」を扱う。', '現実データを意思決定に使える形へ変換する流れの一部である。', '情報モデルと決定モデルのどちらに属する話かを常に区別する。', 'Lecture 2の過去問では、BAプロセス、TSP、時間依存旅行時間との関連で問われる可能性がある。', f'{title} が情報モデルと決定モデルのどちらに関係するか説明せよ。')
    return (f'このスライドは不確実性の「{title}」を扱う。', '確率分布、シナリオ、区間、ロバスト性のいずれかに接続して理解する。', '不確実性をどう表し、意思決定基準へどう入れるかを説明する。', 'Lecture 3の過去問ではstochastic/quasi-stochastic、分布、Hurwicz、regretが頻出である。', f'{title} をstochastic/quasi-stochasticの観点から説明せよ。')


def latex_escape_preserve_math(s: str) -> str:
    # Preserve \\(...\\) math segments.
    parts = re.split(r'(\\\(.+?\\\))', s)
    escmap = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    out = []
    for part in parts:
        if part.startswith('\\(') and part.endswith('\\)'):
            out.append(part)
        else:
            tmp = part
            for k,v in escmap.items():
                tmp = tmp.replace(k,v)
            out.append(tmp)
    return ''.join(out)


def md_escape(s: str) -> str:
    return s


def section_block(label, content):
    return f"\\noindent\\textbf{{{label}}}\\; {latex_escape_preserve_math(content)}\\par\n"


def make_md(lec):
    doc = fitz.open(MAT / lec['pdf'])
    rows = []
    rows.append('---')
    rows.append(f"lecture_id: {lec['id']}")
    rows.append(f"source_pdf: Materials/2026/{lec['pdf']}")
    rows.append(f"slides: {len(doc)}")
    rows.append('status: draft_for_review_l01_l03')
    rows.append('workflow: Markdown主原稿。画像は相対リンク、数式はLaTeX記法。PDF化時はChatGPTが意味的にLaTeX変換。')
    rows.append('---\n')
    rows.append(f"# Lecture {lec['no']}: {lec['title']} - 日本語訳・解説・試験対策ノート\n")
    rows.append('> レビュー用ドラフト。1スライド=1ノートページを保つため、各ページの説明は下半分に収まる長さへ圧縮しています。\n')
    for i in range(len(doc)):
        p = i+1
        title = slide_title(doc, i)
        trans, expl, point, exam, q = NOTES_MAP[lec['no']].get(p, default_note(lec['no'], p, title))
        img = f"../assets/slides/{lec['id']}/{lec['id']}_p{p:03d}.png"
        rows.append(f"## Slide {p:03d}: {title}\n")
        rows.append(f"![Slide {p:03d}]({img})\n")
        rows.append('### 日本語訳・要約\n')
        rows.append(trans + '\n')
        rows.append('### 解説\n')
        rows.append(expl + '\n')
        rows.append('### 試験で確実に理解すべき点\n')
        rows.append(point + '\n')
        rows.append('### 過去問との関連\n')
        rows.append(exam + '\n')
        rows.append('### 確認問題\n')
        rows.append(f"1. {q}\n")
    return '\n'.join(rows)


def make_tex_section(lec):
    doc = fitz.open(MAT / lec['pdf'])
    rows = []
    rows.append(f"\\section*{{Lecture {lec['no']}: {latex_escape_preserve_math(lec['title'])}}}\n")
    for i in range(len(doc)):
        p = i+1
        title = slide_title(doc, i)
        trans, expl, point, exam, q = NOTES_MAP[lec['no']].get(p, default_note(lec['no'], p, title))
        img = f"../Materials/2026/{lec['pdf']}"
        rows.append('% --- slide page ---')
        rows.append('\\clearpage')
        rows.append('\\thispagestyle{empty}')
        rows.append(f"\\noindent\\textbf{{Lecture {lec['no']} / Slide {p:03d}: {latex_escape_preserve_math(title)}}}\\hfill {{\\scriptsize source: {latex_escape_preserve_math(lec['pdf'])}}}\\par")
        rows.append('\\vspace{1mm}')
        rows.append(f"\\noindent\\makebox[\\textwidth][c]{{\\includegraphics[page={p},width=\\textwidth,height=0.455\\textheight,keepaspectratio]{{{img}}}}}")
        rows.append('\\vspace{1mm}')
        rows.append('\\begin{minipage}[t][0.47\\textheight][t]{\\textwidth}')
        rows.append('\\scriptsize')
        rows.append('\\setlength{\\parskip}{1.2pt}')
        rows.append('\\begin{multicols}{2}')
        rows.append(section_block('日本語訳・要約', trans))
        rows.append(section_block('解説', expl))
        rows.append(section_block('試験ポイント', point))
        rows.append(section_block('過去問関連', exam))
        rows.append(section_block('確認問題', q))
        rows.append('\\end{multicols}')
        rows.append('\\end{minipage}')
    return '\n'.join(rows)


def make_main_tex():
    includes = '\n'.join([f"\\input{{sections/{lec['tex']}}}" for lec in lectures])
    return rf'''
\documentclass[a4paper,10pt]{{article}}
\usepackage[margin=8mm]{{geometry}}
\usepackage{{fontspec}}
\usepackage{{xeCJK}}
\usepackage{{graphicx}}
\usepackage{{multicol}}
\usepackage{{amsmath,amssymb}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}
\setmainfont{{Noto Sans}}
\setsansfont{{Noto Sans}}
\setCJKmainfont{{Noto Sans CJK JP}}
\setlength{{\parindent}}{{0pt}}
\setlist{{nosep,leftmargin=*}}
\hypersetup{{colorlinks=true,linkcolor=blue,urlcolor=blue}}
\begin{{document}}
\begin{{titlepage}}
\centering
\vspace*{{2cm}}
{{\Huge Data Driven Decision Making\\}}
\vspace{{0.5cm}}
{{\Large Lecture 1-3 日本語訳・解説・試験対策ノート\\}}
\vspace{{1cm}}
{{\large Review draft generated from Markdown notes\\}}
\vspace{{1cm}}
\begin{{minipage}}{{0.85\textwidth}}
このPDFは、1スライド=1学習ページとして、上半分に元スライド画像、下半分に日本語訳・解説・試験対策ポイント・過去問関連・確認問題を配置したレビュー用ドラフトです。過去問関連は重要論点の発見に使うものであり、出題範囲を限定するものではありません。
\end{{minipage}}
\vfill
{{\large Materials/2026: Lecture 1-3}}
\end{{titlepage}}
\tableofcontents
\clearpage
{includes}
\end{{document}}
'''


def make_focus_doc():
    return '''# Lecture 1-3 過去問ベース重要論点レビュー用メモ

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
- 必要理解: 静的なtravel time matrixではなく、出発時刻に依存する \\(d_{ij}(t)\\) や \\(\\tau_{ij}(t)\\) を用いる。時間依存性があると、挿入や経路選択により後続の到着時刻も変わる。
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
- 必要理解: 確率変数、実現値、確率、期待値、分散、分布フィッティング、Monte Carlo samplingを説明する。\\(x\\) は決定、\\(\\xi\\) は決定後に分かるランダム情報である。
- 過去問以外の対策: 期待値だけでなく分散やリスク姿勢が意思決定に影響する例を説明する。

## 7. Hurwicz基準とMinmax Regret

- 主な対応箇所: Lecture 3 Slide 28-29, 35-37
- 関連過去問: SS23 Aufgabe 3, WS24/25 Aufgabe 1, SS25 Exercise 8
- 必要理解: Hurwiczは最悪ケースと最良ケースを楽観係数で重み付けする。Minmax regretは各シナリオで完全情報の最良決定との差を後悔として測り、最大後悔を抑える。
- 過去問以外の対策: 旅行時間区間 \\([l,u]\\) を使い、平均・最悪・regretのどれを選ぶと何が起こるかを説明できるようにする。
'''


def main():
    NOTES.mkdir(exist_ok=True)
    LATEX_SEC.mkdir(parents=True, exist_ok=True)
    OUT_DOCS.mkdir(exist_ok=True)
    for lec in lectures:
        (NOTES / lec['md']).write_text(make_md(lec), encoding='utf-8')
        (LATEX_SEC / lec['tex']).write_text(make_tex_section(lec), encoding='utf-8')
    (ROOT / 'latex' / 'main_l01_l03.tex').write_text(make_main_tex(), encoding='utf-8')
    (OUT_DOCS / '05_l01_l03_exam_focus.md').write_text(make_focus_doc(), encoding='utf-8')
    print('Generated notes, latex, and focus doc for Lecture 1-3')

if __name__ == '__main__':
    main()
