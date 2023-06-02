from typing import NamedTuple  # 为了注解带有多个字段的元组，推荐使用NamedTuple

from geolib import geohash as gh  # type: ignore

PRECISION = 9


# 与tuple[float,float]互相相容
class Coordinate(NamedTuple):
    lat: float
    lon: float


def geohash(lat_lon: Coordinate) -> str:
    return gh.encode(*lat_lon, PRECISION)


"""
$ mypy coordinates_named.py 
Success: no issues found in 1 source file
"""
