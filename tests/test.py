# from analyzer import analyze
import sus
from pathlib import Path
def main():
    for sus_file in (Path('.') / 'tests').glob('*.sus'):
        if sus_file.name.endswith('.d.sus'):
            continue

        print('----------------------------------------------------------------')
        print(f'  {sus_file.name}')
        print(f'---------------------------------------------------------------')

        with (
            open(sus_file, 'r') as fi,
            open(sus_file.with_suffix('.json'), 'w') as fo,
            open(sus_file.with_suffix('.d.sus'), 'w') as fd
        ):
            score = sus.load(fi)
            fo.write(score.to_json(indent=4))
            
            sus.dump(score, fd, comment='Custom comment.', space=True)
        print('----------------------------------------------------------------')
        print()
        print()

if __name__ == '__main__':
    main()
