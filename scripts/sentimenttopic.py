import pickle
import logging

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from ptm import AuthorTopicModel
from ptm.utils import convert_cnt_to_list, get_top_words

logger = logging.getLogger('AuthorTopicModel')
logger.propagate=False