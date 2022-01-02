# from analyzer import analyze
import sus
from pathlib import Path
def main():
    for sus_file in (Path('.') / 'tests').glob('*.sus'):
        with open(sus_file, 'r') as f:
            data = f.read()
        score = sus.loads(data)
        with open(sus_file.with_suffix('.json'), 'w') as f:
            f.write(score.to_json(indent=4))

if __name__ == '__main__':
    main()
