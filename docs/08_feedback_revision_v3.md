# Review v3 formatting revision

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
