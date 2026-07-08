#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate review v5 Japanese exam notes for all DDDM lecture materials.

v5 implements the latest output management policy:
- compile every lecture separately;
- write current PDFs only into output/latest;
- move old PDF artifacts into output/history/<timestamp> before a new run;
- keep generated PDFs out of the latex/ source folder;
- add detailed, example-rich explanations and page-specific check questions.

The semantic conversion from slide text to Japanese notes remains intentionally
transparent and review-oriented. The generated Markdown/TeX files are designed to
be edited by ChatGPT/humans after review.
"""
from __future__ import annotations

import csv
import datetime as dt
import importlib.util
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
MAT = ROOT / "Materials" / "2026"
LATEX = ROOT / "latex"
SECTIONS = LATEX / "sections"
OUTPUT = ROOT / "output"
LATEST = OUTPUT / "latest"
HISTORY = OUTPUT / "history"
NOTES = ROOT / "notes"
DOCS = ROOT / "docs"
EXTRACT = ROOT / "_extracted_text_all"

LECTURES: List[Dict[str, Any]] = [
    {"id":"l01", "no":1, "pdf":"3DM_01_Overview_SS26.pdf", "stem":"3dm_01_overview_ss26", "title":"Lecture 1 - Overview", "out":"dddm_l01_overview_jp_exam_notes.pdf"},
    {"id":"l02", "no":2, "pdf":"3DM_02_Information-and-Decision-Modeling_SS26.pdf", "stem":"3dm_02_information_decision_modeling_ss26", "title":"Lecture 2 - Information and Decision Modeling", "out":"dddm_l02_information_decision_modeling_jp_exam_notes.pdf"},
    {"id":"l03", "no":3, "pdf":"3DM_03_Uncertainty_SS26.pdf", "stem":"3dm_03_uncertainty_ss26", "title":"Lecture 3 - Uncertainty", "out":"dddm_l03_uncertainty_jp_exam_notes.pdf"},
    {"id":"l04", "no":4, "pdf":"3DM_04_Dynamism_SS26.pdf", "stem":"3dm_04_dynamism_ss26", "title":"Lecture 4 - Dynamism", "out":"dddm_l04_dynamism_jp_exam_notes.pdf"},
    {"id":"l05", "no":5, "pdf":"3DM_05_MDP_SS26.pdf", "stem":"3dm_05_mdp_ss26", "title":"Lecture 5 - Markov Decision Process", "out":"dddm_l05_mdp_jp_exam_notes.pdf"},
    {"id":"l06", "no":6, "pdf":"3DM_06_ADP_SS26.pdf", "stem":"3dm_06_adp_ss26", "title":"Lecture 6 - Approximate Dynamic Programming", "out":"dddm_l06_adp_jp_exam_notes.pdf"},
    {"id":"l07", "no":7, "pdf":"3DM_07_Lookahead-Methods_SS26.pdf", "stem":"3dm_07_lookahead_methods_ss26", "title":"Lecture 7 - Look-ahead Methods", "out":"dddm_l07_lookahead_methods_jp_exam_notes.pdf"},
    {"id":"l08", "no":8, "pdf":"3DM_08_VFA_SS26.pdf", "stem":"3dm_08_vfa_ss26", "title":"Lecture 8 - Value Function Approximation", "out":"dddm_l08_vfa_jp_exam_notes.pdf"},
    {"id":"l09", "no":9, "pdf":"3DM_09_Analytics-Issues-in-ADP_SS26.pdf", "stem":"3dm_09_analytics_issues_in_adp_ss26", "title":"Lecture 9 - Analytics Issues in ADP", "out":"dddm_l09_analytics_issues_in_adp_jp_exam_notes.pdf"},
    {"id":"l10", "no":10, "pdf":"3DM_10_Combined-Methods_SS26.pdf", "stem":"3dm_10_combined_methods_ss26", "title":"Lecture 10 - Combined Methods", "out":"dddm_l10_combined_methods_jp_exam_notes.pdf"},
    {"id":"l11", "no":11, "pdf":"3DM_11_Food-Delivery_SS26.pdf", "stem":"3dm_11_food_delivery_ss26", "title":"Lecture 11 - Platform-based Food Delivery", "out":"dddm_l11_food_delivery_jp_exam_notes.pdf"},
]
LECTURE_BY_ID = {x["id"]: x for x in LECTURES}

# Import richer hand-authored L1-L3 metadata where available.
def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod

try:
    base = load_module("base_notes", ROOT / "scripts" / "generate_l01_l03_structured_notes.py")
    v4 = load_module("v4_notes", ROOT / "scripts" / "generate_l01_l03_v4_notes.py")
    BASE_SLIDES = base.SLIDES
    BASE_LECTURES = base.LECTURES
    BASE_TOPIC_DETAILS = v4.TOPIC_DETAILS
    BASE_ALIASES = v4.ALIASES
except Exception:
    BASE_SLIDES, BASE_TOPIC_DETAILS, BASE_ALIASES = {}, {}, {}

TOPIC_DETAILS: Dict[str, Dict[str, Any]] = {}
TOPIC_DETAILS.update(BASE_TOPIC_DETAILS)
TOPIC_DETAILS.update({
    "dynamism": {
        "focus": ["dynamismは、時間の進行により状態が変わり、意思決定を繰り返す性質である。", "static planning, dynamic planning, a priori optimization, online reoptimizationを区別する。"],
        "explain": [
            "Dynamism は、意思決定問題が時間とともに進行し、状態が変化することを意味する。静的問題では、すべての入力を最初に与えられ、その情報に基づいて一度だけ計画を作る。動的問題では、新しい注文、交通状況、車両位置、キャンセル、故障などが途中で発生し、計画を更新する必要がある。",
            "重要なのは、dynamism は stochasticity と同じではないという点である。stochasticity は未来が不確実であること、dynamism は時間とともに決定と状態が進む構造を持つことである。例えば、すべての未来注文が既知でも、時点ごとに車両位置が変わり決定を繰り返すなら動的である。逆に、将来の需要が確率的でも、最初に一括で決めて変更しないなら静的な確率計画として扱える。",
            "a priori optimization は、実行前に全体計画を作り、実行中は大きく変更しない考え方である。計算しやすく、全体最適を考えやすいが、予期しない情報に弱い。online または dynamic planning は、各時点で現在状態を観測し、必要に応じて決定を変える。現実に適応しやすいが、計算時間や一貫性が問題になる。",
            "配送の例では、朝に全ルートを決めるのが静的計画である。昼に新規注文が入ったり、車両が遅れたりしたときに、現在の車両位置と残り注文を見て再計画するのが動的計画である。動的計画では、今の選択が将来の柔軟性を奪わないかも考える必要がある。",
            "試験答案では、静的/動的の違いを『計画を変更するか』だけでなく、状態、時点、決定、外生情報、遷移の連鎖として説明する。特に動的問題では、状態が更新され、次の決定の入力になるというループを明確に書くと満点答案に近づく。",
        ],
    },
    "mdp": {
        "focus": ["MDPは、状態、決定、外生情報、遷移、報酬、方策で動的意思決定を定式化する。", "未知の事例を見たら、まずMDPの構成要素へ分解する。"],
        "explain": [
            "Markov Decision Process は、時間を持つ意思決定問題を定式化する枠組みである。各時点 t で状態 S_t を観測し、実行可能な決定 x_t を選ぶ。その後、外生情報 W_{t+1} が実現し、遷移関数によって次の状態 S_{t+1} が決まる。このとき報酬または費用 R_t(S_t,x_t) も発生する。",
            "Markov性とは、将来を予測するために必要な情報が現在状態 S_t に含まれているという考え方である。過去の履歴そのものを全て覚える必要はないが、履歴が将来に影響するなら、その影響を現在状態に要約して入れなければならない。例えば配送では、車両位置、残り注文、現在時刻、積載量、遅延状況が状態に含まれる。",
            "方策 policy は、各状態に対してどの決定を選ぶかを定める規則である。最適方策は、単に現在報酬が最大の決定を選ぶのではなく、現在報酬と将来報酬の期待値を合わせて最大にする。これが greedy との違いである。",
            "具体例として在庫問題では、状態は在庫量、決定は注文量、外生情報は需要、遷移は『次在庫 = 現在在庫 + 注文到着 - 需要』、費用は保管費・欠品費・注文費である。配送問題では、状態は車両位置と未処理注文、決定は次に訪問する顧客または割当、外生情報は新規注文や旅行時間、報酬は配送収益または遅延ペナルティである。",
            "試験では、MDPの記号を暗記するより、現実問題を構成要素に落とし込む力が重視される。問題文に新しい事例が出たら、時点、状態、決定、外生情報、遷移、目的関数の順に書くと、体系的な答案になる。",
        ],
    },
    "bellman": {
        "focus": ["Bellman方程式は、即時報酬と期待将来価値の和で決定を評価する。", "Greedy政策と最適政策の違いを説明できるようにする。"],
        "explain": [
            "Bellman方程式は、動的意思決定における最適性の再帰的な考え方である。現在状態 S_t で決定 x を選ぶと、即時報酬 R(S_t,x) が得られる。しかし本当に重要なのは、その決定によって次にどの状態へ進み、そこから将来どれだけ報酬を得られるかである。",
            "Greedy政策は、目の前の即時報酬だけを見て選ぶ。例えば今すぐ最も近い注文を取る、今一番利益が高い注文を取る、在庫を最小にする、といった判断である。短期的には合理的でも、将来の注文や状態を悪化させることがある。",
            "Bellman最適政策は、即時報酬 + 期待将来価値で決定を評価する。配送で、近い注文を取ると車両が需要の少ない地域へ移動し、少し遠い注文を取ると需要が多い地域に残れるなら、後者の方が将来的に良い可能性がある。この『将来の良さ』を価値関数で表す。",
            "価値関数 V(S) は、その状態から将来得られる期待報酬を表す。後決定状態 S_t^x は、決定を行った直後、まだ外生情報が実現していない状態である。後決定状態を使うと、意思決定とランダム情報の実現を分けて考えやすくなる。",
            "試験では、式を書くだけでなく、各項の意味を文章で説明する必要がある。Rは今の報酬、Vは将来価値、期待値は未来の不確実性を平均する操作、argmaxは最も良い決定を選ぶ操作である。",
        ],
    },
    "curse_adp": {
        "focus": ["状態空間・決定空間・情報空間の爆発により厳密DPは実問題で困難になる。", "ADPは近似方策により実用的な良い解を作る考え方である。"],
        "explain": [
            "Curse of dimensionality は、状態や決定や外生情報の次元が増えると、列挙すべき組合せが爆発的に増える現象である。車両が1台で顧客が数人なら全状態を考えられるが、車両が多数、顧客が多数、時間が細かく、新規注文が確率的に来ると、全状態を保存してBellman再帰を解くことは現実的でなくなる。",
            "状態空間のcurseは、状態を表す要素が増えることで起こる。車両位置、積載量、残り時間、未処理注文、ドライバー勤務時間、バッテリー残量をすべて含めると、状態の数は巨大になる。決定空間のcurseは、各状態で選べる行動が多すぎることを意味する。外生情報空間のcurseは、需要、旅行時間、キャンセルなどの未来パターンが多すぎることである。",
            "Approximate Dynamic Programming は、厳密な最適政策を求める代わりに、近似的に良い方策を作る考え方である。近似の対象は、方策そのもの、費用関数、将来価値、look-ahead評価などである。重要なのは、ADPは一つのアルゴリズム名ではなく、厳密DPが困難な問題を実用的に解く方法群である点である。",
            "具体例として配送では、すべての将来注文パターンを列挙する代わりに、現在の車両配置の柔軟性を価値として近似したり、遅延リスクを費用に加えたり、短い将来シナリオを数本だけシミュレーションしたりする。これにより完全最適ではないが、計算時間内に良い意思決定が可能になる。",
            "試験では、なぜADPが必要なのかをまず説明し、その後にPFA, CFA, VFA, look-aheadなどの各手法を比較する。『最適解が見つからないから近似する』だけでなく、どの空間が爆発するのか、何を近似するのかを具体的に述べる。",
        ],
    },
    "policy_classes": {
        "focus": ["Policy Function Approximation, Rolling Horizon, CFA, Look-ahead, VFAを何を近似するかで区別する。", "各手法の強みと弱みを1セットで説明する。"],
        "explain": [
            "Policy Function Approximation は、経験則やルールを直接方策として使う方法である。例えば『在庫が閾値を下回ったら注文する』『最も近いドライバーへ割り当てる』などである。計算は速く解釈しやすいが、複雑な将来影響を十分に扱えない可能性がある。",
            "Rolling Horizon Re-Optimization は、現在時点で見えている情報を使って一定期間の最適化問題を解き、最初の一部だけ実行し、次時点でまた解き直す方法である。現実変化へ適応できるが、見えている範囲だけを最適化するため近視眼的になることがある。",
            "Cost Function Approximation は、現在の目的関数や制約に補正項を加えて、将来に良い影響を持つ決定を誘導する方法である。例えば、将来需要が多い地域から車両を離さないようにペナルティを入れる。設計は問題依存で、補正項が適切でないと逆効果になる。",
            "Look-ahead Methods は、将来シナリオを明示的に考え、現在決定の良し悪しを未来までシミュレーションまたは最適化して評価する方法である。将来を直接見るため直感的だが、計算負荷が大きく、サンプリングやホライズンの選び方に依存する。",
            "Value Function Approximation は、状態または後決定状態の将来価値を特徴量とモデルで近似する方法である。学習した価値を使えば、各決定について遠い未来まで毎回シミュレーションしなくても将来影響を考慮できる。しかし良い特徴量と学習データが必要である。",
        ],
    },
    "lookahead_msa": {
        "focus": ["MSAは複数シナリオを解き、解の共通性から現在決定を選ぶ。", "Consensus functionは問題構造に依存して設計する。"],
        "explain": [
            "Look-ahead は、現在の決定を評価するために将来を仮想的に見る方法である。単一シナリオだけを見ると、そのシナリオに過剰適合する危険がある。そこで Multiple Scenario Approach では、複数の将来シナリオをサンプリングし、それぞれを確定的な問題として解く。",
            "MSAの基本手順は、複数の将来情報列を生成し、各シナリオでMIPなどの確定的最適化を解き、実際にはまだ見えていない将来情報に依存する部分を取り除き、現在時点で実行可能な部分を比較する、という流れである。",
            "Consensus function は、複数シナリオで得られた解の中から代表的な解を選ぶための類似度尺度である。生産スケジューリングなら次に処理するジョブ、VRPなら同じ顧客ペアが同じルートにあるか、TSPならアークや隣接関係が一致するか、施設配置なら選ばれた施設集合が一致するかで測る。",
            "MSAの利点は、通常のMIPソルバーを使えることと、複数シナリオに対して極端に悪くない現在決定を選べることである。欠点は、stochasticityを解選択で間接的に扱うだけで、動的な再意思決定そのものを完全にモデル化しているわけではない点である。",
            "試験では、MSAを『複数シナリオの平均を取る』だけと書かない。各シナリオの解を作り、その解の共通性や代表性を測り、現在実装すべき決定を選ぶ、という構造を説明する。Consensus functionは問題ごとに設計する必要がある。",
        ],
    },
    "rollout": {
        "focus": ["Rolloutは候補決定後の状態から将来方策をシミュレーションし、現在決定を評価する。", "simulation horizonは終端効果、計算時間、将来情報の信頼性に依存する。"],
        "explain": [
            "Rollout は、現在の候補決定を選んだ後、将来をある方策でシミュレーションして総報酬を見積もる方法である。単に現在報酬だけを見るのではなく、決定後の状態が将来どのような結果を生むかを評価する点が重要である。",
            "Post-decision state rollout では、まず候補決定 x を実行した直後の後決定状態 S^x を作る。その後、外生情報をサンプリングし、ベース方策で未来を進める。これを複数回繰り返して平均すれば、その候補決定の期待的な将来性能を近似できる。",
            "ホライズンを長くすれば終端効果や長期的影響を考えられるが、計算量が増え、遠い将来の予測は不確実になる。短いホライズンは速いが近視眼的になる可能性がある。在庫やダムのように長期的な蓄積が重要な問題では長めのホライズンが必要になりやすい。食品配送のように注文が短時間で完結する問題では短めのホライズンでも有効な場合がある。",
            "Rolloutの欠点は、各候補決定について多くの未来シミュレーションが必要になり計算負荷が大きいことである。また、ベース方策が悪いと評価も悪くなり、サンプリング数が少ないと推定が不安定になる。",
            "試験では、Rolloutを将来価値近似やlook-aheadと関連づけて説明する。候補決定を比べる、後決定状態から未来をサンプルする、ベース方策で将来を進める、平均性能で選ぶ、という流れを書くとよい。",
        ],
    },
    "vfa": {
        "focus": ["VFAは将来価値を特徴量に基づいて近似し、現在決定に組み込む。", "状態そのものではなく、価値を説明する特徴量設計が重要である。"],
        "explain": [
            "Value Function Approximation は、各状態の将来価値を厳密に保存する代わりに、特徴量を使って近似する方法である。全状態を列挙できないため、状態の本質的な性質を少数の特徴で表し、その特徴から将来価値を予測する。",
            "後決定状態を使うVFAでは、現在決定を行った後の状態 S^x に対して価値 \hat{V}(S^x) を推定する。そして R(S,x)+\hat{V}(S^x) が最大になる決定を選ぶ。これにより、毎回遠い未来をロールアウトしなくても将来影響を考慮できる。",
            "特徴量の例として配送では、残り注文数、車両の空き容量、車両が需要密度の高い地域にいるか、残り時間、遅延している注文数、将来需要予測などがある。在庫では在庫量、需要予測、残り期間、容量余裕、欠品リスクが特徴になる。",
            "VFAの難しさは、良い特徴量を選ぶことと、価値近似を安定に学習することである。重要な情報を特徴量に入れなければ価値推定は間違う。一方で特徴量が多すぎると学習に必要なデータが増え、過学習や次元の呪いが再び問題になる。",
            "試験では、VFAの式を説明するだけでなく、具体問題でどの特徴量が将来価値を説明するかを提案することが重要である。単に『機械学習で価値を予測する』ではなく、何を入力し、何を出力し、その出力を現在決定にどう使うかを書く。",
        ],
    },
    "analytics_adp": {
        "focus": ["ADPではデータ生成、特徴量、学習方法、評価が政策品質を左右する。", "feature selectionとdimensionality reductionを区別する。"],
        "explain": [
            "Analytics Issues in ADP では、ADPを動かすためのデータ分析上の問題を扱う。価値関数や方策を近似するには、状態、決定、外生情報、報酬、遷移のデータが必要である。実データだけでは不足する場合、シミュレーションで学習データを生成することもある。",
            "supervised learning は、入力と正解ラベルの対応から予測モデルを学ぶ方法である。VFAでは、特徴量を入力し、シミュレーションやDPで得た価値推定をラベルとして学習できる。unsupervised learning は、ラベルなしデータからクラスタや低次元構造を見つける。状態集約や需要パターン分類で役立つ。",
            "Feature selection は、既存の候補特徴から重要なものを選ぶことである。例えば車両位置、残り容量、残り時間、遅延注文数のうち、将来価値の説明に効くものを選ぶ。Dimensionality reduction は、既存特徴を組み合わせて新しい低次元表現を作ることである。PCAやオートエンコーダのような方法が該当する。",
            "外生情報の生成では、過去データから分布を推定し、乱数で将来シナリオを生成する。旅行時間、需要発生、サービス時間などをサンプリングすることで、RolloutやVFA学習に必要な未来パスを作る。ただし、分布仮定が間違っていると学習された方策も現実に合わない。",
            "試験では、ADPを単なる最適化手法としてではなく、データ分析・特徴量設計・学習・シミュレーションが組み合わさったシステムとして説明する。特にfeature selectionとdimensionality reductionの違いは頻出であり、例を添えて説明する。",
        ],
    },
    "combined_methods": {
        "focus": ["ADP手法の組み合わせは、片方の弱点をもう片方で補うために行う。", "計算量、将来考慮、解釈可能性、学習可能性の観点で組み合わせを説明する。"],
        "explain": [
            "Combined Methods は、PFA, CFA, Look-ahead, VFAなどを単独で使うのではなく、複数組み合わせる考え方である。実問題では、一つの手法だけで高速性、将来考慮、解釈可能性、精度のすべてを満たすことは難しい。",
            "PFA + VFA の組み合わせでは、基本方策をルールで高速に作り、その選択を価値関数で補正する。例えば配送で『最も近い注文を選ぶ』というPFAを使いつつ、将来需要が多い地域に残る価値をVFAで加味する。これにより、単純ルールの速さと将来考慮を両立できる。",
            "CFA + Look-ahead では、目的関数に将来柔軟性のペナルティを入れたうえで、短い将来シナリオを解く。これにより、look-aheadの近視眼性を補い、計算可能な範囲で将来リスクを考慮できる。",
            "Rollout + VFA では、遠い未来をすべてシミュレーションする代わりに、途中からVFAで終端価値を近似する。これは長いホライズンの計算負荷を下げる典型的な組み合わせである。チェスや在庫制御のように、探索の末端を価値関数で評価する考え方に近い。",
            "試験では、組み合わせを列挙するだけでは不十分である。各組み合わせについて、どの弱点を補うのか、どの問題で有効か、期待される利点と残る欠点を説明する。",
        ],
    },
    "food_delivery": {
        "focus": ["Platform-based food deliveryは、需要・供給・推薦・配送の複数意思決定が連鎖する問題である。", "food recommendationとdelivery optimizationを分けつつ、相互作用を説明する。"],
        "explain": [
            "Platform-based food delivery は、顧客、レストラン、配達員、プラットフォームが相互作用する多面的なサービスである。顧客は料理を選び、レストランは注文を調理し、配達員は複数注文を運び、プラットフォームは推薦、価格、割当、ルーティングを決める。",
            "この問題では、単に最短ルートを作るだけでは不十分である。推薦システムが特定店舗に需要を集中させると、調理待ちや配達遅延が増える可能性がある。逆に、配送能力を考慮した推薦を行えば、需要を空いている店舗や配送しやすい地域へ誘導できる。",
            "food recommendation では、content-based recommendation, collaborative filtering, ontology graph, diversificationなどが扱われる。顧客の好みだけでなく、料理の種類、価格、距離、調理時間、配達可能性などが推薦品質に影響する。",
            "配送最適化では、注文受諾、配達員割当、ピックアップ順、ドロップオフ順、複数注文のバッチングが問題になる。時間窓、料理の品質劣化、顧客待ち時間、配達員の公平性なども考慮する必要がある。",
            "試験では、食品配送をMDP/ADPとして設計する場合、状態に未処理注文、配達員位置、レストラン調理状態、需要予測を入れ、決定に推薦・注文受諾・割当・ルーティングを入れる。報酬には収益、遅延ペナルティ、顧客満足度、配達員稼働を含めるとよい。",
        ],
    },
})

TITLE_TRANSLATIONS = {
    "Agenda":"アジェンダ", "Goals":"到達目標", "Content":"内容", "Summary":"まとめ", "Literature":"文献", "Introduction":"導入",
    "Decision making":"意思決定", "Dynamism":"動的性質", "Static and Dynamic Planning":"静的計画と動的計画",
    "Markov Decision Process":"マルコフ意思決定過程", "Dynamic Decision Process":"動的意思決定プロセス",
    "Optimal Solution":"最適解", "Bellman Equation":"ベルマン方程式", "Value Function":"価値関数", "Curses of Dimensionality":"次元の呪い",
    "Approximate Dynamic Programming":"近似動的計画法", "Policy Classes":"方策クラス", "Multiple Scenario Approach (MSA)":"Multiple Scenario Approach（MSA）",
    "Sampling + Mixed Integer Programming":"サンプリング + 混合整数計画", "Post-Decision State Rollout":"後決定状態ロールアウト",
    "Value Function Approximation (VFA)":"価値関数近似（VFA）", "Data Analytics Issues for ADP Methods":"ADP手法におけるデータ分析上の論点",
    "Unsupervised vs. Supervised Learning":"教師なし学習と教師あり学習", "Feature Selection":"特徴選択", "Dimensionality Reduction":"次元削減",
    "We can combine ADP-methods":"ADP手法は組み合わせることができる", "Platform-based food delivery":"プラットフォーム型フードデリバリー",
    "Properties":"性質", "Interaction of partner":"参加者間の相互作用", "Food ontology graph (content based recommendation)":"食のオントロジーグラフ（内容ベース推薦）",
}

PHRASE_MAP = [
    ("Data Driven Decision Making", "データ駆動型意思決定"), ("Decision Support", "意思決定支援"),
    ("Office hours", "オフィスアワー"), ("with registration only", "事前登録制"), ("Teaching Assistant", "ティーチングアシスタント"),
    ("Master thesis", "修士論文"), ("Master seminar", "修士セミナー"), ("Lecture", "講義"), ("Exercise", "演習"),
    ("Stochasticity", "確率性"), ("Dynamism", "動的性質"), ("stochastic", "確率的"), ("dynamic", "動的"),
    ("Information Model", "情報モデル"), ("Decision Model", "意思決定モデル"), ("Real-World", "現実世界"),
    ("Aggregation", "集約"), ("Implementation", "実装"), ("Disaggregation", "非集約化/実装への展開"),
    ("Operations Research", "オペレーションズ・リサーチ"), ("Business Analytics", "ビジネスアナリティクス"),
    ("Intelligent Data Analysis", "知的データ分析"), ("Planning", "計画"), ("Transportation", "交通・輸送"), ("Mobility", "モビリティ"),
    ("Travelling Salesman Problem", "巡回セールスマン問題"), ("Vehicle Routing Problem", "車両ルーティング問題"), ("TSP", "TSP"), ("VRP", "VRP"),
    ("Markov Decision Process", "マルコフ意思決定過程"), ("MDP", "MDP"), ("Policy", "方策"), ("policy", "方策"),
    ("Reward", "報酬"), ("reward", "報酬"), ("State", "状態"), ("state", "状態"), ("Decision", "決定"), ("decision", "決定"),
    ("exogenous information", "外生情報"), ("transition", "遷移"), ("Value Function", "価値関数"), ("Bellman", "ベルマン"),
    ("Curses of Dimensionality", "次元の呪い"), ("Approximate Dynamic Programming", "近似動的計画法"), ("ADP", "ADP"),
    ("Policy Function Approximation", "方策関数近似"), ("Cost Function Approximation", "費用関数近似"), ("Value Function Approximation", "価値関数近似"),
    ("Rolling Horizon Re-Optimization", "ローリングホライズン再最適化"), ("Look-ahead", "先読み"), ("look-ahead", "先読み"),
    ("Multiple Scenario Approach", "複数シナリオアプローチ"), ("Consensus Function", "合意関数"), ("Rollout", "ロールアウト"),
    ("post-decision state", "後決定状態"), ("Mixed Integer Programming", "混合整数計画"), ("MIP", "MIP"),
    ("uncertainty", "不確実性"), ("Travel Times", "旅行時間"), ("travel time", "旅行時間"), ("FIFO", "FIFO"),
    ("probability distribution", "確率分布"), ("distribution", "分布"), ("Hurwicz", "Hurwicz基準"), ("regret", "後悔"),
    ("robust", "ロバスト"), ("Quasi", "準"), ("simulation", "シミュレーション"), ("Simulation", "シミュレーション"),
    ("Feature selection", "特徴選択"), ("feature selection", "特徴選択"), ("Dimensionality reduction", "次元削減"), ("supervised learning", "教師あり学習"), ("unsupervised learning", "教師なし学習"),
    ("food delivery", "フードデリバリー"), ("recommendation", "推薦"), ("ontology", "オントロジー"), ("collaborative filtering", "協調フィルタリング"),
]

ANSWER_TEMPLATES = {
    "TSP": "満点答案では、顧客集合をノード、移動をアーク、旅行時間または距離をコストとして定義し、二値決定変数 x_ij により i から j へ移動するかを表す。目的関数は選択アークの総コスト最小化であり、各顧客へ一度入る制約、各顧客から一度出る制約、部分巡回除去制約を含める。時間依存の場合はコストを d_ij ではなく d_ij(t) とし、到着時刻が後続アークの旅行時間へ影響することも述べる。",
    "Business Analytics": "満点答案では、Business AnalyticsをStatistics、Operations Research、Computer Science/Information Systemsの統合領域として説明する。Statisticsは不確実性・推定・予測、ORは最適化・意思決定、CS/ISはデータ処理・情報システム・実装を担当する。データ分析だけでは実行すべき行動が決まらず、最適化だけでは現実データを反映できないため、三領域の交差が必要である。",
    "Information Model": "満点答案では、Real Worldから観測データを集約してInformation Modelを作り、そこからDecision Modelを作り、解をImplementation/Disaggregationで現実の行動へ戻す流れを説明する。Information Modelは現実の圧縮表現であり、Decision Modelは決定変数、目的関数、制約により行動選択を評価する構造である。",
    "FIFO": "満点答案では、FIFOを、同じリンクや経路に先に入った車両が後から入った車両に追い越されない条件として説明する。時間帯別旅行時間が不連続に切り替わると、遅く出発した方が早く到着する矛盾が起こり得る。補正には線形補間や関数の平滑化、FIFOを満たすような旅行時間関数の修正を用いる。",
    "Uncertainty": "満点答案では、stochasticは確率分布があり期待値・分散・分位点・サンプリングを扱える場合、quasi-stochasticは確率は不明だがシナリオや区間が分かる場合として区別する。ロバスト解は平均ケースで最短とは限らないが、複数シナリオで大きく崩れにくい解である。regretは、シナリオが分かった後に選べた最適解との差である。",
    "MDP": "満点答案では、決定時点、状態 S_t、決定 x_t、外生情報 W_{t+1}、遷移 S_{t+1}=S^M(S_t,x_t,W_{t+1})、報酬または費用 R_t(S_t,x_t)、方策 X_t^\pi(S_t)、目的関数を定義する。具体事例では、状態が何を含み、決定で何を選び、外生情報で何がランダムに起こるかを対応付ける。",
    "Bellman": "満点答案では、Bellman方程式が即時報酬と期待将来価値の和を最大化する再帰式であると説明する。Greedy政策は即時報酬だけを見るが、最適政策は将来価値も見る。状態空間、決定空間、外生情報空間が増えると再帰計算が爆発し、ADPや価値関数近似が必要になる。",
    "Policy": "満点答案では、PFA、Rolling Horizon、CFA、Look-ahead、VFAを列挙し、それぞれが何を近似するかを説明する。PFAは方策そのもの、CFAは目的関数や制約、Look-aheadは将来シナリオ評価、VFAは将来価値を近似する。各手法の強みと弱みも必ず書く。",
    "Rollout": "満点答案では、Rolloutが候補決定後の状態から未来をシミュレーションし、現在決定を評価する方法だと説明する。simulation horizonは、終端効果、計算負荷、将来情報の信頼性、問題の時間スケールに依存する。Post-decision rolloutの欠点として計算負荷、ベース方策依存、サンプリング誤差を挙げる。",
    "VFA": "満点答案では、VFAが状態または後決定状態の将来価値を特徴量から近似する方法であると説明する。決定評価では R(S,x)+\hat V(S^x) を使う。特徴量には残り需要、リソース余裕、時間、位置、需要密度などがあり、feature selectionとdimensionality reductionを区別する。",
    "Combined": "満点答案では、ADP手法を組み合わせる目的を、片方の弱点をもう片方で補うこととして説明する。例としてPFA+VFA、CFA+Look-ahead、Rollout+VFAを挙げ、計算量、将来考慮、解釈可能性、学習可能性の観点から利点と残る欠点を述べる。",
    "Food": "満点答案では、フードデリバリーを顧客、レストラン、配達員、プラットフォームの相互作用として説明し、推薦、注文受諾、配達員割当、ルーティングが連鎖することを書く。MDPなら状態は未処理注文、配達員位置、調理状態、需要予測、決定は推薦・受諾・割当・ルート、報酬は収益・遅延・満足度である。",
}


def tex_escape(s: str) -> str:
    repl = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(repl.get(ch, ch) for ch in str(s))


def run(cmd: Sequence[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(list(cmd), cwd=str(cwd) if cwd else None, check=check, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def pdf_pages(pdf: Path) -> int:
    out = run(["pdfinfo", str(pdf)]).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else 1


def extract_text(pdf: Path) -> List[str]:
    EXTRACT.mkdir(exist_ok=True)
    out = EXTRACT / f"{pdf.name}.txt"
    if not out.exists():
        run(["pdftotext", "-layout", str(pdf), str(out)])
    txt = out.read_text(encoding="utf-8", errors="ignore")
    pages = txt.split("\f")
    n = pdf_pages(pdf)
    while len(pages) < n:
        pages.append("")
    return pages[:n]


def filter_lines(text: str) -> List[str]:
    lines = []
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        if any(x in s for x in ["Data Driven Decision Making |", "© Prof", "Technische", "Universität", "Institut für", "Page "]):
            continue
        if re.match(r"^\d+$", s):
            continue
        if s.startswith("Platzhalter"):
            continue
        if re.match(r"^[A-Za-z0-9 .,/:-]+\.(de|com|org)$", s):
            continue
        lines.append(re.sub(r"\s+", " ", s))
    return lines


def guess_title(lines: List[str], fallback: str) -> str:
    if not lines:
        return fallback
    for s in lines:
        if len(s) < 3:
            continue
        if "Lecture" in s and "Data Driven" in s:
            continue
        return s[:120]
    return fallback


def jp_line(line: str) -> str:
    s = line.strip("• ")
    if s in TITLE_TRANSLATIONS:
        return TITLE_TRANSLATIONS[s]
    # Common title-like lines
    for en, jp in sorted(TITLE_TRANSLATIONS.items(), key=lambda x: -len(x[0])):
        if s == en:
            return jp
    # Whole phrase shortcuts
    lower = s.lower()
    if lower.startswith("agenda"):
        return "アジェンダ"
    if lower.startswith("recap"):
        return "前回の復習と今回の位置づけ"
    if lower.startswith("example"):
        return s.replace("Example", "例").replace("Examples", "例")
    if lower.startswith("advantages"):
        return s.replace("Advantages", "利点")
    if lower.startswith("disadvantages"):
        return s.replace("Disadvantages", "欠点")
    # Apply terminology replacements.
    out = s
    for en, jp in sorted(PHRASE_MAP, key=lambda x: -len(x[0])):
        out = out.replace(en, jp)
    # Some syntax cleanup.
    out = out.replace("Objective", "目的").replace("Goals", "目標").replace("Goal", "目標")
    out = out.replace("Idea", "考え方").replace("Properties", "性質").replace("Advantage", "利点").replace("Disadvantage", "欠点")
    out = out.replace("Examples", "例").replace("Example", "例").replace("Case study", "ケーススタディ")
    out = out.replace("maximize", "最大化する").replace("minimize", "最小化する").replace("expected", "期待される")
    if out == s and re.search(r"[A-Za-z]{4,}", out):
        # Explicitly mark as Japanese note generated from original expression, without repeating too much English.
        out = f"{out}（この用語は講義スライド上の専門語として扱う）"
    return out


def make_translation(lines: List[str], max_items: int = 9) -> List[str]:
    if not lines:
        return ["このページは画像・表紙・または図中心であり、本文の翻訳対象は少ない。"]
    seen = set()
    items = []
    for s in lines:
        if s in seen:
            continue
        seen.add(s)
        if len(s) > 160:
            s = s[:160] + "..."
        # skip title duplicate? keep if first.
        items.append(jp_line(s))
        if len(items) >= max_items:
            break
    return items or ["このページは図中心であり、主要概念を解説で扱う。"]


def classify_topic(lec_id: str, title: str, lines: List[str]) -> str:
    text = " ".join([title] + lines).lower()
    if lec_id == "l01":
        if any(k in text for k in ["decision making", "motivation", "stochastic", "dynamism", "summary"]): return "dddm_intro"
        if any(k in text for k in ["real-world", "information model", "decision model", "aggregation", "implementation"]): return "process_loop"
        return "admin"
    if lec_id == "l02":
        if any(k in text for k in ["business analytics", "ida", "intelligent data analysis", "pmt", "appearance", "structure"]): return "ba_ida_pmt"
        if any(k in text for k in ["travelling", "salesman", "tsp", "vehicle routing", "routing"]): return "tsp_model"
        if any(k in text for k in ["travel time", "time-dependent", "temporal", "historical"]): return "time_dependent_travel"
        if any(k in text for k in ["floating car", "fcd", "aggregation", "generalization", "cluster"]): return "fcd_aggregation"
        if "fifo" in text: return "fifo"
        if any(k in text for k in ["heuristic", "insertion", "nearest", "savings"]): return "heuristics"
        return "process_loop"
    if lec_id == "l03":
        if any(k in text for k in ["distribution", "pdf", "probability", "normal", "exponential", "sampling"]): return "probability_distribution"
        if any(k in text for k in ["stochastic decision", "expected", "variance", "monte carlo"]): return "stochastic_decision"
        if any(k in text for k in ["quasi", "hurwicz", "regret", "minmax", "interval"]): return "quasi_stochastic"
        if any(k in text for k in ["robust", "vrp"]): return "robust_vrp"
        if any(k in text for k in ["uncertainty", "travel times", "consequences"]): return "uncertainty_intro"
        return "modeling_uncertainty"
    if lec_id == "l04": return "dynamism"
    if lec_id == "l05":
        if any(k in text for k in ["bellman", "optimal", "value function", "greedy"]): return "bellman"
        return "mdp"
    if lec_id == "l06":
        if any(k in text for k in ["bellman", "value function", "optimal", "policy"]): return "bellman"
        if any(k in text for k in ["curse", "approximate", "adp"]): return "curse_adp"
        return "policy_classes"
    if lec_id == "l07":
        if any(k in text for k in ["multiple scenario", "msa", "consensus", "mixed integer"]): return "lookahead_msa"
        if any(k in text for k in ["rollout", "post-decision"]): return "rollout"
        return "policy_classes"
    if lec_id == "l08":
        if any(k in text for k in ["rollout", "horizon", "simulation"]): return "rollout"
        return "vfa"
    if lec_id == "l09": return "analytics_adp"
    if lec_id == "l10": return "combined_methods" if any(k in text for k in ["combine", "combined", "combination"]) else "policy_classes"
    if lec_id == "l11": return "food_delivery"
    return "dddm_intro"


def base_slide_for_l01_l03(lec_id: str, page: int) -> Dict[str, Any] | None:
    if lec_id not in BASE_SLIDES:
        return None
    b = BASE_SLIDES.get(lec_id, {}).get(page)
    if not b:
        return None
    return {"title": b.get("title", f"Slide {page}"), "translation": [x if isinstance(x, str) else x[0] for x in b.get("translation", [])], "topic": BASE_ALIASES.get(b.get("topic", "admin"), b.get("topic", "admin"))}


def slide_records(lec: Dict[str, Any]) -> List[Dict[str, Any]]:
    pdf = MAT / lec["pdf"]
    pages_text = extract_text(pdf)
    recs = []
    for i, txt in enumerate(pages_text, 1):
        lines = filter_lines(txt)
        title = guess_title(lines, f"Slide {i}")
        base_rec = base_slide_for_l01_l03(lec["id"], i)
        if base_rec:
            # Keep hand-authored title/translation but use the same v5 rendering.
            title = base_rec["title"]
            translation = base_rec["translation"] or make_translation(lines)
            topic = base_rec["topic"]
        else:
            translation = make_translation(lines)
            topic = classify_topic(lec["id"], title, lines)
        # For title/agenda/administrative pages, avoid forced content.
        if i == 1 or re.search(r"^(agenda|content|literature|goals|goals today|recap|about|contact)", title.lower()):
            if topic not in ["dddm_intro", "dynamism", "mdp"]:
                # keep content pages as admin unless keyword makes it conceptually important
                if title.lower() in ["agenda", "content", "literature"] or "contact" in title.lower() or "about the" in title.lower():
                    topic = "admin"
        recs.append({"page": i, "title": title, "translation": translation, "topic": topic, "raw_lines": lines})
    return recs


def detail_for(topic: str) -> Dict[str, Any]:
    return TOPIC_DETAILS.get(topic, TOPIC_DETAILS.get("dddm_intro"))


def latex_itemize(items: Sequence[str]) -> str:
    out = [r"\begin{itemize}"]
    for it in items:
        out.append(r"\item " + tex_escape(it))
    out.append(r"\end{itemize}")
    return "\n".join(out)


def tex_pars(pars: Sequence[str]) -> str:
    return "\n".join(tex_escape(p) + r"\par" for p in pars)


def check_questions(lec: Dict[str, Any], rec: Dict[str, Any]) -> List[Tuple[str, str]]:
    topic = rec["topic"]
    if topic == "admin":
        return []
    detail = detail_for(topic)
    p = rec["page"]
    title = rec["title"]
    focus = detail["focus"][0] if detail.get("focus") else "このページの概念を説明する"
    q1 = f"L{lec['no']:02d}-S{p:03d}: 「{title}」の概念を、定義・具体例・モデル上の意味の順に説明せよ。"
    a1 = f"定義としては、{focus}。具体例では、配送・在庫・フードデリバリーのような現実問題を用い、状態、決定、外生情報、報酬、または情報モデル/意思決定モデルのどこに対応するかを明示する。モデル上の意味として、この概念が目的関数、制約、状態表現、将来価値、または方策選択にどのような影響を与えるかを書く。試験では、用語だけを列挙せず、入力データから意思決定、さらに現実の実装へつながる流れを文章で示すことが重要である。"
    q2 = f"L{lec['no']:02d}-S{p:03d}: このスライドの考え方を、講義全体のDDDMプロセスの中に位置づけよ。"
    a2 = "DDDMプロセスでは、現実世界のデータを集約して情報モデルを作り、意思決定モデルまたは方策で行動を選び、実装後に結果を観測して次の状態へ進む。このスライドの概念は、そのどこか一部だけではなく、データ表現、意思決定、将来不確実性、計算可能性のいずれかに関わる。答案では、まずこの概念がどの段階に属するかを述べ、次に他の段階へどう影響するかを書く。例えば価値関数なら将来価値を現在決定へ戻す役割、FIFOなら旅行時間情報モデルの整合性を保証する役割、CFAなら目的関数を調整して将来に良い行動を誘導する役割である。"
    return [(q1, a1), (q2, a2)]


def write_slide_tex(lec: Dict[str, Any], rec: Dict[str, Any]) -> str:
    topic = rec["topic"]
    detail = detail_for(topic)
    pdf_path = f"../Materials/2026/{lec['pdf']}"
    page = rec["page"]
    title = rec["title"]
    left = []
    left.append(r"\NoteSection{日本語訳}")
    left.append(latex_itemize(rec["translation"][:10]))
    if topic != "admin":
        left.append(r"\NoteSection{試験対策ポイント}")
        left.append(latex_itemize(detail.get("focus", [])[:3]))
    right = []
    if topic != "admin":
        right.append(r"\NoteSection{解説}")
        intro = f"このページでは「{title}」を理解する。スライド上の表現は短いが、試験では定義、具体例、モデル上の意味、手法の限界まで説明できる必要がある。"
        right.append(tex_pars([intro] + detail.get("explain", [])))
        qs = check_questions(lec, rec)
        if qs:
            right.append(r"\NoteSection{確認問題と解答}")
            right.append(r"\begin{enumerate}")
            for q, a in qs:
                right.append(r"\item \textbf{" + tex_escape(q) + r"}\\" + tex_escape(a))
            right.append(r"\end{enumerate}")
    else:
        right.append(r"\NoteSection{注記}")
        right.append(tex_escape("このページは表紙・目次・事務情報・導入画像が中心であるため、無理に確認問題や過去問を付けない。"))
    return rf"""
