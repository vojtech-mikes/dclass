import marimo

__generated_with = "0.16.3"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Notebook that fixes headers in the PLY files and changes name of the files to corespond with experiment notes.""")
    return


@app.cell
def _():
    import marimo as mo
    from pathlib import Path
    import pathlib
    import re
    from datetime import date
    import os
    return Path, mo, os


@app.cell
def _():
    return


@app.cell
def _(Path, os):
    scans_lookup = {}

    target_path = Path("./fixed_scans").absolute()

    for f in Path("processed_scans").iterdir():
        if not f.is_file():
            continue

        parts = f.name.split("_")
        barcode, ext = parts[-1].split(".")
        part1, part2 = barcode.split("-")

        new_name = os.path.join(
            target_path, f"{parts[0]}-{part2}-{int(part1) + 1}_{parts[4]}.{ext}"
        )
        scans_lookup[f.absolute()] = new_name
    return (scans_lookup,)


@app.function
def modify_ply_from_Phenospex(input_filename, output_filename):
    """
    read Phenospex point cloud PLY file
    read header from input file, delete SPACE in header, write to output file in PLY format

    author: Serkan Kartal
    """

    with open(input_filename, "br") as f:  # open input file
        s = f.read()
        end_spaces = s.find(
            b"\x65\x6e\x64\x5f\x68\x65\x61\x64\x65\x72\x0a"
        )  # find end_heder
        start_spaces = (
            s.find(b"\x76\x65\x72\x74\x65\x78\x5f\x69\x6e\x64\x65\x78\x0a") + 13
        )  # find sequence of spaces
        s = s.replace(s[:end_spaces], s[:start_spaces])  # delete spaces
        f.close()
    with open(output_filename, "bw") as f:  # write modified content to output file
        f.write(s[::])
        f.close()

    return output_filename


@app.cell
def _(scans_lookup):
    for k, v in scans_lookup.items():
        modify_ply_from_Phenospex(k, v)
    return


if __name__ == "__main__":
    app.run()
