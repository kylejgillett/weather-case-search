# Chase Case Search

API to expose fuzzy search capability for storm chase cases.

### Prerequisites

* Python >= 3.12
* Docker (optional for development)
* [Poetry](https://python-poetry.org/)
  
### Installation

After installing all prerequisites, run `poetry install`.

### Running the Scripts

#### Soundings Script

First, create a `_soundings` folder inside `data`. This is where the files will be dumped in. Then run:

`poetry run load_soundings a b`

Where `a` and `b` are the start and end indices of the cases. (So to start off testing any updates to the scripts, set `a = 0` and `b = 2` such that the command is `poetry run load_soundings 0 2` to run the first two cases and work up from there).

NEW: The files in the `_soundings` folder should be uploaded to an S3 bucket to expose them thru the API, and not committed directly to the repo. Please contact Jim to help with this.

#### A note on Metpy

Due to `Metpy` having dependencies on `pyproj` and `netcdf4`, which do not play well with Poetry, if you get errors like these (I'm using a Mac, so YMMV):

```
ImportError: dlopen(/Users/jimtang/Library/Caches/pypoetry/virtualenvs/weather-cases-oWfRt2rv-py3.12/lib/python3.12/site-packages/pyproj/_context.cpython-312-darwin.so, 0x0002): symbol not found in flat namespace '_proj_context_create'
```

```
ImportError: dlopen(/Users/jimtang/Library/Caches/pypoetry/virtualenvs/weather-cases-oWfRt2rv-py3.12/lib/python3.12/site-packages/netCDF4/_netCDF4.cpython-312-darwin.so, 0x0002): symbol not found in flat namespace '_H5get_libversion'
```

You may have to run the following after `poetry install`:
```
poetry run pip install --force-reinstall pyproj --no-binary pyproj
poetry run pip install --force-reinstall netcdf4 --no-binary netcdf4
```

For `pyproj` to work you might also have to run `brew install proj` on Mac.


### Starting Locally

```
poetry run uvicorn weather_cases.main:app --reload --host localhost --port 8000
```

API docs available at localhost:8000/docs