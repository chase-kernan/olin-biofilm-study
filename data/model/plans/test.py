Plan(name="testing",
     steps=[
         CreateSpecs(
             light_penetration=0,
             media_ratio=np.linspace(0, 1, 100),
             boundary_layer=[3, 4, 5]
         ),
         RunModels(runs_per_spec=5),
         AnalyzeModels(fields=[
             'convex_hull_density',
             'perimeter',
             'H'
         ])
    ])
