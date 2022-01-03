# sus-io

A SUS (Sliding Universal Score) parser and generator.

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

## Functionality
- Parse sus into tick-based objects.
- Allow json output.

## Usage

### ``sus.loads(data: str)``
```python
import sus

print(sus.loads("#00002: 4\n#BPM01: 120\n#00008: 01"))
```

### ``sus.load(fp: TextIO)``
```python
import sus

with open("score.sus", "r") as f:
    score = sus.load(f)
    print(score)
```

### ``Score(...).to_json(...)``, ``Score.from_json(...)``
```python
import sus
from sus import Score

with open("score.sus", "r") as fi, open("score.json", "w") as fo:
    score = sus.load(fi)
    json = score.to_json(indent=4)
    fo.write(json)

    print(Score.from_json(json))
```

### ``sus.dump(score: Score)``, ``sus.dumps(score: Score)``
```python
import sus

with open("score.sus", 'r') as fi, open(sus_file.with_suffix('.dumped.sus'), 'w') as fd:
    score = sus.load(fi)
    print(sus.dumps(score))
    sus.dump(score, fd, comment='Custom comment.', space=False)
```

## Todo

- Acknowledgement
- Add example I/O
- Contribution Guide
- High Speed
- etc.

## License

MIT © 2021 mkpoli
