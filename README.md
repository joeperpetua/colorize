# Colorize PNG

A CLI tool to colorize PNG images to a solid target color while preserving transparency. It supports processing single files, batch processing via wildcards, and scanning entire directories.

## Features

- Colorize PNGs while perfectly preserving their alpha channel transparency.
- Supports batch operations for multiple files or directories.
- Accepts target colors in HEX format (e.g., `#FF0000`) or standard CSS color names (e.g., `blue`, `green`).
- Save to a new file/directory, or overwrite the original images in-place.

## Requirements

- Python >= 3.7
- Pillow >= 9.0.0

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/joeperpetua/colorize-png.git
   cd colorize-png
   ```

2. **Install via pip:**
   ```sh
   pip install .
   ```
   *Note: This will install the dependencies and make the `colorize` command globally available in your terminal.*

## Usage

```sh
colorize -i <input_path> -c <color> [-o <output_path>]
```

### Options

| Flag | Name | Description |
|---|---|---|
| `-i`, `--input` | Input Path | Path to source PNG(s), or a directory containing PNGs. Supports multiple arguments and wildcards (e.g. `*.png`). **(Required)** |
| `-c`, `--color` | Target Color | Target color in HEX format or CSS color name. **(Required)** |
| `-o`, `--output` | Output Path | Output file (if single input) or output directory (if multiple inputs). If omitted, overwrites in place. |

### Examples

**Colorize a single image to blue:**
```sh
colorize -i icon.png -c blue
```

**Colorize multiple files to red and save them in a specific directory:**
```sh
colorize -i *.png -c '#FF0000' -o ./red_icons/
```

**Colorize all PNGs inside a folder to green (overwrites in place):**
```sh
colorize -i ./my_folder/ -c green
```
