# colorconv

> Convert colors between hex, RGB and HSL and check WCAG contrast ratios.

## Why

Halfway through a CSS change you need the HSL of a hex value, and then you need
to know whether the text on it is actually readable. Two questions, one file,
no browser devtools.

## Usage

```
python colorconv.py "#3b82f6"
python colorconv.py "rgb(59, 130, 246)"
python colorconv.py "hsl(217, 91%, 60%)"
python colorconv.py "#3b82f6" --contrast "#ffffff"
```

## Output

```
hex  #3b82f6
rgb  rgb(59, 130, 246)
hsl  hsl(217, 91%, 60%)

contrast with #ffffff
ratio 3.68:1  -> AA large text only
```
