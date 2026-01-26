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

## Contrast

The ratio is WCAG 2.1 relative luminance, the same number browsers and
accessibility auditors report.

| ratio | verdict |
|-------|---------|
| ≥ 7.0 | AAA |
| ≥ 4.5 | AA — normal body text |
| ≥ 3.0 | AA for large text (18pt+, or 14pt bold) only |
| < 3.0 | fail |

## Accepted input

`#rgb`, `#rrggbb`, with or without the `#`, `rgb(…)` / `rgba(…)`, and
`hsl(…)` / `hsla(…)`. Alpha is parsed and ignored — contrast against a
semi-transparent color depends on what is behind it.
