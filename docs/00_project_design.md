# 00 Project design: DDDM学習ノート作成方針

## 目的

このプロジェクトの目的は、Data Driven Decision Making の講義PDFを、試験対策に使える日本語の学習ノートへ変換することです。

完成形は、**元スライドの視覚情報を保持しつつ、下部に日本語訳・解説・試験対策ポイントを付けたPDF**です。原則として **1スライド=1学習ページ** で対応させます。

## なぜMarkdownを主原稿にするか

MarkdownはChatGPTとの共同編集に向いています。

- 章・スライド単位で構造化しやすい。
- 日本語訳、解説、確認問題、過去問関連を分けて書きやすい。
- Gitで差分管理しやすい。
- 数式はLaTeX記法で書ける。
- 画像は相対パスだけを置ける。

ただし、MarkdownだけではPDFのレイアウトを厳密に制御しにくいため、最終PDFはLaTeXで生成します。

## 基本ワークフロー

```text
元PDF
  ↓ Python: スライド画像を書き出し・命名
assets/slides/*.png
  ↓ Python: Markdownノート雛形作成
notes/*.md
  ↓ ChatGPT: 日本語訳・解説・過去問関連・確認問題を執筆
notes/*.md
  ↓ ChatGPT: MarkdownをLaTeXへ意味的に変換
latex/main.tex, latex/sections/*.tex
  ↓ Python: xelatex/latexmkを呼び出し
output/*.pdf
```

## 役割分担

### Pythonが担当すること

- PDFページを画像化する。
- 画像ファイルを規則的に命名する。
- Markdown雛形を作る。
- LaTeXをPDFにコンパイルする。
- source inventoryやquestion indexのような機械的データを保存する。

### ChatGPTが担当すること

- スライド内容の日本語訳。
- 試験で理解すべき概念の解説。
- 過去問との対応付け。
- MarkdownからLaTeXへの意味的変換。
- ページ内に収まるように内容を圧縮する判断。

MarkdownからLaTeXへの変換を完全自動化しない理由は、学習ノート作成では単なる形式変換ではなく、内容の取捨選択・圧縮・強調が必要だからです。

## 1ページの標準レイアウト

A4縦を想定します。

```text
┌──────────────────────────┐
│ 元スライド画像             │  上部 40-45%
├──────────────────────────┤
│ 日本語訳                   │
│ 解説                       │  下部 55-60%
│ 試験で確実に理解すべき点     │
│ 過去問との関連              │
│ 確認問題                   │
└──────────────────────────┘
```

## ページタイプ別の濃淡

### 事務情報ページ

連絡先、試験情報、過去問入手方法などは簡潔にまとめます。

- 日本語訳
- 行動メモ
- 注意点

### 理論ページ

Motivation, stochasticity, dynamism, MDP, ADP, VFAなどは厚めに書きます。

- 日本語訳
- 概念の説明
- 典型的な試験答案の観点
- 過去問との関連
- 確認問題

### 図解ページ

Information Model / Decision Model / Real World loop などは、図の各要素を対応付けます。

- 図の読み方
- 各ブロックの意味
- 矢印の意味
- 答案で使える説明文

### 数式ページ

Bellman equation, MDP, value function, dynamic programming などは次を追加します。

- 式そのもの
- 記号一覧
- 式の意味
- 直感的説明
- 試験で問われるポイント

## 画像と数式の原則

- スライド画像はMarkdownにバイナリとして埋め込まない。
- 画像は `assets/slides/<lecture_id>/<lecture_id>_pXXX.png` に保存する。
- Markdownでは相対パスだけを書く。
- 数式は `$...$` または `$$...$$` のLaTeX記法で書く。
- 数式をスクリーンショットで保存しない。

## 過去問の扱い

過去問は「出題傾向を知るための材料」であり、暗記対象を限定するものではありません。

各ノートページの `### 過去問との関連` では、次の形式で書きます。

```md
- SS24 Aufgabe 1a と関連。
  - 関連点: Information Model, Decision Model, Aggregation, Disaggregationの機能が問われた。
  - 必要理解: 4要素を定義するだけでなく、現実世界から意思決定モデルへ情報が流れる構造を説明できること。
```

## 今年の資料上の注意

- Lecture 6 `Approximate Dynamic Programming` は、追加アップロードされた `Materials/2026/3DM_06_ADP_SS26.pdf` を正本として追加済みです。
- Lecture 7 `Look-ahead Methods` は、`Materials/2026/3DM_07_Lookahead-Methods_SS26.pdf` を正本として確認済みです。重複ファイルは削除済みです。
