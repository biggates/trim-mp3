# 删除 mp3 头尾的空白

## 依赖项

请确认 PATH 中含有 ffmpeg 。

此外, 如果不需要使用 poetry 进行管理, 请手动安装如下 python 依赖项:

```cmd
> python -m pip install pydub rich-click
```

## 用法

准备好一个包含 mp3 文件的文件夹作为输入。

```cmd
> python cut.py --help

 Usage: cut.py [OPTIONS] INPUT_FOLDER

 将 mp3 文件头尾的安静片段删掉

╭─ Options ───────────────────────────────────────────────────────────────────────────╮
│ --output_folder         -o  PATH  指定输出的文件夹 [default: assets\output]           │
│ --dry-run/--no-dry-run            是否仅检测结果, 不执行任何操作 [default: no-dry-run] │
│ --verbose                         输出更多信息                                       │
│ --help                            Show this message and exit.                       │
╰─────────────────────────────────────────────────────────────────────────────────────╯

```

## 输出

在指定的输出文件夹中, 会生成
