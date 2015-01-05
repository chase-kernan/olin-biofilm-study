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


def run_model(spec):
    return []

class RunModels:
    def __init__(self, runs_per_spec=5):
        self.runs_per_spec = runs_per_spec

    def table(self, store):
        return None

    def remaining(self, store):
        table = self.table(store)
        for index, spec in store['specs'].iterrows():
            num_runs = (table['spec_index'] == index).sum()
            yield index, spec, self.runs_per_spec - num_runs

    def complete(self, store):
        return 'models' in store \
            and all(num_rem == 0 for i, spec, num_rem in self.remaining(store))
    
    def run(self, store):
        table = self.table(store)
        for i, spec, num_rem in self.remaining():
            for _ in range(num_rem):
                result = run_model(spec)
                table.append({ 'spec_index': i, 'result': result })
register_step(RunModels)


class AnalyzeModels:
    def __init__(self, fields=None):
        self.fields = fields or []

    def complete(self, store):
        return False
    
    def run(self, store):
        pass
register_step(AnalyzeModels)
