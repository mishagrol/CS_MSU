import math
import os, sys
import numpy as np
import pandas as pd
import datetime as dt


from pcse.base import WeatherDataContainer, WeatherDataProvider
from pcse.util import reference_ET, angstrom, check_angstromAB
from pcse.exceptions import PCSEError
from pcse.settings import settings


sys.path.append("../soil")
from ANN_Module import PTF_MODEL  # type: ignore
from DB_Module import DB  # type: ignore

soil_kshen = [
    {
        "Thickness": [0.3, "m"],
        "SoilOrganicCarbon": [5.1, "%"],
        "KA5TextureClass": "Lu",
        "Sand": [0.037, "kg kg-1 (%[0-1])"],
        "Clay": [0.09, "kg kg-1 (%[0-1])"],
        "Skeleton": [0.02, "%[0-1]"],
        "PoreVolume": [0.566, "m3 m-3"],
        "FieldCapacity": [0.3, "m3 m-3"],
        "PermanentWiltingPoint": [0.15, "m3 m-3"],
        "pH": [6.213],
        "CN": [12.481],
        "SoilBulkDensity": [1126.625, "kg m-3"],
    },
    {
        "Thickness": [0.1, "m"],
        "SoilOrganicCarbon": [3.3, "%"],
        "KA5TextureClass": "Lu",
        "Sand": [0.045, "kg kg-1 (%[0-1])"],
        "Clay": [0.088, "kg kg-1 (%[0-1])"],
        "Skeleton": [0.02, "%[0-1]"],
        "PoreVolume": [0.594, "m3 m-3"],
        "FieldCapacity": [0.3, "m3 m-3"],
        "PermanentWiltingPoint": [0.15, "m3 m-3"],
        "pH": [6.397],
        "CN": [10.531],
        "SoilBulkDensity": [1056.667, "kg m-3"],
    },
]


class ParseError(PCSEError):
    pass


class OutOfRange(PCSEError):
    pass


class IRRADFromSunshineDuration:
    def __init__(self, latitude, angstA, angstB):

        assert -90 < latitude < 90, "Invalid latitude value (%s) encountered" % latitude
        check_angstromAB(angstA, angstB)
        self.latitude = latitude
        self.angstA = angstA
        self.angstB = angstB

    def __call__(self, value, day):
        """Computes irradiance in J/m2/day from sunshine duration by applying the Angstrom equation

        :param value: sunshine duration in hours
        :param day: the day
        :return: irradiance in J/m2/day
        """
        assert (
            0 <= value <= 24
        ), "Invalid sunshine duration value (%s) encountered at day %s" % (value, day)
        irrad = angstrom(day, self.latitude, value, self.angstA, self.angstB)

        return irrad


def csvdate_to_date(x, dateformat):
    """Converts string x to a datetime.date using given format.

    :param x: the string representing a date
    :param dateformat: a strptime() accepted date format
    :return: a date
    """
    return dt.datetime.strptime(x, dateformat).date()


# Conversion functions
def NoConversion(x, d):
    return float(x)


def kJ_to_J(x, d):
    return float(x) * 1000.0


def mm_to_cm(x, d):
    return float(x) / 10.0


def kPa_to_hPa(x, d):
    return float(x) * 10.0


