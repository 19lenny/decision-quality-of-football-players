import math
import numpy as np
from scipy.stats import kstest, shapiro
from scipy.stats import lognorm

from SetUp import JSONtoDF, CONSTANTS

s = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)