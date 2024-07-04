# 该文件读指定的 mp3 文件, 并将每个文件头尾的安静段删掉
# 用法:
# python cut.py [mp3文件路径]

from pathlib import Path
from typing import Tuple

import rich_click as click
from pydub import AudioSegment, silence
from rich import print
from rich.progress import track


def cut_one(
    mp3_file: Path,
    dest_path: Path,
    padding: int = 0,
    dry_run: bool = True,
    verbose: bool = False,
) -> Tuple[Path, int]:
    # 读 mp3
    segment = AudioSegment.from_mp3(mp3_file)

    # 检测安静片段, 注意这些参数可能是需要调节的
    silenced_slices = silence.detect_silence(
        segment,
        min_silence_len=100,
        silence_thresh=-32,
        seek_step=10,
    )

    if verbose:
        print(
            f"检查到 {mp3_file.name} (时长为 {len(segment)} ms) 的安静段: {silenced_slices}"
        )

    result_path = mp3_file
    result_duration_ms = len(segment)

    if not dry_run:
        # 将结果写入文件
        result_path = dest_path / mp3_file.name

        if silenced_slices is not None and len(silenced_slices) > 0:
            # 至少有一个安静片段才有价值
            headhead = silenced_slices[0][0]
            head = silenced_slices[0][1]
            tail = silenced_slices[-1][0]
            tailtail = silenced_slices[-1][-1]

            # 为了防止删掉本来就在头部和尾部的数据, 再对 head 和 tail 做一些限制
            if headhead != 0:
                head = 0

            if tail == 0 or tailtail != len(segment):
                tail = len(segment)

            head = max(0, head - padding)
            tail = min(len(segment), tail + padding)

            if verbose:
                print(f"实际用于切割的参数为: {head} - {tail}")

            center_segment = segment[head:tail]
        else:
            center_segment = segment

        result_duration_ms = len(center_segment)

        with open(result_path, "wb") as f:
            center_segment.export(f, format="mp3")

    return result_path, result_duration_ms


@click.command(help="将 mp3 文件头尾的安静片段删掉")
@click.argument(
    "input_folder",
    type=click.Path(exists=True, dir_okay=True, path_type=Path),
)
@click.option(
    "--output_folder",
    "-o",
    type=click.Path(exists=True, dir_okay=True, path_type=Path),
    required=False,
    default=Path("./assets/output/"),
    show_default=True,
    help="指定输出的文件夹",
)
@click.option(
    "--dry-run/--no-dry-run",
    is_flag=True,
    default=False,
    required=False,
    show_default=True,
    help="是否仅检测结果, 不执行任何操作",
)
@click.option(
    "--verbose",
    type=bool,
    is_flag=True,
    default=False,
    required=False,
    help="输出更多信息",
)
def main(
    input_folder: Path,
    output_folder: Path = Path("./assets/output/"),
    dry_run: bool = False,
    verbose: bool = False,
):
    all_files = list(input_folder.glob("*.mp3"))

    out_lines = []
    out_lines.append("file_name,duration_ms")

    output_folder.mkdir(parents=True, exist_ok=True)

    for mp3_file in track(all_files, total=len(all_files)):
        out_path, out_duration_ms = cut_one(
            mp3_file,
            dest_path=output_folder,
            dry_run=dry_run,
            verbose=verbose,
        )

        out_lines.append(f"{out_path.name},{out_duration_ms}")

    out_lines.append("")

    # 生成 summary.csv
    with open(output_folder / "summary.csv", "w") as f:
        f.write("\n".join(out_lines))

    print("操作完成")


if __name__ == "__main__":
    main()
