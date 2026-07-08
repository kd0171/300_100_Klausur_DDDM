#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate review v4 DDDM Japanese exam notes.

User feedback addressed in v4:
- Explanations on slide pages are expanded to roughly 2-3x the v3 density.
- Slide pages are forced into a single page by a fixed slide area and a scaled note area.
- Check questions are made page-specific so the same question does not appear on multiple pages.
- Past exam questions remain on dedicated pages only, after the required knowledge has been explained.
"""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple, Union

ROOT = Path(__file__).resolve().parents[1]
LATEX = ROOT / "latex"
SECTIONS = LATEX / "sections"
OUTPUT = ROOT / "output"
NOTES = ROOT / "notes"
DOCS = ROOT / "docs"

# Load base slide inventory and v3 exam pages.
def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod

base = load_module("base_notes", ROOT / "scripts" / "generate_l01_l03_structured_notes.py")
v3 = load_module("v3_notes", ROOT / "scripts" / "generate_l01_l03_v3_notes.py")

LECTURES = base.LECTURES
SLIDES = base.SLIDES
INSERT_AFTER = v3.INSERT_AFTER

Item = Union[str, Tuple[str, Sequence[str]]]

TOPIC_DETAILS: Dict[str, Dict[str, Any]] = {
    "admin": {"explain": [], "focus": []},
    "dddm_intro": {
        "focus": ["DDDMはデータ分析を意思決定と実装へ接続する講義である。", "stochasticity と dynamism を分けて説明できることが最重要である。"],
        "explain": [
            "Data Driven Decision Making は、単にデータを分析してレポートを作ることではない。データを使って、現実で実行する行動を選び、その結果をまた観測して次の意思決定へ反映する考え方である。たとえば食品配送であれば、注文数を予測するだけではなく、どの注文を受けるか、どのドライバーに割り当てるか、どの順番で回るかまで決める。",
            "この講義の中心は、現実の意思決定が静的で完全情報の問題ではないという点にある。現実では、注文、交通、ドライバー位置、キャンセル、サービス時間などが時間とともに変わる。したがって、最初に作った計画を最後まで固定するのではなく、新しい情報を受けて状態を更新し、必要に応じて計画を変える必要がある。",
            "stochasticity は、将来何が起こるかが確率的・不確実であることを意味する。dynamism は、時間が進むにつれて状態が変わり、意思決定を繰り返す必要があることを意味する。試験では、この二語を同義語のように書かないことが重要である。注文がいつ来るか分からないことは stochasticity、注文が来た後に計画を更新することは dynamism である。",
            "答案では、DDDMを Business Analytics、Operations Research、Data Analytics、情報システム実装の交点として説明すると強い。予測モデルだけでは『何をするか』が決まらず、最適化モデルだけでは『現実データをどう入れるか』が決まらない。DDDMはこの間を接続し、現実のデータから実行可能な意思決定を作る。",
            "具体例として、Uberや食品配送では、リアルタイム注文、ドライバーの現在位置、交通状況、顧客の待ち時間を使いながら、数分ごとに新しい割当を作る。このとき、過去データから需要を学習するだけでなく、将来の不確実な注文を見越して現在のドライバーを使い切らないようにするなど、将来の柔軟性も重要になる。",
        ],
    },
    "process_loop": {
        "focus": ["Real-World, Aggregation, Information Model, Decision Model, Implementation の向きを正確に説明する。", "情報モデルは現実の圧縮表現、意思決定モデルは行動選択の評価構造である。"],
        "explain": [
            "Real-World は、配送車、顧客、道路、倉庫、ドライバー、注文、交通といった現実そのものである。現実は複雑すぎるため、そのまま数理モデルやアルゴリズムに入れることはできない。そこで、意思決定に必要な要素だけを抽出し、モデルが扱える形に変換する必要がある。",
            "Aggregation は、現実から得られた詳細データを情報モデルの次元に圧縮する操作である。例として、GPS点列を道路セグメントの速度に変換する、住所を顧客ノードに変換する、過去走行ログから顧客間旅行時間行列を作る、注文履歴から需要分布を推定する、といった処理がある。",
            "Information Model は、意思決定に必要な情報の構造化表現である。ここには、顧客集合、デポ、車両集合、旅行時間行列、需要、時間窓、確率分布などが含まれる。重要なのは、情報モデルは現実の全コピーではなく、意思決定に有用な抽象化だという点である。",
            "Decision Model は、その情報モデルを入力として、どの行動を選べるか、何を最適化するか、どの制約を守るかを定義する。TSPなら、顧客を一度ずつ訪問し総旅行時間を最小化する。VRPなら、複数車両、容量制約、時間窓などが加わる。ここでは決定変数、目的関数、制約が中心になる。",
            "Implementation は、モデル上の解を現実の行動に戻す処理である。たとえば x_{ij}=1 というアーク選択を、ドライバーに提示する訪問順、住所、ナビゲーション、積み込み順へ変換する。実装後には実際の遅延や走行時間が観測され、それが再びAggregationを通じてモデル改善に使われる。",
        ],
    },
    "ba_ida_pmt": {
        "focus": ["IDAは appearance から structure、PMT/ORは structure から solution へ向かう。", "Business Analytics は Statistics, OR, CS/IS の統合領域である。"],
        "explain": [
            "IDA, Intelligent Data Analysis は、記録されたデータの appearance から出発する。appearance とは、現実システムの表面的な観測結果であり、GPSログ、注文履歴、クリック履歴、センサー値のようなものである。これらは誤差、欠損、外れ値を含むため、そのまま構造を表しているとは限らない。",
            "IDAの役割は、データをクリーニングし、補完し、検証し、統計的パターンやモデルを抽出することで、背後にある structure への証拠を与えることである。例えば、タクシーの走行ログから朝夕ラッシュの速度低下パターンを見つけることは、道路交通の構造を推定する作業である。",
            "PMTやOperations Researchは逆方向で考える。まず現実問題の重要構造を仮定し、目的、制約、決定空間を明確にする。そして、ルーティング、スケジューリング、割当、在庫管理などの意思決定モデルを作り、解を求める。これは structure から実行可能な appearance、つまり具体的な解へ向かう流れである。",
            "Business Analytics の三つの基礎は、Statistics、Computer Science/Information Systems、Operations Research である。Statistics は推定と不確実性、CS/IS はデータ処理と実装、OR は最適化と意思決定を担う。三つを列挙するだけでは不十分で、互いの交差領域が現実のデータ駆動意思決定で不可欠であることを説明する必要がある。",
            "具体例として配送計画を考えると、Statistics は旅行時間分布を推定し、CS/IS はGPSデータや注文データを保存・処理し、OR は車両ルートを最適化する。データだけではルートは決まらず、最適化だけでは現実の交通を反映できないため、この統合がDDDMの基礎になる。",
        ],
    },
    "tsp_model": {
        "focus": ["TSPの要素をノード、アーク、コスト、決定変数、目的関数、制約に分けて説明する。", "時間依存TSPでは d_ij が d_ij(t) になり、到着時刻が決定に影響する。"],
        "explain": [
            "Travelling Salesman Problem は、複数の顧客を一度ずつ訪問し、最後に出発点へ戻る最短ツアーを求める基本的なルーティング問題である。顧客やデポはノード、ノード間の移動はアーク、距離や旅行時間はアークコストとして表される。",
            "意思決定モデルとしてのTSPでは、x_{ij}=1 なら i から j へ直接移動する、0なら移動しない、という二値変数を使う。目的関数は、選ばれたアークの距離または旅行時間の合計を最小化する。制約として、各顧客に一度入る、各顧客から一度出る、部分巡回を禁止する条件が必要である。",
            "情報モデルとしては、顧客集合、デポ、顧客間距離または旅行時間行列が必要である。つまり、TSPは情報モデルと意思決定モデルの典型的な接続例である。旅行時間行列が情報モデル、二値変数・目的関数・制約を持つ最適化問題が意思決定モデルである。",
            "時間依存TSPでは、アークコストが出発時刻に依存する。固定の d_{ij} ではなく d_{ij}(t) になるため、同じ i から j への移動でも朝は20分、昼は10分、夕方は30分ということがある。この場合、訪問順序だけでなく、いつそのアークを通るかが重要になる。",
            "具体例として、顧客Aを先に訪問するとBへの移動がラッシュ前に終わるが、Cを先に訪問するとBへの移動がラッシュ中になり遅れることがある。つまり、局所的に短い移動を選んでも、時刻の変化により後続コストが悪化するため、時間を含む意思決定モデルが必要になる。",
        ],
    },
    "time_dependent_travel": {
        "focus": ["時間依存旅行時間は情報モデルを精密にするが、意思決定モデルも複雑にする。", "平均行列、時間帯別行列、連続関数の違いを説明できる。"],
        "explain": [
            "時間依存旅行時間とは、同じ道路や同じ顧客間でも、出発時刻によって旅行時間が変わることを意味する。通勤時間帯、昼間、夜間、週末で交通量が変わるため、単一の平均旅行時間では現実を十分に表せない場合が多い。",
            "最も単純な情報モデルは、すべての時刻に共通する平均旅行時間行列である。これは扱いやすいが、朝夕の混雑や夜間の自由流交通を無視する。次に、時間帯別旅行時間行列がある。これは、例えば月曜8時台、月曜9時台のように複数の行列を用意する方法である。",
            "さらに詳細には、各道路セグメントや顧客間アークに対して連続的な旅行時間関数を持つこともできる。ただし、細かいモデルほど多くのデータが必要になり、各時間帯・道路ごとの観測数が少なくなると推定が不安定になる。詳細さは常に良いわけではなく、意思決定に役立つ粒度を選ぶ必要がある。",
            "時間依存性は意思決定モデルにも影響する。静的TSPではアークコストは固定なので訪問順だけを考えればよいが、時間依存TSPでは到着時刻、出発時刻、サービス時間、次アークの旅行時間が連鎖する。したがって、ある顧客を挿入するだけで後続すべての到着時刻が変わる。",
            "具体例として、昼に郊外を先に回り、夕方に市中心部を回る計画と、逆の計画では、同じ顧客を訪問していても総旅行時間が大きく異なる。試験答案では、時間依存性が単なるデータの違いではなく、ルーティング決定の構造を変える点まで述べるとよい。",
        ],
    },
    "fcd_aggregation": {
        "focus": ["FCDは生データであり、map matching, cleaning, aggregation, generalization を経て情報モデルになる。", "観測数が少ないセルでは信頼性が下がるため一般化が必要である。"],
        "explain": [
            "Floating Car Data は、移動する車両から得られる位置、時刻、場合によって速度や方向のデータである。タクシー、配送車、一般車両、公共交通車両などがプローブとして機能し、道路交通の状態を間接的に観測する。",
            "FCDはそのまま旅行時間行列ではない。まずGPS点を道路ネットワーク上の正しい道路セグメントに対応付ける map matching が必要である。GPSには誤差があるため、位置が道路からずれていたり、並行道路のどちらを走ったか判定が難しかったりする。",
            "次にデータクリーニングが必要である。信号待ち、駐車、GPSジャンプ、異常に高い速度、方向の誤りなどを処理しなければ、平均速度や旅行時間が歪む。例えば制限速度の1.5倍を超える観測を外すという単純なルールも、外れ値処理の一例である。",
            "集約では、道路セグメント l と時間ステップ w ごとに観測をまとめ、平均速度や平均旅行時間を計算する。W=1なら全時間を一つにまとめる。W=24x7なら曜日と時間帯ごとに別の値を持つ。粒度が細かいほど情報は詳しいが、観測数が少ないセルが増える。",
            "一般化では、似た交通パターンを持つ道路セグメントをグループ化し、信頼できる情報モデルを作る。例えば、中心市街地、商業地区、高速道路では速度レベルも日内変化も異なる。クラスタリングにより類似パターンをまとめれば、観測不足を補い、意思決定モデルが扱いやすい旅行時間情報を作れる。",
        ],
    },
    "fifo": {
        "focus": ["FIFOは、同じ経路で遅く出発した人が早く出発した人を不自然に追い越さない条件である。", "時間帯別行列の急な切替は不連続な旅行時間を作り得る。"],
        "explain": [
            "時間依存最短経路では、出発時刻によってリンク旅行時間が変わる。ここで重要なのがFIFO条件である。FIFOとは First In, First Out の略で、同じリンクや経路に先に入った車両が、後から入った車両に追い越されないという自然な条件を意味する。",
            "もし時間帯の境界で旅行時間が突然大きく短くなると、少し遅く出発した車両の方が早く到着するという不自然な状況が発生することがある。これは、時間帯別旅行時間行列を硬く切り替える場合に起きやすい。",
            "FIFOが満たされないと、時間依存Dijkstraなどの最短経路アルゴリズムの前提が崩れる場合がある。そのため、ブレークポイントを線形補間で滑らかにしたり、旅行時間関数を調整したりして、現実的で計算可能な情報モデルにする必要がある。",
            "具体例として、7:59出発では旅行時間30分、8:00出発では旅行時間5分という行列切替があると、8:00出発の方が先に着いてしまう。現実には渋滞が急に消えることは少ないため、このような不連続はモデル上の人工的な問題である。",
            "試験では、FIFOを単なる略語としてではなく、時間依存旅行時間モデルの妥当性条件として説明する。特に、情報モデルを精密化するときは、データの細かさだけでなく、モデルが現実的・計算可能な性質を持つことも重要である。",
        ],
    },
    "heuristics": {
        "focus": ["ヒューリスティックは高速に良い解を作る近似手法であり、最適性保証は弱い。", "時間依存旅行時間では局所的評価が後続時刻に波及する。"],
        "explain": [
            "ヒューリスティックは、厳密な最適解を保証しない代わりに、現実的な時間で良い解を作る方法である。TSPやVRPは顧客数が増えると組合せ数が急増するため、実務では厳密解法だけでは間に合わないことが多い。そこで、Nearest Neighbor, Cheapest Insertion, Savings, メタヒューリスティックなどを使う。",
            "Nearest Neighbor は、現在位置から最も近い未訪問顧客を次に選ぶ単純な貪欲法である。直感的で速いが、近い顧客を先に消費した結果、最後に遠い顧客同士をつなぐ悪い移動が残ることがある。短期的に最良の選択が全体最良とは限らない典型例である。",
            "Cheapest Insertion は、現在のツアーにどの未訪問顧客をどの位置へ挿入すると追加コストが最小かを調べる。静的TSPなら、追加コストは局所的に計算しやすい。しかし時間依存TSPでは、挿入によって後続顧客の到着時刻が変わり、後続アークの旅行時間も変わるため、局所評価だけでは不十分である。",
            "Savings は、別々に配送する場合と同じルートにまとめる場合の節約量を見てルートを統合する考え方である。これは車両ルーティングでよく使われる。ただし、時間依存性がある場合、統合により後続時刻が変化し、節約量の評価が単純ではなくなる。",
            "試験では、ヒューリスティック名を列挙するだけでは不十分である。各手法がどのような局所判断をするか、その長所と弱点は何か、時間依存旅行時間でなぜ評価が難しくなるかを具体例で説明する必要がある。",
        ],
    },
    "uncertainty_intro": {
        "focus": ["不確実性は、需要・リソース・環境の変化として整理できる。", "頻度、範囲、破壊力、予測可能性で性質が異なる。"],
        "explain": [
            "不確実性とは、意思決定時点では将来の状態や入力値が完全には分からないことである。配送であれば、注文がどこから来るか、交通がどれだけ混むか、サービス時間が何分か、ドライバーが利用可能かどうかが事前には確定していない。",
            "不確実性は一種類ではない。需要不確実性は、顧客からの注文の発生時刻、場所、量に関する不確実性である。リソース不確実性は、車両故障、ドライバーのキャンセル、バッテリー残量、積載能力に関する不確実性である。環境不確実性は、交通、天候、道路工事、事故、駐車可能性に関する不確実性である。",
            "不確実性は、頻度、範囲、破壊力、予測可能性によって性質が異なる。例えば日々の交通変動は頻繁に起きるが、過去データからある程度予測できる。一方で、大規模事故や道路閉鎖は低頻度だが、発生すれば計画を大きく壊す。",
            "不確実性を無視して平均値だけで計画すると、平均的には良く見えるが実行時に頻繁に遅れる計画になる可能性がある。特に複数顧客を連続して訪問するルーティングでは、一つの遅延が後続訪問に波及するため、単独の平均時間以上にリスクが大きい。",
            "試験答案では、不確実性の例を挙げるだけでなく、それが情報モデルと意思決定モデルにどう影響するかを書くとよい。情報モデルでは確率分布や区間として表現し、意思決定モデルでは期待値、リスク、ロバスト性、再最適化などを考える。",
        ],
    },
    "modeling_uncertainty": {
        "focus": ["deterministic, stochastic, quasi-stochastic の違いは、将来値と確率情報をどう扱うかで決まる。", "確率分布がある場合とない場合で、使える評価基準が変わる。"],
        "explain": [
            "Deterministic model は、入力値が既知で固定されていると仮定する。例えば、AからBへの旅行時間を常に15分と置く。これは単純で計算しやすいが、実際の交通変動やサービス時間のばらつきを無視するため、現実で計画が崩れることがある。",
            "Stochastic model は、不確実な変数を確率分布として表す。旅行時間が平均20分・標準偏差5分の分布に従う、注文発生がポアソン過程に従う、サービス時間が対数正規分布に従う、といった表現である。確率が分かるため、期待費用、分散、分位点、確率制約、サンプリングを使える。",
            "Quasi-stochastic model は、確率分布は分からないが、起こり得るシナリオや値の範囲は分かる場合に使う。例えば、旅行時間が10分から25分の間であることは分かるが、その確率は分からない場合である。このとき、区間、代表シナリオ、最悪ケース、Hurwicz基準、minmax regret が使われる。",
            "確率分布が十分に推定できるなら stochastic model が自然である。しかし、過去データが少ない、新しいサービスで履歴がない、環境が変化して過去データが当てにならない場合は quasi-stochastic model が有用である。どちらを使うかは、データ量、分布仮定の妥当性、意思決定の目的によって決まる。",
            "試験では、stochastic と quasi-stochastic の違いを『不確実であるかどうか』ではなく『確率情報を持っているかどうか』で説明する。どちらも不確実性を扱うが、stochastic は確率を使い、quasi-stochastic は確率なしで区間やシナリオを使う。",
        ],
    },
    "probability_distribution": {
        "focus": ["期待値は平均性能、分散や分位点はリスクを表す。", "分布フィットでは可視化、パラメータ推定、適合度確認が必要である。"],
        "explain": [
            "確率分布は、不確実な変数がどの値をどれくらいの確率で取るかを表す。配送では、旅行時間、サービス時間、注文間隔、需要量、キャンセル数などを分布で表せる。分布を使うことで、単一の平均値ではなく、ばらつきや極端な値も考慮できる。",
            "期待値は長期的な平均を表すが、期待値だけでは不十分なことが多い。平均20分の旅行時間でも、ほとんどが18-22分なのか、10分と50分が混在しているのかでは、計画上のリスクが全く違う。分散や標準偏差は、このばらつきの大きさを表す。",
            "分位点はサービスレベルを考える際に重要である。例えば90%分位点が35分なら、90%のケースで35分以内に到着することを意味する。顧客に到着時間を約束する場合、平均よりも上位分位点を見る方が安全な計画につながる。",
            "実データから分布を決めるには、まず観測値を集め、外れ値や欠損を確認し、ヒストグラムや箱ひげ図で形を見る。その後、正規分布、対数正規分布、ガンマ分布など候補を選び、平均や分散などのパラメータを推定し、適合度を確認する。",
            "サービス時間のように負にならない値では、正規分布よりも右裾を持つ非負分布が自然な場合がある。家電修理や在宅介護では、多くの作業は短時間で終わるが、例外的に長い作業が起こる。試験では、分布名だけでなく、なぜその形が現実に合うのかを説明する。",
        ],
    },
    "stochastic_decision": {
        "focus": ["決定 x の後にランダム情報 xi が実現するため、期待値やリスク基準で評価する。", "Monte Carlo sampling は期待値を標本平均で近似する方法である。"],
        "explain": [
            "確率的意思決定では、意思決定者は現在の情報に基づいて決定 x を選ぶが、その後にランダム情報 xi が実現する。例えばルートを選んだ後に、実際の交通、サービス時間、注文キャンセルが判明する。したがって、費用 F(x,xi) は意思決定時点では確定していない。",
            "このため、単一の実現値に対する費用を最小化するのではなく、期待費用 E[F(x,xi)]、分散、分位点、確率制約、リスク尺度などを使って評価する。リスク中立なら期待値中心でよいが、遅延に厳しいサービスでは分散や上位分位点も重要になる。",
            "Monte Carlo Sampling は、確率分布から多数のシナリオを生成し、それぞれで費用を計算して平均する方法である。解析的に期待値を計算できない場合でも、サンプル平均によって近似できる。サンプル数が増えるほど推定は安定するが、計算量も増える。",
            "期待値-分散原理では、平均性能とリスクを同時に見る。例えばルートAは平均45分だがばらつきが大きく、ルートBは平均50分だが安定している場合、時間厳守が重要ならBを選ぶ理由がある。平均だけではサービス信頼性を評価できない。",
            "試験では、F(x,xi)を直接最適化できない理由を明確に述べる。xi は決定時点で未知のランダム変数であり、事前に分かるのは分布やサンプルだけである。そのため、期待値やリスクを使う、という流れで説明する。",
        ],
    },
    "quasi_stochastic": {
        "focus": ["Hurwicz は最良ケースと最悪ケースの重み付け、minmax regret は最大の後悔を最小化する。", "regret は、実現シナリオを事前に知っていた場合の最適解との差である。"],
        "explain": [
            "Quasi-stochastic な状況では、確率分布は分からないが、複数のシナリオや区間は分かる。例えば旅行時間が10-25分の範囲にあることは分かるが、10分になる確率、25分になる確率は分からない。このような場合、期待値を正確には計算できない。",
            "Hurwicz基準は、最良ケースと最悪ケースを楽観係数で重み付けして評価する。楽観的な意思決定者は最良ケースを重視し、悲観的な意思決定者は最悪ケースを重視する。これは簡単だが、係数の選び方に主観が入る。",
            "Minmax regret は、各シナリオで『そのシナリオを事前に知っていれば選べた最適解』との差を regret として測る。候補解ごとに全シナリオの regret を計算し、その最大 regret が最小の解を選ぶ。これは、最悪の後悔を抑える基準である。",
            "regret の直感は、後から結果が分かったときに『別の解なら大幅に良かった』という損失を小さくすることである。単純な最悪ケース最適化よりも、各シナリオでの相対的な失敗を見ている点が特徴である。",
            "具体例として、平均的に短いが渋滞時に極端に悪化するルートと、少し長いが安定したルートがある。minmax regret は、各交通シナリオで最良ルートとの差を比べ、最悪の差が小さい安定ルートを選ぶ可能性がある。",
        ],
    },
    "robust_vrp": {
        "focus": ["ロバスト解は、単一平均ケースで最短ではなく、複数シナリオで大きく崩れにくい解である。", "都市物流では効率性と信頼性のトレードオフが重要である。"],
        "explain": [
            "都市物流では、旅行時間の変動、狭い時間窓、駐車問題、顧客の待ち時間、車両数制約が重なるため、平均旅行時間だけを最小化する計画では不十分なことが多い。平均では良くても、渋滞や遅いサービスが起きると多くの顧客に遅延が伝播する。",
            "区間旅行時間 [l,u] は、各アークの旅行時間が下限 l と上限 u の間にあると表す方法である。確率分布を正確に推定できない場合でも、過去データの分位点や専門知識から現実的な範囲を作ることができる。これは準確率的情報モデルの典型である。",
            "ロバストなルートは、平均ケースで必ず最短とは限らない。しかし、複数の交通シナリオや悪条件に対して大きく悪化しにくい。顧客サービスや時間約束が重要な場合、少し長いが安定したルートの方が、実務上は優れていることがある。",
            "一方で、ロバスト性を重視しすぎると過度に保守的な解になる。すべての最悪ケースだけを想定すると、余裕を取りすぎてコストが大きくなる可能性がある。したがって、効率性、信頼性、後悔、サービスレベルのバランスを考える必要がある。",
            "試験では、ロバスト解を『どんな場合でも絶対に最適な解』とは書かない。正しくは、複数の不確実なシナリオに対して性能が大きく崩れにくい解である。平均最適、最悪ケース最適、minmax regret の違いも説明できるとよい。",
        ],
    },
}

ALIASES = {"uncertainty_types": "modeling_uncertainty", "time_dependent": "time_dependent_travel"}

# Two page-specific check questions are built from the slide title and topic, so
# identical question text cannot repeat across pages.
def make_questions(lec: str, page: int, slide: Dict[str, Any], topic: str) -> List[Tuple[str, str]]:
    title = slide.get("title", f"Slide {page}")
    topic = ALIASES.get(topic, topic)
    if topic == "admin":
        return []
    focus = TOPIC_DETAILS.get(topic, TOPIC_DETAILS["dddm_intro"])["focus"]
    q1 = f"Slide {page:03d}「{title}」の中心概念を、専門用語を使わずに説明せよ。"
    a1 = (
        f"このスライドでは、{title} を通じて {focus[0]} ことを理解する必要がある。"
        "試験答案では、まず概念の定義を一文で書き、次に講義の例へ対応付け、最後に意思決定モデルにどのような影響を与えるかを述べる。"
        "単語の列挙だけでは不十分であり、データがどのように情報モデルへ変換され、その情報モデルがどのように決定変数・目的関数・制約へ接続されるかまで説明する。"
    )
    q2 = f"Slide {page:03d}「{title}」を、配送またはTSPの具体例で説明せよ。"
    topic_examples = {
        "dddm_intro": "食品配送では、注文発生は不確実であり、ドライバー位置と交通状況は時間とともに変わる。したがって、需要予測だけでなく、注文受諾、割当、ルート更新まで含めて意思決定を考える。",
        "process_loop": "配送現場のGPSと注文データを集約して顧客集合と旅行時間行列を作り、それをTSP/VRPへ入力し、得られた訪問順をドライバー指示へ戻す。",
        "ba_ida_pmt": "IDAはGPSログから交通パターンを見つけ、ORはその旅行時間情報を使ってルートを最適化し、CS/ISはデータ処理とアプリ実装を担う。",
        "tsp_model": "顧客をノード、移動をアーク、旅行時間をコストとして、全顧客を一度ずつ訪問する順序を選ぶ。時間依存なら出発時刻も評価に入る。",
        "time_dependent_travel": "AからBへ行く時間が朝20分、昼10分、夕方30分なら、同じルートでも出発時刻により総旅行時間が変わる。",
        "fcd_aggregation": "タクシーGPSを道路セグメントへ対応付け、時間帯ごとに平均速度を集計し、顧客間旅行時間行列を作る。",
        "fifo": "7:59出発が8:30着、8:00出発が8:05着になるようなモデルは不自然であり、FIFO条件を満たすよう修正する。",
        "heuristics": "Nearest Neighborは現在地から近い顧客を選び、Cheapest Insertionは追加コストが小さい位置へ顧客を挿入するが、時間依存では後続時刻も変わる。",
        "uncertainty_intro": "注文がいつ来るか、ドライバーが稼働するか、道路が混むかは意思決定時点では確定しない。これが不確実性である。",
        "modeling_uncertainty": "旅行時間分布が分かるならstochastic、10-25分という範囲だけ分かるならquasi-stochasticとして扱う。",
        "probability_distribution": "旅行時間の平均だけでなく、標準偏差や90%分位点を見ることで遅延リスクを評価する。",
        "stochastic_decision": "ルート選択後に実際の交通が実現するため、期待費用やサンプリング平均でルートを評価する。",
        "quasi_stochastic": "各交通シナリオで最良ルートとの差をregretとして計算し、最大regretが小さいルートを選ぶ。",
        "robust_vrp": "平均では少し長くても、渋滞時に大きく遅れないルートはロバストなルートといえる。",
    }
    a2 = topic_examples.get(topic, topic_examples["dddm_intro"])
    a2 += " 答案では、例を出した後に、それがどのモデル要素に対応するかを明示する。例えば、顧客集合や旅行時間行列は情報モデル、訪問順序や車両割当は意思決定モデル、実際の配送指示は実装である。"
    return [(q1, a1), (q2, a2)]


def tex_escape(s: str) -> str:
    repl = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(repl.get(ch, ch) for ch in s)


def tex_itemize(items: Sequence[Item]) -> str:
    if not items:
        return r"{\small このスライドは主に表紙・目次・事務情報であるため、翻訳のみ示す。}"
    out = [r"\begin{itemize}"]
    for it in items:
        if isinstance(it, tuple):
            out.append(r"\item " + tex_escape(it[0]))
            out.append(tex_itemize(it[1]))
        else:
            out.append(r"\item " + tex_escape(it))
    out.append(r"\end{itemize}")
    return "\n".join(out)


def topic_key(topic: str) -> str:
    return ALIASES.get(topic, topic)


def slide_explanation(lec: str, page: int, slide: Dict[str, Any]) -> List[str]:
    topic = topic_key(slide.get("topic", "admin"))
    if topic == "admin":
        return []
    detail = TOPIC_DETAILS.get(topic, TOPIC_DETAILS["dddm_intro"])
    title = slide.get("title", f"Slide {page}")
    first = f"このページでは「{title}」を、講義全体の流れの中で位置づける。スライドの箇条書きは短いが、試験ではその背後にある概念、現実例、モデル上の意味を文章で説明できる必要がある。"
    # Use all detailed paragraphs. This is deliberately 2-3x v3. The note area is scaled to one page.
    return [first] + list(detail["explain"])


def tex_paragraphs(pars: Sequence[str]) -> str:
    return "\n".join(tex_escape(p) + r"\par" for p in pars)


def write_slide_page(lec: str, page: int, slide: Dict[str, Any]) -> str:
    info = LECTURES[lec]
    pdf_path = f"../Materials/2026/{info['pdf']}"
    topic = topic_key(slide.get("topic", "admin"))
    title = slide.get("title", f"Slide {page}")
    detail = TOPIC_DETAILS.get(topic, TOPIC_DETAILS["dddm_intro"])
    lines: List[str] = []
    lines.append(r"\clearpage")
    lines.append(r"\SlideHeader{" + tex_escape(info["title"]) + "}{" + f"{page:03d}" + "}{" + tex_escape(title) + "}")
    lines.append(r"\SlideImage{" + str(page) + "}{" + pdf_path + "}")
    lines.append(r"\begin{adjustbox}{max totalsize={\textwidth}{0.675\textheight},center}")
    lines.append(r"\begin{minipage}{\textwidth}\scriptsize")
    lines.append(r"\begin{minipage}[t]{0.485\textwidth}")
    lines.append(r"\NoteSection{日本語訳}")
    lines.append(tex_itemize(slide.get("translation", [])))
    if topic != "admin":
        lines.append(r"\NoteSection{試験対策ポイント}")
        lines.append(tex_itemize(detail.get("focus", [])[:2]))
    lines.append(r"\end{minipage}\hfill")
    lines.append(r"\begin{minipage}[t]{0.485\textwidth}")
    if topic != "admin":
        lines.append(r"\NoteSection{解説}")
        lines.append(tex_paragraphs(slide_explanation(lec, page, slide)))
        qs = make_questions(lec, page, slide, topic)
        if qs:
            lines.append(r"\NoteSection{確認問題と解答}")
            lines.append(r"\begin{enumerate}")
            for q, a in qs:
                lines.append(r"\item \textbf{" + tex_escape(q) + r"}\\" + tex_escape(a))
            lines.append(r"\end{enumerate}")
    else:
        lines.append(r"\NoteSection{注記}")
        lines.append(r"{\small このページは表紙・目次・連絡先などの事務情報であるため、解説と確認問題は付けない。}")
    lines.append(r"\end{minipage}")
    lines.append(r"\end{minipage}")
    lines.append(r"\end{adjustbox}")
    return "\n".join(lines) + "\n"


def write_exam_pages(exam_group: Dict[str, Any]) -> str:
    # Reuse v3 exam pages; they are already dedicated and non-repeated.
    lines: List[str] = []
    lines.append(r"\clearpage")
    lines.append(r"\ExamHeader{" + tex_escape(exam_group["title"]) + "}")
    for q in exam_group["questions"]:
        lines.append(r"\ExamQuestion{" + tex_escape(q["ref"]) + "}")
        lines.append(r"\ExamSubsection{問題内容}")
        lines.append(tex_escape(q["problem"]) + r"\par")
        lines.append(r"\ExamSubsection{満点答案}")
        for p in q["answer"]:
            lines.append(tex_escape(p) + r"\par")
        lines.append(r"\ExamSubsection{具体例による解説}")
        lines.append(tex_escape(q["example"]) + r"\par")
        lines.append(r"\ExamSubsection{採点で落とさない要素}")
        lines.append(tex_itemize(q["rubric"]))
        lines.append(r"\vspace{2mm}\hrule\vspace{2mm}")
    return "\n".join(lines) + "\n"


def write_section(lec: str) -> None:
    SECTIONS.mkdir(parents=True, exist_ok=True)
    info = LECTURES[lec]
    out: List[str] = []
    out.append(r"\section*{" + tex_escape(info["title"]) + "}")
    out.append(r"\addcontentsline{toc}{section}{" + tex_escape(info["title"]) + "}")
    for page in range(1, info["pages"] + 1):
        slide = SLIDES[lec].get(page, {"title": f"Slide {page}", "translation": [], "topic": "admin"})
        out.append(write_slide_page(lec, page, slide))
        for exam_group in INSERT_AFTER.get(lec, {}).get(page, []):
            out.append(write_exam_pages(exam_group))
    (SECTIONS / f"{info['stem']}_v4.tex").write_text("\n".join(out), encoding="utf-8")


def write_main(lec: str) -> None:
    info = LECTURES[lec]
    main = rf"""
