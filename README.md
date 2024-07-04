# 删除 mp3 头尾的空白

## 依赖项

请下载 ffmpeg.exe 放到项目目录中

## 用法

```
> python cut.py --help

 Usage: cut.py [OPTIONS] INPUT_FOLDER

 将 mp3 文件头尾的安静片段删掉

╭─ Options ─────────────────────────────────────────────────────────────────────╮
│ --output_folder         -o  PATH  指定输出的文件夹 [default: assets\output]     │
│ --dry-run/--no-dry-run            是否仅检测结果, 不执行任何操作                 │
│ --verbose                         输出更多信息                                 │
│ --help                            Show this message and exit.                 │
╰───────────────────────────────────────────────────────────────────────────────╯

```