\clearpage
\SlideHeader{{{tex_escape(lec['title'])}}}{{{page:03d}}}{{{tex_escape(title)}}}
\begin{{minipage}}[t]{{0.405\textwidth}}
\SlideImage{{{page}}}{{{pdf_path}}}
\begin{{adjustbox}}{{max totalsize={{\textwidth}}{{0.43\textheight}},center}}
\begin{{minipage}}{{\textwidth}}\scriptsize
{''.join(left)}
\end{{minipage}}
\end{{adjustbox}}
\end{{minipage}}\hfill
\begin{{minipage}}[t]{{0.58\textwidth}}
\begin{{adjustbox}}{{max totalsize={{\textwidth}}{{0.89\textheight}},center}}
\begin{{minipage}}{{\textwidth}}\scriptsize
{''.join(right)}
\end{{minipage}}
\end{{adjustbox}}
\end{{minipage}}
"""


def exam_topic_key(topic: str) -> str:
    t = topic.lower()
    for key in ["TSP", "Business Analytics", "Information Model", "FIFO", "Uncertainty", "MDP", "Bellman", "Policy", "Rollout", "VFA", "Combined", "Food"]:
        if key.lower().split()[0] in t or key.lower() in t:
            return key
    if "travel" in t or "regret" in t or "hurwicz" in t or "robust" in t: return "Uncertainty"
    if "policy" in t or "adp" in t: return "Policy"
    if "feature" in t or "value" in t: return "VFA"
    if "inventory" in t or "dam" in t or "gas" in t: return "MDP"
    return "Information Model"


def read_exam_index() -> List[Dict[str, str]]:
    path = ROOT / "data" / "exam_question_index.csv"
    if not path.exists(): return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def exam_items_for_lecture(lec: Dict[str, Any]) -> List[Dict[str, str]]:
    items = []
    target1 = f"Lecture {lec['no']}"
    for row in read_exam_index():
        if target1 in row.get("likely_lecture", ""):
            items.append(row)
    # Keep order and avoid duplicates.
    seen = set(); out = []
    for r in items:
        k=(r.get("term"), r.get("question"))
        if k not in seen:
            seen.add(k); out.append(r)
    return out


def write_exam_tex(lec: Dict[str, Any], items: List[Dict[str,str]]) -> str:
    if not items:
        return ""
    parts = [rf"\clearpage\ExamHeader{{{tex_escape(lec['title'])}}}"]
    for r in items:
        ref = f"{r.get('term','')} {r.get('question','')} ({r.get('points','?')} 点)"
        topic = r.get("topic", "")
        understand = r.get("what_to_understand", "")
        key = exam_topic_key(topic)
        answer = ANSWER_TEMPLATES.get(key, ANSWER_TEMPLATES["Information Model"])
        example = (
            "具体例として、配送問題なら、顧客注文・車両位置・旅行時間を情報モデルにし、訪問順や割当を意思決定モデルで決める。"
            "在庫問題なら、在庫水準を状態、注文量を決定、需要を外生情報、在庫更新式を遷移、欠品費・保管費を費用として整理する。"
            "問題文の文脈に合わせて、抽象用語を必ず具体的な変数や行動に置き換える。"
        )
        rubric = [
            "設問が求める概念の定義を最初に明確に書く。",
            "講義の専門語を列挙するだけでなく、現実例とモデル要素へ対応付ける。",
            "利点だけでなく限界・注意点も最低一つ述べる。",
            "式が出る問題では、記号の意味を文章で説明する。",
            "新しい事例問題では、状態・決定・外生情報・遷移・報酬/費用の順に整理する。",
        ]
        parts.append(rf"\ExamQuestion{{{tex_escape(ref)}}}")
        parts.append(r"\ExamSubsection{問題内容}")
        parts.append(tex_escape(f"{topic}。設問では、{understand} ことが求められる。") + r"\par")
        parts.append(r"\ExamSubsection{満点答案}")
        parts.append(tex_escape(answer) + r"\par")
        parts.append(r"\ExamSubsection{具体例による解説}")
        parts.append(tex_escape(example) + r"\par")
        parts.append(r"\ExamSubsection{採点で落とさない要素}")
        parts.append(latex_itemize(rubric))
        parts.append(r"\vspace{2mm}\hrule\vspace{2mm}")
    return "\n".join(parts)


def write_section(lec: Dict[str, Any]) -> None:
    recs = slide_records(lec)
    out = [r"\section*{" + tex_escape(lec["title"]) + "}", r"\addcontentsline{toc}{section}{" + tex_escape(lec["title"]) + "}"]
    for rec in recs:
        out.append(write_slide_tex(lec, rec))
    out.append(write_exam_tex(lec, exam_items_for_lecture(lec)))
    SECTIONS.mkdir(parents=True, exist_ok=True)
    (SECTIONS / f"{lec['stem']}_v5.tex").write_text("\n".join(out), encoding="utf-8")

    md = [f"# {lec['title']} - review v5", "", "このMarkdownは、PDF生成に用いた内容の索引です。詳細本文は latex/sections の v5 TeX に保存されています。", "", "## ページ一覧", ""]
    for rec in recs:
        md.append(f"- Slide {rec['page']:03d}: {rec['title']} / topic={rec['topic']}")
    md.append("\n## 出力方針\n")
    md.append("- 最新PDFは `output/latest/` のみに置く。")
    md.append("- 過去PDFは `output/history/<timestamp>/` に移動する。")
    md.append("- `latex/` にはPDF成果物を置かない。")
    NOTES.mkdir(exist_ok=True)
    (NOTES / f"{lec['stem']}_v5.md").write_text("\n".join(md), encoding="utf-8")


def write_main(lec: Dict[str, Any]) -> None:
    main = rf"""
