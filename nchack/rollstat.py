
from .runthis import run_this

def rollstat(self, window,  stat = "mean"):
    """Method to calculate the monthly statistic from a netcdf file"""
    if type(window) is float:
        window = int(window)

    if type(window) is not int:
        raise ValueError("The window supplied is not numeric!")

    cdo_command = "cdo -run" + stat + "," + str(window)

    run_this(cdo_command, self, output = "ensemble")



def rolling_mean(self, window):

    """
    Calculate a rolling mean based on a window.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling mean

    """

    return rollstat(self, window = window, stat = "mean")

def rolling_min(self, window):
    """
    Calculate a rolling minimum based on a window.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling minimum

    """

    return rollstat(self, window = window, stat = "min")

def rolling_max(self, window):
    """
    Calculate a rolling maximum based on a window.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling maximum

    """
    return rollstat(self, window = window, stat = "max")

def rolling_range(self, window):
    """
    Calculate a rolling range based on a window.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling range

    """
    return rollstat(self, window = window, stat = "range")

def rolling_sum(self, window):
    """
    Calculate a rolling sum based on a window.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    """
    return rollstat(self, window = window, stat = "sum")
