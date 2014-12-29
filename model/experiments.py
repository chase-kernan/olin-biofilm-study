
from pathlib import Path
from itertools import product
from collections import Iterable

import pandas as pd

class Experiment:

    def __init__(self, name, specs):
        self.name = name
        self.specs_frame = pd.DataFrame(specs)

    def data_dir(self, parent_dir):
        return parent_dir / self.name

def cartesian_product(**params):
    params = {name: value if isinstance(value, Iterable) else [value] 
              for name, value in params.items()}
    return map(dict, product(*([(name, value) for value in values]
                               for name, values in params.items())))


