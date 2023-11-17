import csv

from pathlib import Path

from sys import argv


def split_csv(file_path: Path, lines: int = 1000) -> None:
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        chunk: list[list[str]] = []
        for i, row in enumerate(reader):
            if (i % lines) == 0 and i > 0:
                with open('file_{}.csv'.format(i // lines), 'w',
                          newline='') as chunk_file:
                    writer = csv.writer(chunk_file)
                    writer.writerow(headers)
                    writer.writerows(chunk)
                chunk = []
            chunk.append(row)
        with open('file_{}.csv'.format((i // lines) + 1), 'w',
                  newline='') as chunk_file:
            writer = csv.writer(chunk_file)
            writer.writerow(headers)
            writer.writerows(chunk)


if __name__ == '__main__':
    if len(argv) > 1:
        split_csv(Path(argv[1]))
    else:
        raise ValueError('No file path provided')
