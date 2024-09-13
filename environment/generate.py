from itertools import product
from typing import Iterable
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from geojson import GeoJSON

from environment.configs import CONFIGS
from environment.era5_rda import open_era5_dataset, CODES
from environment.geojsons import contour_linestrings, contour_polygons, wind_vector_grid


def heights(
    extent: tuple[float], times: Iterable[pd.Timestamp], pressure_levels: Iterable[int]
) -> Iterable[tuple[pd.Timestamp, int, GeoJSON]]:
    unique_dates = set(time.date() for time in times)
    levels = list(set(pressure_levels))
    date_datasets = (
        open_era5_dataset(d, CODES["height"], subset=extent, levels=levels)
        for d in unique_dates
    )
    for ds in date_datasets:
        valid_times = (t for t in times if t in ds.time)
        valid_levels = (
            l
            for l in levels
            if CONFIGS.get(l, None) and CONFIGS[l].height_contours is not None
        )
        for time, pressure_level in product(valid_times, valid_levels):
            # calculate height from geopotential
            da = ds.sel(level=pressure_level, time=time).Z / 9.8065
            da = _process_da(da)

            x, y = np.meshgrid(da.longitude, da.latitude)
            CS = plt.contour(x, y, da, levels=CONFIGS[pressure_level].height_contours)
            yield time, pressure_level, contour_linestrings(CS)


def winds(
    extent: tuple[float], times: Iterable[pd.Timestamp], pressure_levels: Iterable[int]
) -> Iterable[tuple[pd.Timestamp, int, GeoJSON, GeoJSON]]:
    unique_dates = set(time.date() for time in times)
    levels = list(set(pressure_levels))
    u_datasets = (open_era5_dataset(d, CODES["u"], subset=extent) for d in unique_dates)
    v_datasets = (open_era5_dataset(d, CODES["v"], subset=extent) for d in unique_dates)

    for u_ds, v_ds in zip(u_datasets, v_datasets):
        valid_times = (t for t in times if t in u_ds.time and t in v_ds.time)
        valid_levels = (
            l
            for l in levels
            if CONFIGS.get(l, None) and CONFIGS[l].isotachs is not None
        )
        for time, pressure_level in product(valid_times, valid_levels):
            # convert to kt
            u = u_ds.sel(level=pressure_level, time=time).U * 1.94384
            v = v_ds.sel(level=pressure_level, time=time).V * 1.94384
            u = _process_da(u)
            v = _process_da(v)

            x, y = np.meshgrid(u.longitude, u.latitude)
            wspd = np.sqrt(u**2 + v**2)
            CS = plt.contourf(x, y, wspd, levels=CONFIGS[pressure_level].isotachs)
            yield time, pressure_level, contour_polygons(CS), wind_vector_grid(u, v)


def _process_da(da: xr.DataArray) -> xr.DataArray:
    da_processed = da.reindex(latitude=list(reversed(da.latitude)))
    da_processed.coords["longitude"] = (
        da_processed.coords["longitude"] + 180
    ) % 360 - 180
    return da_processed.sortby(da_processed.longitude)
