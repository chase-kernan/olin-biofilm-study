from pathlib import Path

import pandas as pd
import numpy as np

from model.experiments import Experiment, from_plan

def test_from_plan(tmpdir):
    path = tmpdir / 'plan.json'
    with path.open('w') as json_file:
        json_file.write("""{
            "name": "test_experiment",
            "runs_per_spec": 3,
            "specs": {
                "a": 1,
                "b": [3, 4],
                "c": { "from": 1, "to": 10, "num": 5 }
            }
        }""")

    exp = from_plan(path)
    assert exp.name == 'test_experiment'
    assert exp.runs_per_spec == 3
    assert exp.specs['a'] == 1
    assert exp.specs['b'] == [3, 4]
    assert all(exp.specs['c'] == np.arange(1, 10, 5))

def test_new_experiment():
    specs = { 'a': 10 }
    exp = Experiment('my_experiment', runs_per_spec=9, specs=specs)
    assert exp.name == 'my_experiment'
    assert exp.runs_per_spec == 9
    assert exp.specs == specs

def test_data_file():
    exp = Experiment('some-exp')
    root = Path('root')
    assert exp.data_file(root) == root/'some-exp.hdf5'

def test_expanded_specs():
    expanded = Experiment(specs=dict(
        a=1,
        b=[3, 4, 5],
        c=[6, 7],
    )).expanded_specs

    keys = 'a', 'b', 'c'
    as_tuples = { tuple(value[key] for key in keys) 
                  for _, value in expanded.iterrows() }
    assert as_tuples == {
        (1, 3, 6),
        (1, 3, 7),
        (1, 4, 6),
        (1, 4, 7),
        (1, 5, 6),
        (1, 5, 7),
    }

