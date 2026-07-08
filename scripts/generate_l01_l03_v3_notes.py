#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate v3 DDDM Japanese exam notes.

Revision logic:
- Each lecture is output as a separate PDF.
- Slide pages contain only the slide, Japanese translation, explanation, and check questions.
- Past exam questions are moved to dedicated exam-practice pages inserted only once after
  the relevant knowledge has been explained.
- Exam-practice pages contain the question context, a full-score answer, scoring points,
  examples, and common mistakes.
"""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple, Union

ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "Materials" / "2026"
LATEX = ROOT / "latex"
SECTIONS = LATEX / "sections"
OUTPUT = ROOT / "output"
NOTES = ROOT / "notes"

spec = importlib.util.spec_from_file_location("base_notes", ROOT / "scripts" / "generate_l01_l03_structured_notes.py")
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)  # type: ignore[attr-defined]

Item = Union[str, Tuple[str, Sequence[str]]]

LECTURES = base.LECTURES
SLIDES = base.SLIDES

# ---------------------------------------------------------------------------
# Topic explanations for slide pages.  These are deliberately not past-exam
# pages.  They are written so that each slide remains a one-page study note.
# ---------------------------------------------------------------------------
TOPIC_NOTES: Dict[str, Dict[str, Any]] = {
    "admin": {"explain": [], "focus": [], "questions": []},
    "dddm_intro": {
        "explain": [
            "DDDMでは、データを眺めるだけでなく、データに基づいて実行可能な行動を選ぶ。例えば、食品配送なら『どの注文をどのドライバーに割り当てるか』、在庫管理なら『いつ何個発注するか』が決定である。",
            "stochasticity は、将来情報が確実には分からないことを意味する。例として、注文発生、道路混雑、サービス時間、ドライバーのキャンセルがある。dynamism は、新しい情報が入るたびに状態と計画が変わることである。",
            "試験答案では、stochasticity=不確実な情報実現、dynamism=時間を通じた状態変化と再意思決定、と分けて書き、最後に『そのため将来を先読みしつつ柔軟性を残す必要がある』と結ぶとよい。",
        ],
        "focus": [
            "DDDM = データ分析 + 意思決定モデル + 現実への実装、というループで理解する。",
            "単なる予測ではなく、予測・観測を意思決定に変換する点が講義の中心である。",
        ],
        "questions": [
            ("DDDMは通常のデータ分析と何が違うか。", "通常のデータ分析は、過去データの記述や将来予測で終わる場合がある。DDDMでは、その予測や観測を使って具体的な行動を選ぶ。配送なら需要予測だけでなく、車両割当、訪問順序、注文受諾、再計画まで含める。したがって情報モデル、意思決定モデル、実装を一体で説明する必要がある。"),
            ("stochasticity と dynamism を例で区別せよ。", "食品配送で『次にどこから注文が来るか分からない』ことは stochasticity である。注文が実際に入った後、ドライバー位置や未配送注文が変わり、計画を作り直す必要があることは dynamism である。両者が合わさると stochastic dynamic decision problem になる。"),
        ],
    },
    "process_loop": {
        "explain": [
            "Real-World は、実際の配送現場、道路、顧客、車両、作業員のような現実対象である。現実は非常に複雑なので、そのまま最適化モデルには入れられない。",
            "Aggregation は、現実データを意思決定で使える形に圧縮する処理である。例: GPS点列を道路セグメント別速度へ変換する、住所を顧客ノードへ変換する、過去走行記録から旅行時間行列を作る。",
            "Information Model は『意思決定に必要な情報の表現』である。顧客集合、デポ、道路ネットワーク、旅行時間行列、需要分布、時間帯などが入る。Decision Model は『その情報を使って何を最適化するか』を表し、決定変数、目的関数、制約、実行可能解を定義する。",
            "Implementation は、モデルの解を現実の作業指示に戻す処理である。例: x_{ij}=1 というアーク選択を、ドライバー向けの住所順序とナビゲーションに変換する。実装後の観測により、モデル仮説は更新される。",
        ],
        "focus": [
            "Real-World -> Aggregation -> Information Model -> Decision Model -> Implementation -> Real-World の流れを、配送例で説明できる。",
            "Information Model と Decision Model を混同しない。前者は情報表現、後者は意思決定の評価・選択構造である。",
        ],
        "questions": [
            ("Information Model と Decision Model の違いを説明せよ。", "Information Model は、現実を意思決定に必要な形へ圧縮した情報表現である。例として、顧客集合、距離行列、時間帯別旅行時間、需要分布がある。Decision Model は、その情報を用いて選択肢を評価する数学的・論理的構造であり、決定変数、目的関数、制約を持つ。配送例なら、旅行時間行列は情報モデル、訪問順序を選んで総旅行時間を最小化するTSP/VRPは意思決定モデルである。"),
            ("Aggregation と Implementation を配送例で説明せよ。", "Aggregation は、GPS記録、道路地図、住所データなどを、顧客ノードや旅行時間行列に変換する処理である。Implementation は、最適化モデルが出した訪問順序やアーク選択を、実際のドライバーが使える配送順、住所リスト、ナビゲーションに変換する処理である。Aggregation は現実からモデルへ、Implementation はモデルから現実への橋である。"),
        ],
    },
    "ba_ida_pmt": {
        "explain": [
            "IDAは appearance から structure へ向かう。つまり、記録データの表面的なパターンから、背後の情報構造を推測する。例: GPS走行ログから道路混雑パターンを推定する。",
            "PMT/ORは structure から appearance/solution へ向かう。つまり、問題構造を仮定し、目的関数・制約・決定変数を作り、解を求める。例: 顧客集合と旅行時間行列からTSPを作る。",
            "Business Analytics では、データ側と意思決定側をつなぐ。データ分析だけでは『何を実行すべきか』が出ない。最適化だけでも、現実のデータを正しく表現しなければ役に立たない。",
        ],
        "focus": [
            "IDA = データから構造を発見する方向、PMT/OR = 構造から意思決定モデルと解を作る方向。",
            "三分野を列挙するだけでなく、交差領域がなぜ必要かを説明する。",
        ],
        "questions": [
            ("IDA と PMT/OR の方向性の違いを説明せよ。", "IDAは記録データ、つまり appearance から出発し、クリーニング、補完、検証、データマイニングを通じて情報構造やパターンを見つける。PMT/ORは問題構造を仮説として置き、目的、制約、決定空間を定義して、実行可能な解を計算する。DDDMでは両方が必要で、情報モデルが両者を接続する。"),
            ("Business Analytics の三分野を使って、配送計画を説明せよ。", "Statistics は旅行時間や需要の不確実性を推定する。Computer Science/Information Systems はGPS、注文、地図データを保存・処理し、システムとして実装する。Operations Research は訪問順序、車両割当、制約を最適化する。三つを統合することで、データに基づく実行可能な配送計画が得られる。"),
        ],
    },
    "tsp_model": {
        "explain": [
            "TSPでは、顧客をノード、顧客間移動をアーク、距離または旅行時間を重みとして表す。目的は、全顧客を一度ずつ訪問し、総移動時間または距離を最小にする訪問順序を求めることである。",
            "情報モデルとしては、顧客集合、デポ、顧客間旅行時間行列が必要である。意思決定モデルとしては、アークを使うかどうかを表す二値変数 x_{ij}、各顧客へ一度入る・一度出る制約、部分巡回除去制約、総旅行時間最小化の目的関数が必要である。",
            "時間依存を入れると、旅行時間は定数 d_{ij} ではなく、出発時刻 t に依存する d_{ij}(t) になる。ある顧客を先に訪問するか後に訪問するかで、後続アークの出発時刻が変わり、旅行時間も変わる。",
        ],
        "focus": [
            "TSPの基本定式化を、変数・目的関数・制約に分けて説明できる。",
            "時間依存TSPでは、旅行時間行列だけでなく時刻依存関数や複数行列が必要になる。",
        ],
        "questions": [
            ("TSPの数理モデルを言葉で説明せよ。", "ノード集合はデポと顧客、アーク集合は顧客間移動を表す。二値変数 x_{ij}=1 は、i から j へ直接移動することを意味する。目的は sum d_{ij}x_{ij} を最小化することである。制約として、各顧客に一度入る、各顧客から一度出る、複数の小さな巡回ができないようにする部分巡回除去制約が必要である。"),
            ("時間依存旅行時間がTSPを難しくする理由を説明せよ。", "静的TSPではアークのコストは固定である。しかし時間依存TSPでは、iからjへのコストが出発時刻に依存する。ある挿入や訪問順変更により後続の到着時刻が変わり、その後の全アークの旅行時間も変わるため、局所的な評価が全体に波及する。"),
        ],
    },
    "time_dependent_travel": {
        "explain": [
            "時間依存旅行時間では、道路や顧客間の旅行時間が時刻で変わる。朝の通勤時間、昼間、夕方では、同じ道路でも速度が違う。したがって一つの平均旅行時間だけでは現実を十分に表せない。",
            "情報モデルとしては、時間帯別旅行時間行列、または連続的な旅行時間関数を使う。例: 7-9時、9-15時、15-18時で別の行列を持つ。",
            "重要なのは、時間依存性は情報モデルだけでなく意思決定モデルも変える点である。訪問順序を決めるだけでなく、どの時刻にどのアークを通るかが決定に入る。",
        ],
        "focus": [
            "詳細な情報モデルほど現実に近いが、データ量・計算複雑性・解釈可能性にコストがある。",
            "時間依存旅行時間は、FCDなどから推定される。",
        ],
        "questions": [
            ("なぜ常に最も詳細な旅行時間モデルを選ばないのか。", "詳細なモデルは時間帯・道路セグメントごとに多くの観測を必要とする。観測が少ないセルでは平均値が不安定になり、過学習のように現実を誤って表す可能性がある。また、意思決定モデルの変数や制約が増え、計算時間が長くなる。したがって、意思決定に有用な粒度を選ぶ必要がある。"),
            ("時間帯別旅行時間行列の長所と短所を述べよ。", "長所は、朝夕の混雑など平均行列では消える変動を反映できることである。短所は、時間帯ごとに十分な観測が必要であり、境界時刻で旅行時間が不連続になる可能性があること、意思決定モデルが複雑になることである。"),
        ],
    },
    "fcd_aggregation": {
        "explain": [
            "Floating Car Data (FCD) は、車両から位置・時刻・場合によって速度を収集したデータである。タクシー、配送車、一般車両のGPSログが例である。",
            "FCDはそのまま旅行時間行列ではない。位置を道路セグメントに対応付ける map matching、方向の確認、異常値除去、時間帯ごとの集約が必要である。",
            "観測数が少ない道路や時間帯では平均速度が不安定になる。そこで、時間帯を広げる、似た道路をまとめる、空間的・時間的な一般化を行うなどの工夫が必要になる。",
        ],
        "focus": [
            "FCD -> map matching -> セグメント速度 -> 時間帯別旅行時間 -> 顧客間旅行時間行列、という変換を説明できる。",
            "データが最初に来るが、データは必ず加工・検証しなければ情報モデルにならない。",
        ],
        "questions": [
            ("FCDから旅行時間行列を作る手順を説明せよ。", "まず車両の位置・時刻・速度を取得する。次に位置を道路セグメントにマッチングし、方向と時刻を確認する。外れ値や停止などを処理し、セグメントと時間帯ごとに速度または旅行時間を集約する。最後に、顧客間経路を道路セグメント列として計算し、セグメント旅行時間を足し合わせて顧客間旅行時間行列を作る。"),
            ("小さな観測数が問題になる理由を説明せよ。", "観測数が少ないと、たまたま渋滞していた一台や異常なGPS点が平均値に大きく影響する。結果として、情報モデルが現実の典型的な状態ではなく偶然の観測を表してしまう。これを避けるには、時間帯や道路分類で集約したり、外れ値処理や補間を行う。"),
        ],
    },
    "heuristics": {
        "explain": [
            "Nearest Neighbor は、現在地から最も近い未訪問顧客を順に選ぶ貪欲法である。簡単だが、後半に悪い選択が残ることがある。",
            "Cheapest Insertion は、未訪問顧客を現在のツアーのどこに挿入すると追加コストが最小かを評価する。静的TSPでは使いやすいが、時間依存旅行時間では挿入が後続時刻を変えるため評価が難しくなる。",
            "Savings は、別々に訪問する場合と一つのツアーにまとめる場合の節約量を評価する考え方である。ヒューリスティックは高速だが、最適性保証は弱いことを説明できる必要がある。",
        ],
        "focus": ["主要ヒューリスティックの直感、長所、時間依存で難しくなる理由を説明できる。"],
        "questions": [
            ("Cheapest Insertion の考え方を説明せよ。", "現在のツアーに対して、まだ訪問していない顧客をどの位置に入れると追加旅行時間が最も小さいかを計算し、その最も安い挿入を繰り返す方法である。静的TSPでは追加コストは局所的に計算しやすい。"),
            ("時間依存旅行時間で Cheapest Insertion が難しくなる理由を述べよ。", "一人の顧客を挿入すると、その後の全顧客への到着時刻が変わる。旅行時間が時刻依存なら、後続アークのコストも変わる。したがって、挿入の効果は局所的な追加距離だけでは評価できず、全体の再評価が必要になる。"),
        ],
    },
    "uncertainty_intro": {
        "explain": [
            "不確実性とは、意思決定時点では将来の実現値が完全には分からないことである。需要、交通、サービス時間、ドライバーの可用性、天候、政治状況などが例である。",
            "不確実性は、頻度、範囲、破壊力、予測可能性で異なる。例えば毎日変わる交通量は高頻度だが比較的予測可能であり、突然の道路閉鎖は低頻度だが破壊力が大きい。",
            "不確実性は情報モデルに入るだけでなく、意思決定モデルにも影響する。平均値だけで計画すると、遅延リスクやサービス品質低下を見落とす可能性がある。",
        ],
        "focus": ["不確実性の発生源を、需要・リソース・環境に分けて説明できる。"],
        "questions": [
            ("Same-Day配送における三種類の不確実性を例示せよ。", "需要不確実性は、注文がいつ・どこで・どれだけ発生するかである。リソース不確実性は、ドライバーの出勤、車両故障、バッテリー残量、スキルである。環境不確実性は、交通、駐車、天候、道路工事、ネットワーク障害である。"),
            ("平均値だけを使う計画の危険性を説明せよ。", "平均旅行時間では、遅延の裾の長さや極端な渋滞を見落とす。全アークで平均を使うと、各区間では小さな誤差でも全体ツアーでは大きな遅延になることがある。サービス時間や交通が右裾の長い分布を持つ場合、平均値だけでは信頼性を評価できない。"),
        ],
    },
    "modeling_uncertainty": {
        "explain": [
            "Deterministic model は、すべての入力値が既知で固定されているとみなす。簡単で解きやすいが、不確実性を無視する。",
            "Stochastic model は、実現値の確率分布または確率を仮定する。期待値、分散、サンプリング、確率制約などを使えるが、十分なデータと妥当な分布仮定が必要である。",
            "Quasi-stochastic model は、確率は分からないが、あり得るシナリオや区間は分かる場合に使う。What-if分析、区間旅行時間、Hurwicz基準、minmax regret が典型である。",
        ],
        "focus": ["stochastic と quasi-stochastic の違いを、確率が分かるかどうかで説明する。"],
        "questions": [
            ("stochastic と quasi-stochastic を比較せよ。", "stochastic では確率分布や各シナリオの確率が既知または推定可能であるため、期待値最小化やMonte Carlo samplingを使える。quasi-stochastic では確率が未知で、シナリオ集合や区間だけを用いる。したがって、最悪ケース、Hurwicz、minmax regret のような基準で決定する。"),
            ("いつ quasi-stochastic model が有用か。", "過去データが少ない、新しいサービスで履歴がない、道路工事などで環境が変わった、確率分布を置くには不確実性が大きすぎる場合である。このとき、区間や代表シナリオを用いることで、完全な確率分布なしに頑健な意思決定ができる。"),
        ],
    },
    "probability_distribution": {
        "explain": [
            "確率分布は、不確実な変数がどの値をどの程度取りやすいかを表す。旅行時間、サービス時間、需要量、注文間隔などを表現できる。",
            "期待値は平均的な値、分散と標準偏差はばらつき、変動係数は平均に対する相対的なばらつきを表す。中央値・分位点は、遅延リスクやサービスレベルを説明する際に重要である。",
            "分布の決定では、理論分布を仮定する場合と、データに分布をフィットする場合がある。フィットでは、ヒストグラム、パラメータ推定、適合度検定、ブートストラップによる妥当性確認を行う。",
        ],
        "focus": ["期待値・分散・標準偏差・分位点を、意思決定上の意味と結びつける。"],
        "questions": [
            ("旅行時間分布をデータから決める手順を説明せよ。", "観測された旅行時間を集め、外れ値を確認し、ヒストグラムや密度を描く。正規分布、ガンマ分布、対数正規分布など候補分布を選び、平均・分散などのパラメータを推定する。可視化やKolmogorov-Smirnov検定で適合度を確認し、必要ならブートストラップで推定の安定性を検査する。"),
            ("サービス時間分布の典型的な特徴を述べよ。", "サービス時間は負にならないため非負である。多くのケースでは短い時間に集中し、例外的に長い作業があるため右裾が長い。平均だけでなく分散や上位分位点が重要で、例えば90%分位点は遅延リスクを評価するために使える。"),
        ],
    },
    "stochastic_decision": {
        "explain": [
            "確率的意思決定では、決定 x を選んだ後にランダム情報 xi が実現する。費用 F(x,xi) は事前には確定していないため、期待費用 E[F(x,xi)] やリスクを含む基準を最適化する。",
            "Monte Carlo Sampling では、分布から複数のシナリオを発生させ、期待値を標本平均で近似する。サンプル数が多いほど安定しやすいが、計算量も増える。",
            "期待値-分散原理では、平均性能だけでなくばらつきも評価する。リスク回避的なら分散の大きい解を避け、リスク中立なら期待値中心で判断する。",
        ],
        "focus": ["決定後にランダム情報が実現するため、F(x,xi)ではなく期待値やリスク基準を最適化する。"],
        "questions": [
            ("なぜ F(x,xi) を直接最適化できないのか。", "xi は意思決定時点ではまだ実現していないランダム情報である。したがって、特定の実現値に対する費用 F(x,xi) は事前に確定していない。意思決定時点では、分布に基づく期待値、分散、分位点、サンプリング平均などを使って x を評価する必要がある。"),
            ("Monte Carlo Sampling の役割を説明せよ。", "確率分布から多数のシナリオを発生させ、それぞれで費用を計算することで、期待費用を標本平均で近似する。解析的に期待値を計算できない場合でも、サンプルに基づいて近似的な意思決定が可能になる。"),
        ],
    },
    "quasi_stochastic": {
        "explain": [
            "Hurwicz基準は、最悪ケースと最良ケースを楽観係数 lambda で重み付けする。lambda が大きいほど楽観的、0に近いほど悲観的である。",
            "Minmax regret は、選んだ解が各シナリオで、そのシナリオの完全情報最適解に比べてどれだけ悪いかを regret として測る。各解の最大 regret を計算し、それが最小の解を選ぶ。",
            "regret の直感は『後からそのシナリオが実現したと分かった時に、別の解を選んでおけばよかったという損失を抑える』ことである。平均的な効率だけでなく、後悔の大きい極端な失敗を避ける。",
        ],
        "focus": ["Hurwicz は楽観/悲観の重み付け、minmax regret は最悪の後悔を最小化する基準。"],
        "questions": [
            ("minmax regret を言葉で説明せよ。", "各シナリオについて、選んだ解の費用と、そのシナリオを事前に知っていた場合の最良費用との差を regret とする。候補解ごとに最も大きい regret を求め、その最大 regret が最も小さい解を選ぶ。目的は、どのシナリオが実現しても『別の解なら大幅に良かった』という状況を抑えることである。"),
            ("Hurwicz基準とminmax regretの違いを述べよ。", "Hurwicz基準は最良ケースと最悪ケースの性能そのものを重み付けして評価する。minmax regret は性能そのものではなく、各シナリオの完全情報最適解との差、つまり後悔を評価する。前者は楽観度を直接反映し、後者はシナリオ間での相対的な失敗を抑える。"),
        ],
    },
    "robust_vrp": {
        "explain": [
            "都市物流では、顧客期待、渋滞、狭い配送時間、車両数制約により、単に平均旅行時間を最小化するだけでは不十分である。",
            "区間旅行時間 [l,u] は、下限と上限で不確実性を表す準確率的情報モデルである。十分な分布推定が難しい場合でも、5%分位点や95%分位点を使って現実的な範囲を作れる。",
            "ロバストルーティングでは、平均的に短いルートだけでなく、複数の交通シナリオで大きく崩れにくいルートを選ぶ。効率性とサービス信頼性のトレードオフが中心である。",
        ],
        "focus": ["都市物流では、平均時間最小化・最悪ケース・regret の違いを説明できる。"],
        "questions": [
            ("都市物流で区間旅行時間が有用な理由を説明せよ。", "都市交通では旅行時間のばらつきが大きく、十分な確率分布を推定できない道路や時間帯もある。区間旅行時間なら、下限・上限で不確実性の範囲を表せるため、少ないデータや専門知識でもロバストな計画に使える。"),
            ("効率性と信頼性のトレードオフを説明せよ。", "平均旅行時間だけを最小化すると短いが遅延に弱いルートになる場合がある。最悪ケースだけを重視すると非常に安全だが過度に長いルートになる場合がある。regretやロバスト基準は、その中間で、複数の交通状況に対して大きく悪化しにくいルートを選ぼうとする。"),
        ],
    },
}

# Backward topic aliases from previous generator.
ALIASES = {
    "uncertainty_types": "modeling_uncertainty",
    "time_dependent": "time_dependent_travel",
}

# ---------------------------------------------------------------------------
# Dedicated exam-practice pages.  Each is inserted once, not repeated on slide
# pages.  Questions are provided as structured summaries close to the original
# prompt, followed by full-score answers and explanation.
# ---------------------------------------------------------------------------
Exam = Dict[str, Any]
EXAM_PAGES: Dict[str, List[Exam]] = {
    "l01_after_17": [
        {
            "title": "Business Analytics とDDDMの全体像",
            "questions": [
                {
                    "ref": "WS23/24 Aufgabe 1 [6 Punkte]",
                    "problem": "Business Analytics が用いる三つの分野を挙げ、各二分野の交差領域も説明する問題。合計で三つの分野と三つの交差領域が問われる。",
                    "answer": [
                        "Business Analytics は、Operations Research、Statistics、Computer Science/Information Systems の三分野を組み合わせる。Operations Research は、目的関数、制約、決定変数、実行可能解、最適化アルゴリズムを扱い、どの行動を選ぶべきかを定式化する。Statistics は、不確実なデータから分布、期待値、分散、予測、推定を扱い、観測値の背後にある規則性や不確実性を表す。Computer Science/Information Systems は、データの保存、処理、アルゴリズム実装、情報システムへの統合を扱う。",
                        "Operations Research と Statistics の交差では、確率的最適化や不確実性下の意思決定が中心になる。Statistics と Computer Science の交差では、データマイニング、機械学習、データ処理が中心になる。Computer Science と Operations Research の交差では、最適化アルゴリズム、計算複雑性、意思決定支援システムが中心になる。Business Analytics はこれらを統合し、データから実行可能な意思決定を導く。",
                    ],
                    "example": "配送計画では、Statistics が旅行時間分布を推定し、Computer Science がGPS・注文データを処理し、Operations Research が車両ルートを最適化する。三つのうち一つでも欠けると、現実データに基づく実行可能な意思決定にならない。",
                    "rubric": ["三分野を正しく列挙", "三つの二分野交差を説明", "Business Analytics が統合領域であることを明示", "配送などの具体例で説明"],
                },
                {
                    "ref": "WS23/24 Aufgabe 2 [5 Punkte]",
                    "problem": "Real-World Problem と Decision Model がどのように関係し、どの概念的構成要素とデータフローで結ばれるかを説明する問題。",
                    "answer": [
                        "現実問題は直接そのまま意思決定モデルにはならない。まず Real-World で行動が実行され、その結果として状態やデータが観測される。Aggregation は、観測データを情報モデルの次元へ変換する。Information Model は、現実を意思決定に必要な形へ圧縮した表現であり、例えば顧客、道路、旅行時間、需要などを含む。Decision Model は、この情報モデルを使い、決定空間、目的関数、制約、評価基準を定義する。Implementation または Disaggregation は、モデルの解を現実の行動へ戻す。",
                        "データフローは、Real-World から Aggregation を通じて Information Model へ入り、Information Model が Decision Model の入力になる。Decision Model の解は Implementation により Real-World へ戻る。実装結果を観測することで、仮説、情報モデル、意思決定モデルを更新する。したがって、関係は一方向ではなく循環である。",
                    ],
                    "example": "配送では、GPSと注文データを集約して顧客集合と旅行時間行列を作る。これが情報モデルである。そこからTSP/VRPを作り、訪問順序を決める。訪問順序をドライバーのナビに変換して実行し、遅延や実走時間を再び観測してモデルを改善する。",
                    "rubric": ["Real-World, Aggregation, Information Model, Decision Model, Implementationを全て説明", "データフローを正しい順序で説明", "ループとして説明", "具体例を含める"],
                },
            ],
        }
    ],
    "l02_after_8": [
        {
            "title": "情報モデル・意思決定モデル・Business Analyticsプロセス",
            "questions": [
                {
                    "ref": "SS24 Aufgabe 1a [8 Punkte]",
                    "problem": "Information Model, Decision Model, Aggregation, Disaggregation の機能を説明する問題。",
                    "answer": [
                        "Aggregation は、現実世界から得られる詳細で雑多なデータを、情報モデルで扱える抽象度へ変換する機能である。例えば、GPS点列を道路セグメントの速度に変換し、住所を顧客ノードに変換し、過去走行記録を時間帯別旅行時間に集約する。",
                        "Information Model は、意思決定に必要な情報を構造化した表現である。現実のすべてを含むのではなく、目的に関連する顧客、デポ、道路、旅行時間、需要、時間帯などを圧縮して表す。Decision Model は、情報モデルを入力として、どの決定を選べるか、どの制約を守るか、何を最小化または最大化するかを定義する。TSPなら、アーク選択変数、訪問制約、部分巡回除去制約、総旅行時間最小化が該当する。",
                        "Disaggregation は、モデルの解を現実の実行可能な指示へ戻す機能である。例えば、モデル上のノード番号列を住所・道路ルート・ドライバー指示に変換する。したがって、Aggregation は現実からモデルへ、Disaggregation はモデルから現実への橋である。",
                    ],
                    "example": "顧客A,B,Cへの配送では、住所と地図から旅行時間行列を作るのがAggregation、旅行時間行列と顧客集合がInformation Model、最短訪問順を求めるTSPがDecision Model、A->C->Bという解を実際のナビにするのがDisaggregationである。",
                    "rubric": ["四概念をそれぞれ定義", "モデル入力・出力の方向を明示", "配送/TSP例で対応付け", "現実とモデルのループを説明"],
                },
                {
                    "ref": "WS23/24 Aufgabe 3 [10 Punkte]",
                    "problem": "配送車両フリートの業務的ツアープランニングを例に、Real-World, Aggregation, Information Model, Decision Model, Implementation の構成要素とデータフローを説明する問題。",
                    "answer": [
                        "Real-World は、配送センター、顧客住所、道路ネットワーク、配送車両、ドライバー、交通状況である。ここで実際の配送が行われ、走行時間や遅延などが観測される。Aggregation では、顧客住所をノードにし、道路地図やGPSから顧客間旅行時間を計算し、必要なら時間帯別旅行時間行列を作る。",
                        "Information Model は、デポ、顧客集合、車両集合、顧客需要、旅行時間または距離行列、時間帯などから成る。Decision Model は、どの車両がどの顧客をどの順序で訪問するかを決めるVRP/TSPである。決定変数はアーク使用や車両割当を表し、制約は各顧客を一度訪問すること、車両容量、勤務時間、時間窓などである。目的関数は総旅行時間、車両数、遅延、コストの最小化である。",
                        "Implementation は、得られたルートをドライバーの配送順序、ナビゲーション、出発時刻、作業指示に変換することである。実装後の走行時間や遅延は再び観測され、旅行時間モデルや制約仮説の改善に使われる。",
                    ],
                    "example": "例えば、モデルが『車両1: Depot-A-C-Depot、車両2: Depot-B-D-Depot』を出した場合、Implementationでは実住所、積載順、ナビ経路、時間窓をドライバーに渡す。もしA-C間が常に遅れるなら、AggregationやInformation Modelを更新する。",
                    "rubric": ["配送例のReal-Worldを具体化", "各構成要素の対応付け", "決定変数・制約・目的関数を説明", "実装とフィードバックを説明"],
                },
            ],
        }
    ],
    "l02_after_17": [
        {
            "title": "Floating Car Data と旅行時間情報モデル",
            "questions": [
                {
                    "ref": "WS22/23 Aufgabe 4 [8 Punkte]",
                    "problem": "交通観測データから、時間帯別の平均旅行時間または旅行時間行列を構築する手順を説明する問題。",
                    "answer": [
                        "まず、車両から時刻付き位置データ、速度、方向などを収集する。次に、位置データを道路ネットワーク上のリンクに対応付ける map matching を行う。これにより、各観測がどの道路セグメント・どの方向・どの時刻に属するかが分かる。",
                        "その後、エラー、外れ値、停止中データ、GPSのずれを除去または補正する。観測を時間帯と道路セグメントごとにグループ化し、平均速度または平均旅行時間を計算する。観測数が少ないセグメントや時間帯では、時間帯をまとめる、類似道路で補完する、空間的・時間的な一般化を使う。",
                        "最後に、顧客間の経路を道路セグメント列として求め、各セグメントの時間帯別旅行時間を足し合わせて、顧客間の時間依存旅行時間行列を作る。この情報モデルは、時間依存TSP/VRPの意思決定モデルの入力になる。",
                    ],
                    "example": "タクシーFCDが1分ごとに位置を送る場合、Hildesheimer Strasseの月曜8時台に属する観測を集め、平均速度を出す。その速度からリンク旅行時間を求め、顧客AからBへ行く経路上のリンク旅行時間を合計してA-Bの8時台旅行時間を作る。",
                    "rubric": ["データ収集", "map matching", "外れ値処理", "時間帯・セグメント別集約", "顧客間行列への変換", "観測不足への対応"],
                },
                {
                    "ref": "SS24 Aufgabe 1b [4 Punkte]",
                    "problem": "旅行時間の情報モデルを二つ例示し、なぜ常により詳細なモデルを選ばないのかを説明する問題。",
                    "answer": [
                        "旅行時間情報モデルの例として、第一に単一の平均旅行時間行列がある。これは各顧客間の旅行時間を一つの値で表す。第二に時間帯別旅行時間行列がある。これは朝、昼、夕方などの時間帯ごとに異なる旅行時間を持つ。さらに詳細には、道路セグメントごとの連続的な時間依存関数も考えられる。",
                        "常に詳細なモデルを選ばない理由は、データ量、信頼性、計算複雑性、解釈可能性にコストがあるからである。時間帯や道路を細かく分けるほど、各セルの観測数が減り、平均値が不安定になる。また、意思決定モデルの変数・制約が増え、解くのが難しくなる。したがって、目的に十分な粒度を選ぶ必要がある。",
                    ],
                    "example": "夜間配送が中心なら、朝夕ラッシュを細かく分けたモデルは不要かもしれない。一方、Same-Day配送で夕方ラッシュに多く走るなら、平均行列では遅延を過小評価するため、時間帯別モデルが有用である。",
                    "rubric": ["二つ以上の情報モデルを提示", "詳細モデルの利点", "データ量・信頼性・計算量の欠点", "目的に応じた粒度選択"],
                },
            ],
        }
    ],
    "l02_after_39": [
        {
            "title": "TSP、時間依存TSP、ヒューリスティック",
            "questions": [
                {
                    "ref": "WS22/23 Aufgabe 1 [7 Punkte]",
                    "problem": "TSPの数理最適化モデルをスケッチし、時間次元をTSPモデルでどのように考慮するかを説明する問題。",
                    "answer": [
                        "標準TSPでは、ノード集合を顧客とデポ、アーク集合を顧客間移動として定義する。各アーク (i,j) には距離または旅行時間 d_{ij} がある。二値決定変数 x_{ij} は、i から j へ直接移動するなら1、そうでなければ0である。目的関数は、sum_i sum_j d_{ij} x_{ij} を最小化する。制約として、各顧客にちょうど一度入る、各顧客からちょうど一度出る、部分巡回を排除する制約が必要である。",
                        "時間次元を考慮する場合、旅行時間 d_{ij} は定数ではなく、出発時刻 t に依存する d_{ij}(t) になる。さらに、顧客 i への到着時刻、サービス開始時刻、顧客 j への出発時刻などの時間変数が必要になる。アークを選ぶかどうかだけでなく、いつそのアークを通るかが重要になるため、x_{ij}(t) のような時刻依存決定変数や時間伝播制約が必要になる。",
                    ],
                    "example": "A->B が朝8時なら20分、昼12時なら10分なら、同じ訪問順でも出発時刻により目的関数値が変わる。Aを先に訪問するか後に訪問するかが、後続の全旅行時間に影響する。",
                    "rubric": ["変数 x_ij", "目的関数", "入次数・出次数制約", "部分巡回除去", "時間依存旅行時間 d_ij(t)", "到着時刻/出発時刻の伝播"],
                },
                {
                    "ref": "WS23/24 Aufgabe 5 [7 Punkte]",
                    "problem": "Cheapest Insertion が時間依存旅行時間を持つ場合になぜ難しくなるかを説明する問題。",
                    "answer": [
                        "Cheapest Insertion は、未訪問顧客を現在のツアーのどの位置へ挿入すると追加コストが最小になるかを計算し、その最安挿入を繰り返すヒューリスティックである。静的TSPでは、追加コストは d_{i,k}+d_{k,j}-d_{i,j} のように局所的に計算できる。",
                        "時間依存旅行時間では、顧客 k を i と j の間に挿入すると、j 以降の到着時刻が変わる。旅行時間が出発時刻に依存するため、後続アークの旅行時間もすべて変わり得る。したがって、局所的な追加コストだけでは真の影響を測れず、ツアー全体の時刻を再計算しなければならない。",
                    ],
                    "example": "A-Bの間にCを入れると、Bへの到着が15分遅れ、その結果B-Dを夕方ラッシュ時に走ることになるかもしれない。この場合、Cの挿入自体は短く見えても、後続アークが大きく悪化する。",
                    "rubric": ["Cheapest Insertionの基本説明", "静的追加コスト", "後続到着時刻への波及", "時間依存コストの再評価", "局所貪欲法の限界"],
                },
            ],
        }
    ],
    "l03_after_20": [
        {
            "title": "不確実性の種類とモデリング",
            "questions": [
                {
                    "ref": "SS24 Aufgabe 2a [3 Punkte]",
                    "problem": "Same-Day配送における不確実性を、需要、リソース、環境の三カテゴリについて一例ずつ挙げる問題。",
                    "answer": [
                        "需要の不確実性として、注文がいつ発生するか、どの地域から発生するか、注文量がどれくらいかがある。リソースの不確実性として、ドライバーの利用可能性、車両故障、バッテリー残量、積載容量、ドライバーのスキルがある。環境の不確実性として、交通渋滞、駐車可能性、天候、道路工事、事故、通信ネットワーク障害がある。",
                        "満点を取るには、単に三語を列挙するのではなく、それぞれが配送計画へどう影響するかを説明する。需要は訪問先と負荷を変え、リソースは実行可能な割当を変え、環境は旅行時間や遅延リスクを変える。",
                    ],
                    "example": "夕方に予想外の大量注文が入ると需要不確実性、登録ドライバーがアプリを切って稼働しないとリソース不確実性、突然の道路閉鎖で到着時間が変わると環境不確実性である。",
                    "rubric": ["三カテゴリをすべて挙げる", "各カテゴリに具体例", "計画への影響を説明"],
                },
                {
                    "ref": "WS24/25 Aufgabe 3 [12 Punkte]",
                    "problem": "stochastic と quasi-stochastic の違い、および各手法の考え方を説明する問題。",
                    "answer": [
                        "stochastic model では、不確実な実現値について確率分布またはシナリオ確率が既知または推定可能である。したがって、期待値、分散、確率制約、Monte Carlo sampling などを用いて意思決定を評価できる。例として、旅行時間がガンマ分布に従うと仮定し、その期待値や分位点を使ってルートを評価する場合がある。",
                        "quasi-stochastic model では、確率分布は分からないが、起こり得るシナリオや区間は分かる。例えば、旅行時間が [l,u] の範囲にあることだけが分かる場合である。このとき、Hurwicz基準、最悪ケース最適化、minmax regret、What-if分析を使う。",
                        "両者の違いは、確率を使って平均的・分布的に評価できるか、確率なしで代表シナリオや区間に対して頑健に評価するかである。データが十分なら stochastic、データが少ない・分布仮定が難しいなら quasi-stochastic が適する。",
                    ],
                    "example": "旅行時間の過去観測が大量にあり、分布をフィットできるなら stochastic。新しい道路工事で過去データがなく、専門家が『10分から25分』という範囲だけを与えるなら quasi-stochastic。",
                    "rubric": ["確率既知/未知の違い", "stochastic手法", "quasi-stochastic手法", "適用条件", "具体例"],
                },
            ],
        }
    ],
    "l03_after_29": [
        {
            "title": "不確実性下の意思決定: expectation, Hurwicz, regret",
            "questions": [
                {
                    "ref": "SS24 Aufgabe 2b [3 Punkte]",
                    "problem": "修理サービスや在宅介護の顧客サービス時間について、確率密度関数の典型的性質を三つ説明する問題。",
                    "answer": [
                        "第一に、サービス時間は負にならないため、分布の定義域は0以上である。第二に、多くのサービスは標準的な短い所要時間に集中するが、例外的に長い作業が起こるため右裾が長くなりやすい。第三に、サービス品質や遅延リスクを評価するには平均だけでは不十分であり、分散、標準偏差、分位点、特に上位分位点が重要である。",
                        "試験では、単に『正規分布』など分布名を書くよりも、なぜ非負・右裾・ばらつきが意思決定に影響するかを説明する方がよい。サービス時間の上振れは次顧客への遅延を引き起こし、ツアー全体に伝播する。",
                    ],
                    "example": "家電修理では多くの訪問は20分で終わるが、故障が複雑な場合は90分かかる。この長い右裾を無視して平均30分だけで計画すると、後続訪問が連鎖的に遅れる。",
                    "rubric": ["非負性", "右裾/歪み", "平均だけでなく分散・分位点", "計画への影響"],
                },
                {
                    "ref": "SS23 Aufgabe 3 [6 Punkte] / WS24/25 Aufgabe 1 [10 Punkte]",
                    "problem": "区間旅行時間、楽観値・悲観値、regret に基づき、最大の後悔を抑える意思決定の論理を説明する問題。",
                    "answer": [
                        "区間旅行時間では、各アークについて楽観的旅行時間 l_{ij} と悲観的旅行時間 u_{ij} が分かるが、その確率は分からない。この場合、平均値で最適化するのではなく、複数の可能な交通状態に対して解を評価する。regret とは、あるシナリオが実現したときに、自分が選んだ解の費用と、そのシナリオを事前に知っていた場合の最適解の費用との差である。",
                        "minmax regret では、各候補ルートについて全シナリオの regret を計算し、その最大値を求める。そして最大 regret が最小になるルートを選ぶ。これにより、どのシナリオが実現しても『別のルートなら大幅に良かった』という最悪の後悔を小さくできる。",
                        "この基準は、最良ケースだけを見てリスクを無視することも、最悪ケースだけを見て過度に保守的になることも避ける。都市物流では、効率性とサービス信頼性のバランスを取るために有用である。",
                    ],
                    "example": "ルートAは通常なら短いが、渋滞時に大きく悪化する。ルートBは通常少し長いが、どの状態でも安定している。minmax regretでは、シナリオごとに完全情報最適ルートとの差を見て、最悪の差が小さいBを選ぶ可能性がある。",
                    "rubric": ["regretの定義", "完全情報最適解との差", "最大regretを最小化", "平均/最悪ケースとの違い", "物流例"],
                },
            ],
        }
    ],
    "l03_after_40": [
        {
            "title": "ロバスト都市物流と区間旅行時間",
            "questions": [
                {
                    "ref": "WS22/23 Aufgabe 5 [6 Punkte]",
                    "problem": "旅行時間不確実性を確率的または準確率的にモデル化し、ロバストな解が何を意味するかを説明する問題。",
                    "answer": [
                        "確率的モデルでは、旅行時間の確率分布やシナリオ確率を仮定し、期待旅行時間、分散、分位点、サンプリングに基づいてルートを評価する。準確率的モデルでは、確率は分からないが、区間やシナリオ集合を使って不確実性を表す。区間旅行時間 [l_{ij},u_{ij}] はその典型である。",
                        "ロバストな解とは、単一の平均ケースで最も短いだけでなく、複数のあり得る交通状態で大きく性能が崩れにくい解である。例えば、平均旅行時間最小ルートはラッシュ時に大きく遅れる可能性がある。一方、ロバストルートは少し長くても、遅延リスクやサービス品質低下を抑える。",
                        "都市物流では、効率性と信頼性のトレードオフが重要である。最悪ケースだけに最適化すると過度に保守的になり、平均ケースだけではサービス違反が増える。regretや区間ベースの基準は、その中間を狙う。",
                    ],
                    "example": "Aルートは平均45分だが渋滞時90分、Bルートは平均55分だが渋滞時65分なら、平均だけならA、ロバスト性ならBが有利になる場合がある。配送時間約束がある場合、Bの方が顧客サービスに適する。",
                    "rubric": ["確率的/準確率的の違い", "区間旅行時間", "ロバスト解の定義", "効率性と信頼性のトレードオフ", "具体例"],
                }
            ],
        }
    ],
}

INSERT_AFTER: Dict[str, Dict[int, List[Exam]]] = {
    "l01": {17: EXAM_PAGES["l01_after_17"]},
    "l02": {8: EXAM_PAGES["l02_after_8"], 17: EXAM_PAGES["l02_after_17"], 39: EXAM_PAGES["l02_after_39"]},
    "l03": {20: EXAM_PAGES["l03_after_20"], 29: EXAM_PAGES["l03_after_29"], 40: EXAM_PAGES["l03_after_40"]},
}


def tex_escape(s: str) -> str:
    repl = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
        "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in s)


def tex_itemize(items: Sequence[Item]) -> str:
    out = [r"\begin{itemize}"]
    for it in items:
        if isinstance(it, tuple):
            out.append(r"\item " + tex_escape(it[0]))
            out.append(tex_itemize(it[1]))
        else:
            out.append(r"\item " + tex_escape(it))
    out.append(r"\end{itemize}")
    return "\n".join(out)


def normalize_topic(topic: str) -> str:
    return ALIASES.get(topic, topic)


def topic_block(topic: str) -> Dict[str, Any]:
    return TOPIC_NOTES.get(normalize_topic(topic), TOPIC_NOTES["dddm_intro"])


def compact_paragraphs(pars: Sequence[str], max_n: int = 3) -> str:
    return "\n\n".join(tex_escape(p) + r"\par" for p in pars[:max_n])


def write_slide_page(lec: str, page: int, slide: Dict[str, Any]) -> str:
    info = LECTURES[lec]
    pdf_path = f"../Materials/2026/{info['pdf']}"
    topic = normalize_topic(slide.get("topic", "admin"))
    block = topic_block(topic)
    title = slide.get("title", f"Slide {page}")
    lines: List[str] = []
    lines.append(r"\clearpage")
    lines.append(r"\SlideHeader{" + tex_escape(info["title"]) + "}{" + f"{page:03d}" + "}{" + tex_escape(title) + "}")
    lines.append(r"\SlideImage{" + str(page) + "}{" + pdf_path + "}")
    if topic == "admin":
        lines.append(r"\begin{multicols}{2}\scriptsize\raggedcolumns")
    else:
        lines.append(r"\begin{multicols}{2}\footnotesize\raggedcolumns")
    lines.append(r"\NoteSection{日本語訳}")
    lines.append(tex_itemize(slide.get("translation", [])))
    if block.get("explain"):
        lines.append(r"\NoteSection{解説}")
        lines.append(compact_paragraphs(block["explain"], 3))
    if block.get("focus"):
        lines.append(r"\NoteSection{試験対策ポイント}")
        lines.append(tex_itemize(block["focus"][:2]))
    if block.get("questions"):
        lines.append(r"\NoteSection{確認問題と解答}")
        lines.append(r"\begin{enumerate}")
        for q, a in block["questions"][:2]:
            lines.append(r"\item \textbf{" + tex_escape(q) + r"}\\" + tex_escape(a))
        lines.append(r"\end{enumerate}")
    lines.append(r"\end{multicols}")
    return "\n".join(lines) + "\n"


def write_exam_pages(exam_group: Exam) -> str:
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
    (SECTIONS / f"{info['stem']}_v3.tex").write_text("\n".join(out), encoding="utf-8")


def write_main(lec: str) -> None:
    info = LECTURES[lec]
    main = rf"""