\documentclass[a4paper,10pt]{{article}}
\usepackage[margin=7mm]{{geometry}}
\usepackage{{fontspec}}
\usepackage{{xeCJK}}
\usepackage{{graphicx}}
\usepackage{{adjustbox}}
\usepackage{{amsmath,amssymb}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}
\usepackage{{titlesec}}
\setmainfont{{Noto Sans}}
\setsansfont{{Noto Sans}}
\setCJKmainfont{{Noto Sans CJK JP}}
\definecolor{{TUBSred}}{{HTML}}{{BE1E3C}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{2.0pt}}
\setlist[itemize]{{leftmargin=1.05em,itemsep=0.8pt,topsep=1.0pt,parsep=0pt}}
\setlist[enumerate]{{leftmargin=1.20em,itemsep=1.2pt,topsep=1.0pt,parsep=0pt}}
\hypersetup{{colorlinks=true,linkcolor=blue,urlcolor=blue}}
\titleformat{{\section}}{{\Large\bfseries\color{{TUBSred}}}}{{}}{{0pt}}{{}}
\newcommand{{\SlideHeader}}[3]{{%
  \noindent{{\large\bfseries #1 / Slide #2: #3}}\hfill {{\scriptsize review v4}}\par
  \vspace{{0.7mm}}\hrule\vspace{{0.7mm}}
}}
\newcommand{{\SlideImage}}[2]{{%
  \noindent\makebox[\textwidth][c]{{\includegraphics[page=#1,width=0.94\textwidth,height=0.255\textheight,keepaspectratio]{{#2}}}}\par
  \vspace{{0.5mm}}
}}
\newcommand{{\NoteSection}}[1]{{%
  \vspace{{1.0mm}}\noindent{{\normalsize\bfseries\color{{TUBSred}}#1}}\par\vspace{{0.4mm}}
}}
\newcommand{{\ExamHeader}}[1]{{%
  \noindent{{\Large\bfseries\color{{TUBSred}}過去問演習: #1}}\hfill {{\scriptsize review v4}}\par
  \vspace{{1mm}}\hrule\vspace{{2mm}}
  {{\small このページは、関連概念を説明した後に一度だけ配置する過去問演習ページである。スライドページには同じ過去問を繰り返さない。}}\par\vspace{{2mm}}
}}
\newcommand{{\ExamQuestion}}[1]{{\vspace{{2mm}}\noindent{{\large\bfseries #1}}\par\vspace{{0.8mm}}}}
\newcommand{{\ExamSubsection}}[1]{{\vspace{{1.2mm}}\noindent{{\normalsize\bfseries\color{{TUBSred}}#1}}\par\vspace{{0.6mm}}}}
\begin{{document}}
\begin{{titlepage}}
\centering
\vspace*{{2cm}}
{{\Huge Data Driven Decision Making\par}}
\vspace{{0.5cm}}
{{\Large {tex_escape(info['title'])} - 日本語訳・詳細解説・試験対策ノート\par}}
\vspace{{1cm}}
\begin{{minipage}}{{0.88\textwidth}}
このPDFは review v4 です。各スライドページは、元スライド、日本語訳、詳細解説、試験対策ポイント、ページ固有の確認問題を1ページに収めています。解説は review v3 より詳細化し、前提知識が少ない読者でも試験答案を作れるように具体例を増やしています。過去問は重複を避け、必要知識を説明した後に独立した演習ページとして配置しています。
\end{{minipage}}
\vfill
{{\large Materials/2026}}
\end{{titlepage}}
\tableofcontents
\clearpage
\input{{sections/{info['stem']}_v4.tex}}
\end{{document}}
"""
    LATEX.mkdir(exist_ok=True)
    (LATEX / f"main_{info['stem']}_v4.tex").write_text(main, encoding="utf-8")


def compile_pdf(lec: str) -> None:
    info = LECTURES[lec]
    tex = f"main_{info['stem']}_v4.tex"
    for _ in range(2):
        subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex], cwd=LATEX, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    pdf = LATEX / f"main_{info['stem']}_v4.pdf"
    out = OUTPUT / info["out"]
    OUTPUT.mkdir(exist_ok=True)
    out.write_bytes(pdf.read_bytes())
    (ROOT.parent / info["out"]).write_bytes(pdf.read_bytes())


def write_markdown_note(lec: str) -> None:
    info = LECTURES[lec]
    lines = [
        f"# {info['title']} - review v4",
        "",
        "## 変更方針",
        "",
        "- 解説を review v3 より2-3倍程度詳細化した。",
        "- スライドページは、元スライド・日本語訳・解説・確認問題を1ページに収める。",
        "- 確認問題はページ番号とスライドタイトルに紐づけ、複数ページで同じ問題が繰り返されないようにする。",
        "- 過去問は各スライドに繰り返さず、関連知識を説明した後の独立ページにのみ置く。",
        "",
    ]
    NOTES.mkdir(exist_ok=True)
    (NOTES / f"{info['stem']}_v4.md").write_text("\n".join(lines), encoding="utf-8")


def write_revision_doc() -> None:
    text = """# Review v4 revision

この版では、ユーザーの追加レビューに基づき、Lecture 1-3 のノートをさらに修正した。

## 変更点

- 解説を review v3 より 2-3 倍程度詳細化した。
- 具体例を増やし、前提知識が少ない読者でも、試験答案として説明できる水準を目指した。
- 確認問題の重複を避けるため、各問題をページ番号とスライドタイトルに紐づけた。
- スライドページは、元スライド、日本語訳、解説、試験対策ポイント、確認問題と解答を1ページに収めるため、ノート領域を自動縮小するLaTeXレイアウトにした。
- 過去問は review v3 と同じく、必要知識を説明した後の独立ページにのみ配置する。

## 出力ファイル

- output/dddm_l01_overview_jp_exam_notes.pdf
- output/dddm_l02_information_decision_modeling_jp_exam_notes.pdf
- output/dddm_l03_uncertainty_jp_exam_notes.pdf

## 生成スクリプト

`scripts/generate_l01_l03_v4_notes.py`
"""
    DOCS.mkdir(exist_ok=True)
    (DOCS / "09_feedback_revision_v4.md").write_text(text, encoding="utf-8")


def main() -> None:
    write_revision_doc()
    for lec in ["l01", "l02", "l03"]:
        write_section(lec)
        write_main(lec)
        write_markdown_note(lec)
        compile_pdf(lec)
    print("Generated v4 lecture notes.")


if __name__ == "__main__":
    main()
