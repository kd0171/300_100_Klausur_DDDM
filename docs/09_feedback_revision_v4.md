# Review v4 revision

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