\documentclass[a4paper,10pt]{{article}}
\usepackage[margin=7mm]{{geometry}}
\usepackage{{fontspec}}
\usepackage{{xeCJK}}
\usepackage{{graphicx}}
\usepackage{{multicol}}
\usepackage{{amsmath,amssymb}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}
\usepackage{{titlesec}}
\setmainfont{{Noto Sans}}
\setsansfont{{Noto Sans}}
\setCJKmainfont{{Noto Sans CJK JP}}
\definecolor{{TUBSred}}{{HTML}}{{BE1E3C}}
\definecolor{{lightgray}}{{HTML}}{{F4F4F4}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{3.2pt}}
\setlength{{\columnsep}}{{5mm}}
\setlist[itemize]{{leftmargin=1.15em,itemsep=1.2pt,topsep=1.5pt,parsep=0pt}}
\setlist[enumerate]{{leftmargin=1.35em,itemsep=2pt,topsep=1.5pt,parsep=0pt}}
\hypersetup{{colorlinks=true,linkcolor=blue,urlcolor=blue}}
\titleformat{{\section}}{{\Large\bfseries\color{{TUBSred}}}}{{}}{{0pt}}{{}}
\newcommand{{\SlideHeader}}[3]{{%
  \noindent{{\large\bfseries #1 / Slide #2: #3}}\hfill {{\scriptsize review v3}}\par
  \vspace{{0.8mm}}\hrule\vspace{{1.0mm}}
}}
\newcommand{{\SlideImage}}[2]{{%
  \noindent\makebox[\textwidth][c]{{\includegraphics[page=#1,width=0.96\textwidth,height=0.31\textheight,keepaspectratio]{{#2}}}}\par
  \vspace{{1.0mm}}
}}
\newcommand{{\NoteSection}}[1]{{%
  \vspace{{1.8mm}}\noindent{{\normalsize\bfseries\color{{TUBSred}}#1}}\par\vspace{{0.8mm}}
}}
\newcommand{{\ExamHeader}}[1]{{%
  \noindent{{\Large\bfseries\color{{TUBSred}}過去問演習: #1}}\hfill {{\scriptsize review v3}}\par
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
{{\Large {tex_escape(info['title'])} - 日本語訳・解説・試験対策ノート\par}}
\vspace{{1cm}}
\begin{{minipage}}{{0.88\textwidth}}
このPDFは review v3 です。各スライドページは、元スライド、日本語訳、解説、確認問題を原則1ページに収めています。過去問は重複を避け、必要知識を説明した後に独立した演習ページとして配置しています。過去問ページには、問題内容、満点答案、具体例、採点要素を記載しています。
\end{{minipage}}
\vfill
{{\large Materials/2026}}
\end{{titlepage}}
\tableofcontents
\clearpage
\input{{sections/{info['stem']}_v3.tex}}
\end{{document}}
"""
    (LATEX / f"main_{info['stem']}_v3.tex").write_text(main, encoding="utf-8")


def compile_pdf(lec: str) -> None:
    info = LECTURES[lec]
    tex = f"main_{info['stem']}_v3.tex"
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex], cwd=LATEX, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex], cwd=LATEX, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_name = info["out"]
    pdf = LATEX / f"main_{info['stem']}_v3.pdf"
    target = OUTPUT / out_name
    target.write_bytes(pdf.read_bytes())
    # Also write top-level copies for quick download.
    (ROOT.parent / out_name).write_bytes(pdf.read_bytes()) if ROOT.parent.exists() else None


def write_markdown_note(lec: str) -> None:
    # A compact semantic log of the changed design; detailed content is in TeX.
    info = LECTURES[lec]
    lines = [f"# {info['title']} - review v3", "", "## 設計方針", "", "- スライドページには過去問を繰り返し配置しない。", "- スライドページは、日本語訳、解説、試験対策ポイント、確認問題と解答で構成する。", "- 過去問は関連知識を説明した後に独立ページとして配置する。", "- 過去問ページには、問題内容、満点答案、具体例、採点要素を含める。", ""]
    NOTES.mkdir(parents=True, exist_ok=True)
    (NOTES / f"{info['stem']}_v3.md").write_text("\n".join(lines), encoding="utf-8")


def write_revision_doc() -> None:
    doc = """# Review v3 formatting revision

この版では、過去問が複数スライドに重複して現れる問題を修正した。

## 変更点

- 各回のPDFを分けて出力する。
- スライドページは原則1ページ完結とし、元スライド、日本語訳、解説、確認問題のみを置く。
- 過去問は、必要知識が説明された後に独立ページとして配置する。
- 過去問ページには、問題内容、満点答案、具体例による解説、採点要素を含める。
- 日本語訳はスライドの箇条書き構造を維持し、訳だけを書く。
- 解説と確認問題は、情報学学士を終えた初学者が試験答案を作れる水準を目標に拡充した。

## 出力ファイル

- output/dddm_l01_overview_jp_exam_notes.pdf
- output/dddm_l02_information_decision_modeling_jp_exam_notes.pdf
- output/dddm_l03_uncertainty_jp_exam_notes.pdf

## 生成スクリプト

`scripts/generate_l01_l03_v3_notes.py`
"""
    (ROOT / "docs" / "08_feedback_revision_v3.md").write_text(doc, encoding="utf-8")


def main() -> None:
    write_revision_doc()
    for lec in ["l01", "l02", "l03"]:
        write_section(lec)
        write_main(lec)
        write_markdown_note(lec)
        compile_pdf(lec)
    print("Generated v3 lecture notes.")


if __name__ == "__main__":
    main()
