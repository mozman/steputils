from pathlib import Path
import time
from steputils.scl.part21 import readfile

# p21 example files not included in public repository, because legal status of files is not clear
DIR = Path(r'..\data\p21examples').resolve()


class LoadResult:
    def __init__(self, filename: Path, content, loading_time: float):
        self.filename = filename
        self.content = content
        self.loading_time = loading_time

    def print(self):
        if self.content is None:
            print(f"{self.filename.name} is not as STEP-file.")
        else:
            size = self.filename.stat().st_size / 1024.
            print(f"File: {self.filename.name}; Size: {size:.2f} kB; Loading Time: {self.loading_time:.2f} sec.")


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
    print('-'*79)
    print(f"Folder <{p.stem}> Runtime: {run_time:.2f} sec.")


def load_p21(fn: Path) -> LoadResult:
    if fn.suffix.lower() not in ('.p21', '.ifc', '.stp'):
        return LoadResult(fn, None, 0)
    content = None
    start_time = time.perf_counter()
    try:
        content = readfile(str(fn))
    except IOError as e:
        print(e)

    end_time = time.perf_counter()
    loading_time = end_time - start_time
    return LoadResult(fn, content, loading_time)


if __name__ == '__main__':
    start_time = time.perf_counter()
    scan_p21_files(DIR)
    run_time = time.perf_counter() - start_time
    print(f"Overall Runtime: {run_time:.2f} sec.")
