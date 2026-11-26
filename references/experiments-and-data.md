# Experiments, statistics and integration

Use a named Simulation experiment for smoke tests. Set model time units, a finite stop time, and a fixed seed. Keep the seed, model build and rate/capacity settings with results. Separate smoke-test assertions from production KPI thresholds. For comparison of alternatives, run more than one seed. For replications, avoid pooling run averages without their sample sizes.

## Count the process at its boundaries

| Metric | Define and collect it |
| --- | --- |
| Queue length per floor | Increment once when a pedestrian starts waiting and decrement on boarding or cancellation. For a live snapshot with no custom lifecycle, check the definition of `Elevator.getWaitingPeds(level)`. Keep queues per car if comparing car assignments. |
| Waiting time | `onStartWaiting` stores time and `onEnterElevator` records the sample. The first callback may be skipped if the pedestrian never stops. Treat such boardings as zero if the denominator is all boardings, or keep a distinct sample count. Add walking-to-lobby time only if the metric calls for it. |
| Riding time | `onEnterElevator` to `onExitElevator` measures time inside the car. Includes any intervening stops. Use a separate measure for time while the car moves. |
| Transported | Increment at `onExitElevator` and cross-check against `nTransportedPeds()`. The sink counts passengers who reached the end of the post-ride walk. At a finite horizon these counts can differ. |
| Capacity | Check occupancy on each transition. The labs track current and peak board/alight load per car and compare with the native capacity. |

The callbacks above and their local variables are documented. Check callback timing for the binding you use. Track deleted or timed-out requests explicitly if enabling those paths. For a stochastic lab, confirm the population, event durations, floor and car counts are plausible. [Elevator statistics](https://www.anylogic.help/markup/elevator.html), [PedElevator actions](https://www.anylogic.help/library-reference-guides/pedestrian-library/pedelevator.html).

## Export a small stable contract

For a local file, export in **After simulation run** with routine Java NIO or an appropriate native file or database element. The callback runs at a natural finish, and termination through the UI is different. The supplied models use UTF-8, decimal points independent of Windows locale, explicit unit fields, and distinct output paths per model. Use relative AnyLogic file resources for portable model inputs. Keep model configuration and run outputs in separate files. [Simulation experiment](https://www.anylogic.help/anylogic/experiments/simulation-experiment.html), [file resources](https://anylogic.help/anylogic/connectivity/resources.html), [model database](https://anylogic.help/anylogic/connectivity/database.html).

For external integrations, start by exposing a small parameter contract and a versioned CSV or JSON summary. Keep service calls out of per-pedestrian callbacks unless the simulation design needs them. Add Pypeline, Cloud API or a custom external integration when explicitly requested and compatible with the installation and license. Pypeline is a separate optional library and local connector and was not tested here. The supplied labs need no Python at model runtime. [Pypeline](https://www.anylogic.help/advanced/code/pypeline.html), [AnyLogic Cloud help](https://anylogic.help/cloud/index.html).
