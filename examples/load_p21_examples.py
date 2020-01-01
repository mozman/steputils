from pathlib import Path
from datetime import timedelta, datetime
from steputils.stepfile import Factory as sf
from pyparsing import ParseException

# p21 example files not included in public repository, because legal status of files is not clear
DIR = Path(r'..\data\p21examples').resolve()


class LoadResult:
    def __init__(self, filename: Path, content, loading_time: timedelta):
        self.filename = filename
        self.content = content
        self.loading_time = loading_time

    def print(self):
        if self.content is None:
            print(f"{self.filename.name} is not as STEP-file.")
        else:
            size = self.filename.stat().st_size / 1024.
            print(f"File: {self.filename.name}; Size: {size:.2f} kB; Loading Time: {self.loading_time.seconds} sec.")


def scan_p21_files(p: Path):
    for file in p.iterdir():
        if file.is_dir():
            scan_p21_files(file)
        else:
            result = load_p21(file)
            result.print()


def load_p21(fn: Path) -> LoadResult:
    content = None
    start_time = datetime.now()
    try:
        content = sf.readfile(str(fn))
    except IOError as e:
        print(e)
    except ParseException:
        pass

    end_time = datetime.now()
    loading_time = end_time - start_time
    return LoadResult(fn, content, loading_time)


if __name__ == '__main__':
    scan_p21_files(DIR)
