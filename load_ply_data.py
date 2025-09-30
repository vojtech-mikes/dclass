import marimo

__generated_with = "0.16.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pathlib
    import plyfile
    import polars
    return pathlib, plyfile, polars


@app.cell
def _(pathlib, plyfile):
    source_dir = pathlib.Path("fixed_scans/").absolute()

    ply_files = {}

    for i in source_dir.iterdir():
        ply_files[i] = plyfile.PlyData.read(i)
    return (ply_files,)


@app.cell
def _():
    features = [
        "x",
        "y",
        "z",
        "intensity",
        "profile",
        "x_pos",
        "red",
        "green",
        "blue",
        "nir",
        "ndvi",
        "wvl1",
        "wvl2",
        "wvl3",
        "wvl4",
        "wvl5",
        "wvl6",
        "wvl7"
    ]
    return (features,)


@app.cell
def _(features, pathlib, ply_files, polars):
    schema = {
        "index": polars.String,
        "x": polars.Float32,
        "y": polars.Float32,
        "z": polars.Float32,
        "intensity": polars.UInt32,
        "profile": polars.Int32,
        "x_pos": polars.Int32,
        "red": polars.UInt32,
        "green": polars.UInt32,
        "blue": polars.UInt32,
        "nir": polars.UInt32,
        "ndvi": polars.UInt32,
        "wvl1": polars.UInt32,
        "wvl2": polars.UInt32,
        "wvl3": polars.UInt32,
        "wvl4": polars.UInt32,
        "wvl5": polars.UInt32,
        "wvl6": polars.UInt32,
        "wvl7": polars.UInt32,
    }


    big_df = polars.DataFrame(schema=schema)

    for path, plant in ply_files.items():
        data = {"index": pathlib.Path(path).stem}
        for f in features:
            data[f] = plant.elements[0].data[f]
        df = polars.DataFrame(data, schema=schema)
        big_df = polars.concat([big_df, df], how="vertical_relaxed")
    return (big_df,)


@app.cell
def _(big_df):
    big_df.write_delta("./data/all_plants", mode="overwrite")

    big_df
    return


if __name__ == "__main__":
    app.run()
