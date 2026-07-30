import argparse
import sys
import os
from PIL import Image, ImageColor

def colorize(input_path, output_path, target_color):
    """Processes a single image."""
    try:
        img = Image.open(input_path).convert("RGBA")
        alpha = img.split()[3]
        
        solid_color = target_color + (255,) if len(target_color) == 3 else target_color
        colorized_img = Image.new("RGBA", img.size, solid_color)
        
        colorized_img.putalpha(alpha)
        colorized_img.save(output_path)
        
        return True, output_path
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(
        description="A CLI tool to colorize PNG images while preserving transparency. Supports bulk processing.",
        epilog="Examples:\n  colorize -i icon.png -c blue\n  colorize -i *.png -c '#FF0000' -o ./red_icons/\n  colorize -i ./my_folder/ -c green",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # nargs='+' allows one or more arguments (e.g., file1.png file2.png or *.png)
    parser.add_argument("-i", "--input", nargs='+', required=True, help="Path to source PNG(s), or a directory containing PNGs")
    parser.add_argument("-c", "--color", required=True, help="Target color in HEX format or CSS color name")
    parser.add_argument("-o", "--output", help="Output file (if single input) or output directory (if multiple inputs). If omitted, overwrites in place.")

    args = parser.parse_args()

    # 1. Parse the target color once for all images
    try:
        target_color = ImageColor.getrgb(args.color)
    except ValueError:
        print(f"❌ Error: Invalid color format '{args.color}'. Use hex (e.g., '#FF0000') or names.", file=sys.stderr)
        sys.exit(1)

    # 2. Gather all files to process (handling directories and wildcards)
    files_to_process = []
    for path in args.input:
        if os.path.isdir(path):
            # If it's a directory, grab all PNGs inside it
            for f in os.listdir(path):
                if f.lower().endswith('.png'):
                    files_to_process.append(os.path.join(path, f))
        elif os.path.isfile(path):
            files_to_process.append(path)
        else:
            print(f"⚠️ Warning: '{path}' is not a valid file or directory. Skipping.")

    if not files_to_process:
        print("❌ Error: No valid PNG files found to process.", file=sys.stderr)
        sys.exit(1)

    # 3. Determine output directory logic
    multiple_files = len(files_to_process) > 1
    if args.output and multiple_files:
        # If outputting multiple files to a target, ensure the target is a directory
        os.makedirs(args.output, exist_ok=True)
        print(f"📁 Outputting to directory: {args.output}")

    # 4. Process the files
    success_count = 0
    for in_file in files_to_process:
        # Determine the correct output path for this specific file
        if args.output:
            if multiple_files or os.path.isdir(args.output):
                # Save into the target directory with the original filename
                filename = os.path.basename(in_file)
                out_file = os.path.join(args.output, filename)
            else:
                # Single file to single specific output name
                out_file = args.output
        else:
            # Overwrite in place
            out_file = in_file

        # Run the colorizer
        success, msg = colorize(in_file, out_file, target_color)
        
        if success:
            action = "Updated" if in_file == out_file else "Saved"
            print(f"✅ {action}: {out_file}")
            success_count += 1
        else:
            print(f"❌ Failed '{in_file}': {msg}", file=sys.stderr)

    print(f"\n🎉 Done! Successfully colorized {success_count}/{len(files_to_process)} images.")

if __name__ == "__main__":
    main()