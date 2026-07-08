# Prompt: MarkdownからLaTeXへの変換

次のMarkdown学習ノートを、A4縦のPDF出力用LaTeXに変換してください。

## 変換方針

- Markdownを機械的に変換するのではなく、1ページに収まるように内容を整理してください。
- 1スライド=1PDFページを原則として維持してください。
- 上部に元スライド画像、下部に日本語訳・解説・試験ポイントを配置してください。
- 事務ページは軽く、理論ページは厚くしてください。
- 数式はLaTeX数式として保持してください。
- 過去問関連は、年度・Aufgabe/Exercise番号・何を理解すべきかを簡潔に残してください。
- 長すぎる説明は、本文ではなく「補足ページ」に分けてもよい。ただし本編の1対1対応は崩さないでください。

## LaTeX前提

- `xelatex` を使います。
- 日本語は `xeCJK` を使います。
- メインファイルは `latex/main.tex`、各講義は `latex/sections/*.tex` に分けます。
- スライド画像は `../assets/slides/...png` の相対パスを使います。

## ページテンプレート

```tex

otePage{<Slide title>}{<image path>}{%
  	extbf{日本語訳}\par
  ...

  \medskip
  	extbf{試験で確実に理解すべき点}\par
  ...

  \medskip
  	extbf{過去問との関連}\par
  ...
}
```

## 出力

- `latex/sections/<lecture_id>.tex` に入れる内容を出力してください。
- 必要があれば `latex/main.tex` の `\input{sections/...}` も更新してください。
