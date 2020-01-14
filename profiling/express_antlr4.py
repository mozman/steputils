# Copyright (c) 2020 Manfred Moitzi
# License: MIT License

from pathlib import Path
import time
from steputils.express import Parser

DATAPATH = Path(r'..\data\schema').resolve()


class LoadResult:
    def __init__(self, filename: Path, content, loading_time: float, parsing_time: float = 0):
        self.filename = filename
        self.content = content
        self.loading_time = loading_time
        self.parsing_time = parsing_time

    def print(self):
        if self.content is None:
            print(f"{self.filename.name} is not an EXPRESS schema file.")
        else:
            size = self.filename.stat().st_size / 1024.
            overall = self.loading_time + self.parsing_time
            print(
                f"File: {self.filename.name}; "
                f" Size: {size:.2f} kB; "
                f"Parsing: {self.parsing_time:.2f}s; "
            )


def scan_express_schemas(p: Path):
    print(f"\nEntering Folder <{p.stem}>")
    start_time = time.perf_counter()
    for file in p.iterdir():
        if file.is_dir():
            scan_express_schemas(file)
        else:
            result = load_schema(file)
            result.print()
    run_time = time.perf_counter() - start_time
    print('-' * 79)
    print(f"Folder <{p.stem}> Runtime: {run_time:.2f} sec.")


def load_schema(fn: Path) -> LoadResult:
    if fn.suffix.lower() != '.exp':
        return LoadResult(fn, None, 0)
    content = None
    start_time = time.perf_counter()
    loaded = time.perf_counter()
    try:
        data = open(str(fn), mode='rt').read()
    except IOError as e:
        print(e)
    else:
        loaded = time.perf_counter()
        print(f'parsing {fn.stem} ...')
        parser = Parser(data)
        content = parser.schema()
    end_time = time.perf_counter()
    loading_time = loaded - start_time
    parsing_time = end_time - loaded
    return LoadResult(fn, content, loading_time, parsing_time)


if __name__ == '__main__':
    start_time = time.perf_counter()
    scan_express_schemas(DATAPATH)
    run_time = time.perf_counter() - start_time
    print(f"Overall Runtime: {run_time:.2f} sec.")
