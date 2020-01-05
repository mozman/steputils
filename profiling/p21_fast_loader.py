from pathlib import Path
import time
from steputils import p21

# p21 example files not included in public repository, because legal status of files is not clear
DIR = Path(r'..\data\p21examples').resolve()


class LoadResult:
    def __init__(self, filename: Path, content, loading_time: float, parsing_time: float = 0):
        self.filename = filename
        self.content = content
        self.loading_time = loading_time
        self.parsing_time = parsing_time

    def print(self):
        if self.content is None:
            print(f"{self.filename.name} is not as STEP-file.")
        else:
            size = self.filename.stat().st_size / 1024.
            overall = self.loading_time + self.parsing_time
            print(
                f"File: {self.filename.name}; "
                f" Size: {size:.2f} kB; "
                f"IO: {self.loading_time:.2f}s; "
                f"Parsing: {self.parsing_time:.2f}s; "
                f"Sum: {overall:.2f}s; "
            )


def scan_p21_files(p: Path):
    print(f"\nEntering Folder <{p.stem}>")
    start_time = time.perf_counter()
    for file in p.iterdir():
        if file.is_dir():
            scan_p21_files(file)
        else:
            result = load_p21(file)
            result.print()
    run_time = time.perf_counter() - start_time
    print('-' * 79)
    print(f"Folder <{p.stem}> Runtime: {run_time:.2f} sec.")


def load_p21(fn: Path) -> LoadResult:
    if fn.suffix.lower() not in ('.p21', '.ifc', '.stp'):
        return LoadResult(fn, None, 0)
    content = None
    start_time = time.perf_counter()
    loaded = time.perf_counter()
    try:
        data = open(str(fn), mode='rt', encoding=p21.STEP_FILE_ENCODING).read()
        loaded = time.perf_counter()
        content = p21.loads(data)
    except IOError as e:
        print(e)
    except p21.ParseError as e:
        print(e)
    end_time = time.perf_counter()
    loading_time = loaded - start_time
    parsing_time = end_time - loaded
    return LoadResult(fn, content, loading_time, parsing_time)


if __name__ == '__main__':
    start_time = time.perf_counter()
    scan_p21_files(DIR)
    run_time = time.perf_counter() - start_time
    print(f"Overall Runtime: {run_time:.2f} sec.")
