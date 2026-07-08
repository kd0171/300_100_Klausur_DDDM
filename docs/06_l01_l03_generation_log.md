# Lecture 1-3 generation log

## 対象

- Lecture 1: `Materials/2026/3DM_01_Overview_SS26.pdf`
- Lecture 2: `Materials/2026/3DM_02_Information-and-Decision-Modeling_SS26.pdf`
- Lecture 3: `Materials/2026/3DM_03_Uncertainty_SS26.pdf`

## 生成物

- `notes/3dm_01_overview_ss26.md`
- `notes/3dm_02_information_decision_modeling_ss26.md`
- `notes/3dm_03_uncertainty_ss26.md`
- `docs/05_l01_l03_exam_focus.md`
- `latex/main_l01_l03.tex`
- `latex/sections/l01_overview.tex`
- `latex/sections/l02_information_decision_modeling.tex`
- `latex/sections/l03_uncertainty.tex`
- `output/dddm_l01_l03_jp_exam_notes.pdf`

## 設計上の判断

Markdownはレビューと追記に適した主原稿として維持し、スライドは画像リンクで参照する。数式はLaTeX記法で保存する。

PDF出力用LaTeXでは、PNG画像を大量に埋め込む代わりに、元PDFの該当ページを直接参照する。これにより画質劣化を避け、PDF容量とコンパイル時間を抑える。

## レビュー観点

- スライド上半分と解説下半分の対応が自然か。
- 日本語訳が直訳すぎず、試験理解に役立つ形になっているか。
- 過去問関連の記述が、過去問対策に偏りすぎていないか。
- Lecture 2-3のモデル記号、確率分布、expectation、Monte Carlo の説明が十分か。
- 下半分の情報量が多すぎるページは、補足ページ化する必要があるか。

## 検証

`compile_latex.py` により `output/dddm_l01_l03_jp_exam_notes.pdf` を生成した。選択ページを画像レンダーし、スライド部分、本文部分、日本語フォント、数式表示に大きな崩れがないことを確認した。

## 2026-07-08 v2 formatting revision

User review requested a stronger structure and richer content. Applied changes:

- Lecture 1, 2, and 3 are now exported as separate PDFs:
  - `output/dddm_l01_overview_jp_exam_notes.pdf`
  - `output/dddm_l02_information_decision_modeling_jp_exam_notes.pdf`
  - `output/dddm_l03_uncertainty_jp_exam_notes.pdf`
- LaTeX format revised:
  - Clear item headers: `日本語訳`, `解説`, `試験対策ポイント`, `過去問関連`, `確認問題と解答`.
  - Headers use larger red text and are followed by line breaks.
  - Item groups are separated by paragraph spacing.
  - Translation section keeps slide bullet structure and avoids explanatory additions.
  - Two-column layout is used for note content.
  - Long past-exam sections may flow to additional pages.
- Content revised:
  - Concepts are explained at answer-ready level for beginners.
  - Related past exam items include year, question number, point value, problem focus, and expected answer.
  - Confirmation questions include detailed model answers.
- New generator:
  - `scripts/generate_l01_l03_structured_notes.py`
- New design note:
  - `docs/07_formatting_revision_l01_l03.md`