\documentclass[a4paper,landscape,9pt]{{article}}
\usepackage[margin=6mm]{{geometry}}
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
\setlength{{\parskip}}{{1.8pt}}
\setlist[itemize]{{leftmargin=1.05em,itemsep=0.7pt,topsep=0.8pt,parsep=0pt}}
\setlist[enumerate]{{leftmargin=1.20em,itemsep=1.0pt,topsep=0.8pt,parsep=0pt}}
\hypersetup{{colorlinks=true,linkcolor=blue,urlcolor=blue}}
\titleformat{{\section}}{{\Large\bfseries\color{{TUBSred}}}}{{}}{{0pt}}{{}}
\newcommand{{\SlideHeader}}[3]{{%
  \noindent{{\large\bfseries #1 / Slide #2: #3}}\hfill {{\scriptsize review v5}}\par
  \vspace{{0.6mm}}\hrule\vspace{{0.8mm}}
}}
\newcommand{{\SlideImage}}[2]{{%
  \noindent\makebox[\textwidth][c]{{\includegraphics[page=#1,width=\textwidth,height=0.45\textheight,keepaspectratio]{{#2}}}}\par
  \vspace{{0.8mm}}
}}
\newcommand{{\NoteSection}}[1]{{%
  \vspace{{1.0mm}}\noindent{{\normalsize\bfseries\color{{TUBSred}}#1}}\par\vspace{{0.35mm}}
}}
\newcommand{{\ExamHeader}}[1]{{%
  \noindent{{\Large\bfseries\color{{TUBSred}}過去問演習: #1}}\hfill {{\scriptsize review v5}}\par
  \vspace{{1mm}}\hrule\vspace{{2mm}}
  {{\small 関連知識を一通り説明した後に置く独立演習ページである。スライドページには同じ過去問を繰り返さない。}}\par\vspace{{2mm}}
}}
\newcommand{{\ExamQuestion}}[1]{{\vspace{{2mm}}\noindent{{\large\bfseries #1}}\par\vspace{{0.8mm}}}}
\newcommand{{\ExamSubsection}}[1]{{\vspace{{1.2mm}}\noindent{{\normalsize\bfseries\color{{TUBSred}}#1}}\par\vspace{{0.6mm}}}}
\begin{{document}}
\begin{{titlepage}}
\centering
\vspace*{{2cm}}
{{\Huge Data Driven Decision Making\par}}
\vspace{{0.5cm}}
{{\Large {tex_escape(lec['title'])} - 日本語訳・詳細解説・試験対策ノート\par}}
\vspace{{1cm}}
\begin{{minipage}}{{0.82\textwidth}}
このPDFは review v5 です。全講義資料へ同じ形式を適用し、各スライドページには元スライド、日本語訳、詳細解説、試験対策ポイント、ページ固有の確認問題と解答を配置しています。過去問は重複を避け、必要な知識を説明した後に独立演習ページとしてまとめています。
\end{{minipage}}
\vfill
{{\large Materials/2026/{tex_escape(lec['pdf'])}}}
\end{{titlepage}}
\tableofcontents
\clearpage
\input{{sections/{lec['stem']}_v5.tex}}
\end{{document}}
"""
    LATEX.mkdir(exist_ok=True)
    (LATEX / f"main_{lec['stem']}_v5.tex").write_text(main, encoding="utf-8")


def archive_old_pdfs() -> Path | None:
    OUTPUT.mkdir(exist_ok=True)
    HISTORY.mkdir(parents=True, exist_ok=True)
    LATEST.mkdir(parents=True, exist_ok=True)
    old: List[Path] = []
    old += list(OUTPUT.glob("*.pdf"))
    old += list(LATEST.glob("*.pdf"))
    old += list(LATEX.glob("*.pdf"))
    # Avoid archiving current new files if script is run immediately after writing? called before compilation.
    old = [p for p in old if p.is_file()]
    if not old:
        return None
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = HISTORY / stamp
    dest.mkdir(parents=True, exist_ok=True)
    for p in old:
        sub = "latex" if LATEX in p.parents else ("latest" if LATEST in p.parents else "output_root")
        d = dest / sub
        d.mkdir(exist_ok=True)
        try:
            shutil.move(str(p), str(d / p.name))
        except Exception:
            shutil.copy2(p, d / p.name)
            p.unlink(missing_ok=True)
    return dest


def compile_pdf(lec: Dict[str, Any]) -> Path:
    tex = f"main_{lec['stem']}_v5.tex"
    for _ in range(2):
        cp = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex], cwd=LATEX, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if cp.returncode != 0:
            log_path = LATEX / f"main_{lec['stem']}_v5_compile_error.log"
            log_path.write_text(cp.stdout, encoding="utf-8")
            raise RuntimeError(f"xelatex failed for {tex}; see {log_path}\n{cp.stdout[-2000:]}")
    pdf = LATEX / f"main_{lec['stem']}_v5.pdf"
    out = LATEST / lec["out"]
    out.write_bytes(pdf.read_bytes())
    pdf.unlink(missing_ok=True)
    return out


def write_revision_doc(archived: Path | None) -> None:
    DOCS.mkdir(exist_ok=True)
    text = [
        "# Review v5 full-material generation", "",
        "## 目的", "",
        "全講義資料（Lecture 1-11）について、日本語訳・詳細解説・試験対策ポイント・確認問題・過去問演習を含むPDFを各回別に生成した。", "",
        "## 出力管理", "",
        "- 最新PDFは `output/latest/` にのみ保存する。", "- 過去版は `output/history/<timestamp>/` に移動する。", "- `latex/` にはPDF成果物を残さない。", "",
        "## 今回の過去版移動先", "", f"- {archived.relative_to(ROOT) if archived else '移動対象なし'}", "",
        "## 生成対象", "",
    ]
    for lec in LECTURES:
        text.append(f"- {lec['title']}: `output/latest/{lec['out']}`")
    (DOCS / "10_full_materials_v5.md").write_text("\n".join(text), encoding="utf-8")


def update_readme() -> None:
    path = ROOT / "README.md"
    old = path.read_text(encoding="utf-8") if path.exists() else "# DDDM Exam Notes Project\n"
    add = """

## PDF成果物の管理ルール（review v5以降）

PDF成果物は `latex/` には置かず、次の成果物フォルダで管理します。

```text
output/
├─ latest/   # 最新版PDFのみ。新しく生成するたびに中身を入れ替える
└─ history/  # 過去版PDF。生成時刻ごとのフォルダに退避
```

全講義PDFを生成するには、プロジェクトルートで次を実行します。

```bash
conda activate exam_26so
python scripts/generate_all_v5_notes.py
```

このスクリプトは、既存の `output/*.pdf`、`output/latest/*.pdf`、`latex/*.pdf` を `output/history/<timestamp>/` に退避してから、新しいPDFを `output/latest/` に出力します。
"""
    if "PDF成果物の管理ルール（review v5以降）" not in old:
        path.write_text(old.rstrip() + "\n" + add, encoding="utf-8")


def main() -> None:
    archived = archive_old_pdfs()
    for lec in LECTURES:
        print(f"Writing {lec['title']}")
        write_section(lec)
        write_main(lec)
        out = compile_pdf(lec)
        print(f"  -> {out.relative_to(ROOT)}")
    write_revision_doc(archived)
    update_readme()
    # Copy latest PDFs to /mnt/data as convenience links.
    for pdf in LATEST.glob("*.pdf"):
        shutil.copy2(pdf, ROOT.parent / pdf.name)
    print("Generated all v5 notes.")

if __name__ == "__main__":
    main()
