# sus-io

A SUS (Sliding Universal Score) parser and generator.

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

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

### ``Score(...).to_json(...)``
```python
import sus

with open("score.sus", "r") as fi, open("score.json", "w") as fo:
    score = sus.load(fi)
    json = score.to_json(indent=4)
    fo.write(json)
```

## Todo

- json -> dict of objects -> sus
- Acknowledgement
- Add example I/O
- Contribution Guide
- High Speed
- etc.

## License

MIT © 2021 mkpoli
