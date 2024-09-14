import numpy
import pandas


class GeocoderError(Exception):
    pass


class OutOfBoundError(Exception):
    pass


def load_gazetteer(filepath: str) -> pandas.DataFrame:
    g = pandas.read_json(filepath, orient="records", lines=True).dropna(
        axis=1, how="all"
    )
    g = g.rename(columns={"name_0": "country_name", "region_name_1": "region_name"})
    # title location names for 1:1 matching
    names = [f for f in g if "name" in f]
    g.loc[:, names] = g.loc[:, names].apply(lambda s: s.str.title())
    # verify coordinates
    if "latitude" not in g and "longitude" not in g:
        raise GeocoderError("Missing latitude/longitude fields")
    # format coordinates
    g["coordinates"] = [
        dict(lat=lat, lon=lon) for lat, lon in zip(g.latitude, g.longitude)
    ]
    return g


def distance(s_lat, s_lng, e_lat, e_lng):
    # approximate radius of earth in km
    R = 6373.8
    s_lat = s_lat * numpy.pi / 180.0
    s_lng = numpy.deg2rad(s_lng)
    e_lat = numpy.deg2rad(e_lat)
    e_lng = numpy.deg2rad(e_lng)
    d = (
        numpy.sin((e_lat - s_lat) / 2) ** 2
        + numpy.cos(s_lat) * numpy.cos(e_lat) * numpy.sin((e_lng - s_lng) / 2) ** 2
    )
    return 2 * R * numpy.arcsin(numpy.sqrt(d))


def filter_places_by_buffer(
    gazetteer: pandas.DataFrame,
    latitude: float,
    longitude: float,
    radius: int = 100,
) -> pandas.DataFrame:
    # get places within a given buffer
    g = gazetteer.loc[
        distance(gazetteer.latitude, gazetteer.longitude, latitude, longitude)
        <= radius,
        :,
    ]
    if g.empty:
        raise OutOfBoundError("No places found within the given buffer")
    return g.copy()


def filter_places_by_bounding_box(
    gazetteer: pandas.DataFrame,
    bbox: str,
) -> pandas.DataFrame:
    minx, miny, maxx, maxy = map(float, bbox.split(","))
    g = gazetteer.loc[
        gazetteer.latitude.between(miny, maxy)
        & gazetteer.longitude.between(minx, maxx),
        :,
    ]
    if g.empty:
        raise OutOfBoundError("No places found within the given bounding box")
    return g.copy()
