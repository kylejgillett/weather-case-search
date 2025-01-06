# Chase Case Search

API to expose fuzzy search capability for storm chase cases.

### Prerequisites

* Python >= 3.12
* Docker (optional for development)
* [Poetry](https://python-poetry.org/)
  
### Installation

After installing all prerequisites, run `poetry install`.

#### A note on the Metpy and the sounding scripts

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