class ForecastConverter(WeatherDataProvider):
    """Reading weather data from pandas.DataFrame into PCSE Weather Container.
    :df pandas.DataFrame with weather records
    :param dateformat: date format to be read. Default is '%Y%m%d'
    :keyword ETmodel: "PM"|"P" for selecting Penman-Monteith or Penman
        method for reference evapotranspiration. Default is 'PM'.
    :metainfo dict with general info
        ## Site Characteristics
        Country     = 'Netherlands'
        Station     = 'Wageningen, Haarweg'
        Description = 'Observed data from Station Haarweg in Wageningen'
        Source      = 'Meteorology and Air Quality Group, Wageningen University'
        Contact     = 'Peter Uithol'
        Longitude = 5.67; Latitude = 51.97; Elevation = 7; AngstromA = 0.18; AngstromB = 0.55; HasSunshine = False
        ## Daily weather observations (missing values are NaN)
        DAY,IRRAD,TMIN,TMAX,VAP,WIND,RAIN,SNOWDEPTH
    """

    obs_conversions = {
        "TMAX": NoConversion,
        "TMIN": NoConversion,
        "IRRAD": kJ_to_J,
        "VAP": kPa_to_hPa,
        "WIND": NoConversion,
        "RAIN": mm_to_cm,
        "SNOWDEPTH": NoConversion,
    }

    def __init__(
        self,
        metainfo: dict,
        df: pd.DataFrame,
        dateformat: str = "%Y-%m-%d",
        ETmodel: str = "PM",
        force_reload: bool = False,
    ):

        WeatherDataProvider.__init__(self)
        self.dateformat = dateformat
        self.ETmodel = ETmodel

        self._read_meta(metainfo)

        self._read_observations(df)

    def _read_meta(self, metainfo):
        header = metainfo

        self.nodata_value = -99
        self.description = [
            "Weather data for:",
            "Country: %s" % header["Country"],
            "Station: %s" % header["Station"],
            "Description: %s" % header["Description"],
            "Source: %s" % header["Source"],
            "Contact: %s" % header["Contact"],
        ]

        self.longitude = float(header["Longitude"])
        self.latitude = float(header["Latitude"])
        self.elevation = float(header["Elevation"])
        angstA = float(header["AngstromA"])
        angstB = float(header["AngstromB"])
        self.angstA, self.angstB = check_angstromAB(angstA, angstB)
        self.has_sunshine = bool(header["HasSunshine"])
        # If the file has sunshine duration, we replace the convertor with the angstrom module
        if self.has_sunshine:
            self.obs_conversions["IRRAD"] = IRRADFromSunshineDuration(  # type: ignore
                self.latitude, self.angstA, self.angstB
            )

    def _read_observations(self, df: pd.DataFrame):
        """Processes the pandas DataFrame with meteo data
        and converts into the correct units.
        """
        for i, d in df.iterrows():
            try:
                day = None
                day = csvdate_to_date(d.pop("DAY"), self.dateformat)
                row = {"DAY": day}
                for label in self.obs_conversions.keys():
                    func = self.obs_conversions[label]
                    value = float(d[label])
                    r = func(value, day)
                    if math.isnan(r):
                        if label == "SNOWDEPTH":
                            continue
                        raise ParseError
                    row[label] = r  # type: ignore
                # Reference ET in mm/day
                e0, es0, et0 = reference_ET(
                    LAT=self.latitude,
                    ELEV=self.elevation,
                    ANGSTA=self.angstA,
                    ANGSTB=self.angstB,
                    ETMODEL=self.ETmodel,
                    **row
                )
                # convert to cm/day
                row["E0"] = e0 / 10.0  # type: ignore
                row["ES0"] = es0 / 10.0  # type: ignore
                row["ET0"] = et0 / 10.0  # type: ignore

                wdc = WeatherDataContainer(
                    LAT=self.latitude, LON=self.longitude, ELEV=self.elevation, **row
                )
                self._store_WeatherDataContainer(wdc, day)
            except (ParseError, KeyError):
                msg = (
                    "Failed reading element '%s' for day '%s' at line %i. Skipping ..."
                    % (label, day, i)  # type: ignore
                )
                self.logger.warn(msg)
            except ValueError as e:  # strange value in cell
                msg = "Failed computing a value for day '%s' at row %i" % (day, i)  # type: ignore
                self.logger.warn(msg)


def rosseta(data_in, n_model=3):
    with DB(
        host="localhost",
        user="root",
        db_name="Rosetta",
        sqlite_path="../soil/sqlite/Rosetta.sqlite",
    ) as db:
        ptf_model = PTF_MODEL(n_model, db)
        data = data_in
        raw = False
        if not raw:
            res_dict = ptf_model.predict(data, sum_data=True)
            vgm_name = res_dict["var_names"]
            vgm_mean = res_dict["sum_res_mean"]
            vgm_new = np.stack(
                (
                    vgm_mean[0],
                    vgm_mean[1],
                    10 ** vgm_mean[2],
                    10 ** vgm_mean[3],
                    10 ** vgm_mean[4],
                )
            )
            vgm_new = vgm_new.transpose()
            return vgm_new
        else:
            res_dict = ptf_model.predict(data, sum_data=False)
            return res_dict


def vangen_direct(theta_r, theta_s, alpha, n, psy: int):
    return theta_r + (theta_s - theta_r) / ((1 + (alpha * psy) ** n)) ** (1 - 1 / n)
