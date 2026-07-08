# DDDM Exam Learning System

Data Driven Decision Making の講義スライドを、**1スライド=1学習ページ**として日本語訳・解説・試験対策ポイント付きに変換するためのプロジェクトです。

このプロジェクトでは、Markdown を主原稿にします。スライド画像は Markdown には埋め込まず、相対パスだけを記載します。数式は Markdown 内でも LaTeX 記法で書きます。最終PDF化するときだけ、ChatGPT が Markdown の意味内容を LaTeX に変換し、Python は LaTeX のコンパイルだけを担当します。

## 1. 推奨ディレクトリ構成

```text
learning_system_dddm_exam_project/
├─ Materials/
│  ├─ 2026/                         # 元講義PDF。編集しない
│  └─ Altklausuren/                  # 過去問PDF。編集しない
├─ assets/slides/                 # PDFから書き出したスライド画像
├─ notes/                         # Markdown学習ノート。ここを主原稿にする
├─ latex/                         # ChatGPTが生成するLaTeX出力
│  ├─ main.tex
│  └─ sections/
├─ scripts/                       # 画像書き出し・雛形作成・PDFコンパイル
├─ docs/                          # 設計方針・過去問重要論点
├─ prompts/                       # ChatGPTに渡す作業プロンプト
├─ data/                          # source inventory / exam question index
├─ build/                         # LaTeX中間ファイル
└─ output/                        # 生成PDF
```

## 2. Anaconda環境の作成

```bash
conda create -n exam_26so python=3.11 -y
conda activate exam_26so
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

LaTeXからPDFを生成するには、Pythonパッケージとは別に TeX Live または MiKTeX が必要です。Windowsでは MiKTeX、Linux/macOSでは TeX Live が扱いやすいです。`latexmk` と `xelatex` がPATHから実行できる状態にしてください。

確認:

```bash
xelatex --version
latexmk --version
```

## 3. スライド画像の作成

全講義PDFから画像を書き出す場合:

```bash
python scripts/export_slide_images.py --pdf-dir Materials/2026 --out-dir assets/slides --dpi 180 --skip-duplicates
```

特定PDFだけ処理する場合:

```bash
python scripts/export_slide_images.py --pdf Materials/2026/3DM_01_Overview_SS26.pdf --out-dir assets/slides --dpi 180
```

画像名は次の形式で作成されます。

```text
assets/slides/3dm_01_overview_ss26/3dm_01_overview_ss26_p001.png
assets/slides/3dm_01_overview_ss26/3dm_01_overview_ss26_p002.png
```

## 4. Markdownノート雛形の作成

```bash
python scripts/create_note_skeletons.py --pdf-dir Materials/2026 --slides-dir assets/slides --notes-dir notes --skip-duplicates
```

各スライドについて次の構造が作成されます。

```md
## Slide 001

![slide](../assets/slides/.../xxx_p001.png)

### 日本語訳

### 解説

### 試験で確実に理解すべき点

### 過去問との関連

### 確認問題
```

## 5. ChatGPTによる Markdown → LaTeX 変換

このプロジェクトでは、MarkdownからLaTeXへの変換は自動スクリプトに任せません。理由は、単なる記法変換ではなく、次のような意味的判断が必要だからです。

- 下半分に入る訳・解説をページ内に収める。
- 過去問に関係する箇所では、どの年度・第何問と関連するかを明示する。
- 数式ページでは、記号一覧・直感的説明・試験での使い方を追加する。
- 事務連絡ページは軽く、理論ページは厚くする。

作業時は `prompts/md_to_latex_prompt.md` をChatGPTに渡してください。

## 6. LaTeXからPDFへの変換

ChatGPTが `latex/main.tex` と `latex/sections/*.tex` を作成したあと、次を実行します。

```bash
python scripts/compile_latex.py --tex latex/main.tex --out-dir output --build-dir build
```

生成物:

```text
output/main.pdf
```

## 7. 最初に読むべき設計ドキュメント

- `docs/00_project_design.md`
- `docs/01_workflow_md_latex_pdf.md`
- `docs/02_note_page_template.md`
- `docs/03_past_exam_important_topics.md`
- `docs/04_question_index.md`

## 8. 注意

- 過去問は参考です。過去問に出た内容だけを覚えるのではなく、講義全体のモデル化能力を優先します。
- Lecture 6 は追加アップロードされた `Materials/2026/3DM_06_ADP_SS26.pdf` を正本として追加済みです。
- Lecture 7 は `Materials/2026/3DM_07_Lookahead-Methods_SS26.pdf` を正本として確認済みです。旧重複ファイルは削除しました。
- 通常は `--skip-duplicates` を付けたまま実行すると、将来同じPDFを誤って追加した場合も二重出力を避けられます。

## 9. Review run: Lecture 1-3

Lecture 1-3について、レビュー用の日本語訳・解説・試験対策ノートを生成済みです。

生成済みファイル:

```text
notes/3dm_01_overview_ss26.md
notes/3dm_02_information_decision_modeling_ss26.md
notes/3dm_03_uncertainty_ss26.md
docs/05_l01_l03_exam_focus.md
latex/main_l01_l03.tex
latex/sections/l01_overview.tex
latex/sections/l02_information_decision_modeling.tex
latex/sections/l03_uncertainty.tex
output/dddm_l01_l03_jp_exam_notes.pdf
```

再生成する場合:

```bash
python scripts/export_slide_images.py --pdf Materials/2026/3DM_01_Overview_SS26.pdf --out-dir assets/slides --dpi 160 --index data/slide_image_index_l01.csv
python scripts/export_slide_images.py --pdf Materials/2026/3DM_02_Information-and-Decision-Modeling_SS26.pdf --out-dir assets/slides --dpi 160 --index data/slide_image_index_l02.csv
python scripts/export_slide_images.py --pdf Materials/2026/3DM_03_Uncertainty_SS26.pdf --out-dir assets/slides --dpi 160 --index data/slide_image_index_l03.csv

python scripts/generate_l01_l03_review_notes.py
python scripts/compile_latex.py --tex latex/main_l01_l03.tex --out-dir output --build-dir build --jobname dddm_l01_l03_jp_exam_notes
```

Markdownノートでは、スライド画像への相対リンクを保持しています。一方、LaTeX出力ではPDF容量と画質を安定させるため、元PDFの各ページを `\includegraphics[page=...]` で直接参照しています。これはプロジェクト方針と矛盾しません。Markdownは編集・レビュー用、LaTeXは最終PDF化用です。


## Lecture 1-3 structured review PDFs

After the first quality review, Lecture 1-3 can be regenerated with a more structured layout and richer exam-oriented content:

```bash
conda activate exam_26so
python scripts/generate_l01_l03_structured_notes.py
```

This creates separate PDFs:

```text
output/dddm_l01_overview_jp_exam_notes.pdf
output/dddm_l02_information_decision_modeling_jp_exam_notes.pdf
output/dddm_l03_uncertainty_jp_exam_notes.pdf
```

The revised layout uses these sections per slide when relevant:

1. 日本語訳
2. 解説
3. 試験対策ポイント
4. 過去問関連
5. 確認問題と解答

For cover, agenda, and administrative pages, explanatory/exam sections are intentionally omitted unless they are useful.
