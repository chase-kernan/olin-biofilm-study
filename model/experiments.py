from pathlib import Path
from itertools import product
from collections import Iterable, Mapping

import json
import pandas as pd
import numpy as np

STEPS = set()

def register_step(step):
    STEPS.add(step)


def load_plan(path):
    plan = []
    exposed = {
        'Plan': lambda *args, **kwargs: plan.append(Plan(*args, **kwargs)),
        'np': np,
        'pd': pd }
    exposed.update({ cls.__name__: cls for cls in STEPS })

    with path.open('r') as plan_file:
        exec(plan_file.read(), exposed)

    return plan[0]


class Plan:
    def __init__(self, name="experiment", steps=None):
        self.name = name
        self.steps = steps or []


    def experiment_file(self, parent_dir):
        return parent_dir / "{}.hdf5".format(self.name)

    def run(self, parent_dir):
        store = pd.HDFStore(self.experiment_file(parent_dir))
        for step in self.steps:
            if not step.complete(store):
                step.run(store)
        return store


class CreateSpecs:
    def __init__(self, **params):
        self.params = params

    @property
    def expanded_specs(self):
        params = { name: value if isinstance(value, Iterable) else [value] 
                   for name, value in self.params.items() }

        return pd.DataFrame(list(map(dict, 
            product(*([(name, value) for value in values]
                       for name, values in params.items())))))

    def complete(self, store):
        return 'specs' in store

    def run(self, store):
        store['specs'] = self.expanded_specs
register_step(CreateSpecs)


class RunModels:
    def __init__(self, runs_per_spec=5):
        self.runs_per_spec = runs_per_spec

    def complete(self, store):
        return False
    
    def run(self, store):
        pass
register_step(RunModels)


class AnalyzeModels:
    def __init__(self, fields=None):
        self.fields = fields or []

    def complete(self, store):
        return False
    
    def run(self, store):
        pass
register_step(AnalyzeModels)
