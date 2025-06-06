"""Script to download open legal datasets."""

import requests

DATASETS = {
    'Indian_Law': 'https://raw.githubusercontent.com/awsm-research/Indian-Law-Dataset/main/data/sample.jsonl'
}


def download():
    for name, url in DATASETS.items():
        resp = requests.get(url, timeout=10)
        outfile = f'{name}.jsonl'
        with open(outfile, 'wb') as f:
            f.write(resp.content)
        print(f"Saved {outfile}")


if __name__ == '__main__':
    download()
