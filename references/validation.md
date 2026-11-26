# Validation evidence

Environment examined on 2026-11-25. Windows, AnyLogic PLE 8.9.10 build 202609231424, Python 3.13.9 and lxml 5.3.0.

| Scenario | File creation and structural inspection | Native PLE build/run of the public workflow's output |
| --- | --- | --- |
| Pedestrian-only walk | Passed. One Source, one GoTo, one Sink, no Elevator. | Pending |
| Two-floor single elevator | Passed. One native car and one corresponding PedElevator. | Pending |
| Two-floor three elevators | Passed. Three independent complete flow lanes. | Pending |
| Three elevators after parameter edit | Passed. Capacity 2 per car and 24 arrivals/minute per lane. | Pending |

A separate locally developed project provided evidence for generated Java initialization order and the installed enum names. Direct use of its Java engine outside the PLE launcher was attempted and rejected. Evidence for a lab run requires its native run output at the stop horizon with nonzero completions and consistent counts. Record visual checks independently.

The exact Java CSV actions embedded in each of the four labs passed a local JDK test with fixture objects. The generated CSVs passed the parser and count checks. A corrupted native transport count, an invalid arrival rate, an overwrite request and a non-lab configure request were rejected. Fixture input counts are not simulation results.

An independent offline forward test generated the three-car model and a capacity/rate/seed variant in a separate temporary directory. It checked the connectors, served floors, parameter changes, and valid and over-capacity CSV cases. Its findings led to reporting rate, seed and horizon in the inspector, directing generated models to a separate workspace in the instructions, and rejecting capacities and seeds outside the lab's Java integer range.
