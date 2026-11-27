# Colour fonts

This project is an attempt to build COLRv0 versions of emoji fonts.

Currently, it builds a COLRv0 version of
[@jdecked’s fork of Twemoji](https://github.com/jdecked/twemoji).

COLRv0 refers to version 0 of the
[OpenType COLR table](https://learn.microsoft.com/en-gb/typography/opentype/spec/colr).
It essentially allows layering glyphs in different colours to produce a single
multicoloured glyph.

COLRv0 is targeted as it is more compatible than COLRv1.

[nanoemoji](https://github.com/googlefonts/nanoemoji) is used to build fonts from input
SVG files.

## Building fonts

1. Install Python 3.14 using your preferred method.
   ([Official installers for some operating systems.](https://www.python.org/downloads/))

2. [Install uv](https://docs.astral.sh/uv/getting-started/installation/).

3. Run:

   ```bash
   uv sync
   ```

4. Run:
   ```bash
   uv run twemoji/build.py
   ```

If the command is successful, the built fonts will in the `twemoji/dist` directory.

Two fonts are built:

- `twemoji-colrv0.ttf` – the standard version will all emojis
- `twemoji-colrv0--no-keycap.ttf` - a version with emoji sequences for digits and some
  other characters removed (see [twemoji/post.toml](./twemoji/post.toml) for a list of
  removed code points)

`twemoji-colrv0--no-keycap.ttf` will allow font fallback to be used for digits and the
other omitted characters, but will not have support for emoji versions of those
characters such as keycap emojis. With `twemoji-colrv0.ttf`, the non-emoji versions of
those characters may not render.

## Contributing

This repository uses [lefthook](https://lefthook.dev) for pre-commit hooks.

For the pre-commit hooks to run, you need to
[install Node.js](https://nodejs.org/en/download) and run:

```bash
npm install
uv run lefthook install
```

## Licence

This repo is released under the [MIT License](./LICENCE).

Built fonts and their sources have their own licence:

- [Licence information for @jdecked’s fork of Twemoji](https://github.com/jdecked/twemoji#license)
