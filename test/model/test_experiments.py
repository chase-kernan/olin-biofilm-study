from model.experiments import Experiment, cartesian_product
from pathlib import Path
import pandas as pd

def test_new_experiment():
    exp = Experiment('my experiment', [])
    assert exp.name == 'my experiment'

def test_data_dir():
    exp = Experiment('some-exp', [])
    root = Path('root')
    assert exp.data_dir(root) == root/'some-exp'

def test_empty_specs_frame():
    exp = Experiment('some-exp', [])
    assert exp.specs_frame.empty

def test_cartesian_product():
    actual = cartesian_product(
        a=1,
        b=[3, 4, 5],
        c=[6, 7],
    )

    keys = 'a', 'b', 'c'
    as_tuples = {tuple(value[key] for key in keys) for value in actual}
    assert as_tuples == {
        (1, 3, 6),
        (1, 3, 7),
        (1, 4, 6),
        (1, 4, 7),
        (1, 5, 6),
        (1, 5, 7),
    }

