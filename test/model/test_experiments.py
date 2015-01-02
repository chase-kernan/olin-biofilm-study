from pathlib import Path

import pandas as pd
import numpy as np

from model.experiments import Plan, load_plan

def test_load_plan(tmpdir):
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

    plan = load_plan(path)
    assert plan.name == 'test_experiment'
    assert plan.runs_per_spec == 3
    assert plan.specs['a'] == 1
    assert plan.specs['b'] == [3, 4]
    assert all(plan.specs['c'] == np.arange(1, 10, 5))

def test_new_plan():
    specs = { 'a': 10 }
    plan = Plan('my_experiment', runs_per_spec=9, specs=specs)
    assert plan.name == 'my_experiment'
    assert plan.runs_per_spec == 9
    assert plan.specs == specs

def test_experiment_file():
    exp = Plan('some-exp')
    root = Path('root')
    assert exp.experiment_file(root) == root/'some-exp.hdf5'

def test_expanded_specs():
    expanded = Plan(specs=dict(
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

