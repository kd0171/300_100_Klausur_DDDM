# 01 Workflow: Markdown → LaTeX → PDF

## 全体方針

このプロジェクトでは、Markdownを「内容のマスター」とし、LaTeXを「PDF出力用の最終形式」とします。

```text
notes/*.md  = 内容の主原稿
latex/*.tex = ChatGPTがPDF用に整えた出力形式
output/*.pdf = 最終成果物
```

## Step 1: スライド画像の作成

```bash
python scripts/export_slide_images.py --pdf-dir Materials/2026 --out-dir assets/slides --dpi 180 --skip-duplicates
```

画像命名規則:

```text
assets/slides/<lecture_id>/<lecture_id>_p001.png
```

例:

```text
assets/slides/3dm_05_mdp_ss26/3dm_05_mdp_ss26_p014.png
```

## Step 2: Markdown雛形の作成

```bash
python scripts/create_note_skeletons.py --pdf-dir Materials/2026 --slides-dir assets/slides --notes-dir notes --skip-duplicates
```

この段階では、訳や解説は空欄です。

## Step 3: ChatGPTでノート本文を作る

各 `notes/*.md` について、スライド内容を読み、日本語訳・解説・試験対策ポイントを埋めます。

特に重要な講義では、`docs/03_past_exam_important_topics.md` を参照し、過去問との対応も明記します。

## Step 4: ChatGPTでLaTeX化する

`prompts/md_to_latex_prompt.md` を使い、MarkdownをLaTeXに変換します。

この変換は機械的に行いません。理由は次の通りです。

- ページ下半分に収まるように説明を圧縮する必要がある。
- 過去問との関連は、単純な文字列変換ではなく概念対応を判断する必要がある。
- 数式ページでは、記号一覧や直感的説明を補う必要がある。
- 事務ページと理論ページで情報量を変える必要がある。

## Step 5: LaTeXからPDFを生成

```bash
python scripts/compile_latex.py --tex latex/main.tex --out-dir output --build-dir build
```

## Markdown記法ルール

### 画像

```md
![Slide 014](../assets/slides/3dm_05_mdp_ss26/3dm_05_mdp_ss26_p014.png)
```

### インライン数式

```md
状態を $S_t$、決定を $x_t$ と表す。
```

### ブロック数式

```md
$$
V_t(S_t) = \max_{x_t \in X_t(S_t)} \mathbb{E}\left[ C(S_t, x_t, W_{t+1}) + V_{t+1}(S_{t+1}) 
ight]
$$
```

### 過去問関連

```md
### 過去問との関連

- SS24 Aufgabe 3c と関連。
  - 関連点: Bellman方程式と、状態・遷移が増えたときに計算不能になる部分が問われた。
  - 必要理解: max演算、期待値計算、遷移列挙がどこに現れるかを説明できること。
```

## LaTeX設計ルール

- エンジンは `xelatex` を前提にする。
- 日本語には `xeCJK` を使う。
- スライド画像は `\includegraphics` で読み込む。
- 画像ファイルを使う場合は `assets/slides/...png` を参照する。
- 元PDFページを直接埋め込みたい場合は、次の形式も可。

```tex
\includegraphics[page=5,width=\linewidth,height=.43\textheight,keepaspectratio]{../Materials/2026/3DM_01_Overview_SS26.pdf}
```

大量のPNGを作りたくない場合、LaTeXでは元PDFページを直接埋め込む方が軽いです。ただしMarkdown段階では画像リンクの方がプレビューしやすいため、学習ノート作成時はPNG画像を使う方針にします。
