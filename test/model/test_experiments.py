from pathlib import Path

import pandas as pd
import numpy as np

from model.experiments import Plan, load_plan, \
                              CreateSpecs, RunModels, AnalyzeModels

def load_plan_str(tmpdir, plan_str):
    path = tmpdir/'plan.py'
    with path.open('w') as plan_file:
        plan_file.write(plan_str)
    return load_plan(path)


def test_load_plan_name(tmpdir):
    plan = load_plan_str(tmpdir, 'Plan(name="testing")')
    assert plan.name == 'testing'

def test_load_plan_globals(tmpdir):
    assert load_plan_str(tmpdir, 'np; pd; Plan()')

def test_load_plan_with_create_specs(tmpdir):
    plan = load_plan_str(tmpdir, """
        Plan(steps=[CreateSpecs(a=1, b=np.arange(0, 1), c=[3, 4])])
    """.strip())
    create = plan.steps[0]
    assert create.params['a'] == 1
    assert all(create.params['b'] == np.arange(0, 1))
    assert create.params['c'] == [3, 4]

def test_load_plan_with_run_models(tmpdir):
    plan = load_plan_str(tmpdir, """
        Plan(steps=[RunModels(runs_per_spec=9)])
    """.strip())
    run = plan.steps[0]
    assert run.runs_per_spec == 9

def test_load_plan_with_analyze_models(tmpdir):
    plan = load_plan_str(tmpdir, """
        Plan(steps=[AnalyzeModels(fields=['a', 'b', 'c'])])
    """.strip())
    analyze = plan.steps[0]
    assert analyze.fields == ['a', 'b', 'c']

def test_new_plan():
    steps = [CreateSpecs(), RunModels()]
    plan = Plan(name='my_experiment', steps=steps)
    assert plan.name == 'my_experiment'
    assert plan.steps == steps

def test_experiment_file():
    exp = Plan('some-exp')
    root = Path('root')
    assert exp.experiment_file(root) == root/'some-exp.hdf5'

def test_create_specs_expanded_specs():
    expanded = CreateSpecs(
        a=1,
        b=[3, 4, 5],
        c=[6, 7],
    ).expanded_specs

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

