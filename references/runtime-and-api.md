# Local API, licensing and execution

## Discover the actual build

On Windows PLE 8.9.10 the examples bundle can be under the installation's `plugins` directory or under `ProgramData\AnyLogic 8.9 Personal Learning Edition\eclipse\plugins\com.anylogic.examples_*\`. The inventory helper is read-only. Pass `-Install` for nondefault install paths and `-ExamplesRoot` if the examples are elsewhere.

```powershell
& .\scripts\inspect-install.ps1 -ClassName @(
  'com.anylogic.engine.markup.ElevatorState',
  'com.anylogic.engine.markup.Elevator',
  'com.anylogic.libraries.pedestrian.PedElevator'
)
```

Use installed engine `javadoc` and Pedestrian Library `lib\doc`, then `javap -public` against the shipped JAR if naming conflicts. On 8.9.10 build `202609231424`, `ElevatorState` has `IDLE`, `MOVING`, `LOADING` and `FAILED`. `ElevatorDirection` still has names such as `ELEVATOR_DIRECTION_UP`, and per-level movement uses `ElevatorMovementMode.ELEVATOR_MOVEMENT_BY_TIME_PER_LEVEL`. Transcribing historical `ELEVATOR_STATE_*` identifiers from the web caused six actual compiler errors in a local model.

## Use a supported run context

**Official.** The desktop launcher supports opening a quoted ALP path and documents a `-r` experiment launch. Use the installation directory as the working directory for the documented run syntax. This launches the desktop workflow. The documents do not establish an unattended PLE compilation or licensed standalone runtime.

```powershell
& 'C:\path\to\AnyLogic.exe' 'C:\path\to\Model.alp'
# From the installation directory for the documented run syntax
.\AnyLogic.exe -r 'C:\path\to\Model.alp' 'Simulation'
```

For a user-controlled PLE session, open the exact updated ALP or ALPX project, run **F7** for build and **F5** for the intended Simulation experiment, and let it reach the set stop time. If another project is selected, right-click the desired Simulation experiment and choose Run. Review Problems for compile errors and the model run console for runtime errors. [Desktop command line and standalone export](https://www.anylogic.help/anylogic/running/export-java-application.html), [Simulation experiment](https://www.anylogic.help/anylogic/experiments/simulation-experiment.html).

**Observed on local 8.9.10.** The editor generated Java and model metadata into its workspace. The project-specific build folders contained `src.generated`, `.classpath` and classes. Those files are evidence for troubleshooting. Their names and locations vary by edition or installation. PLE-generated model code from the earlier corrected project was compiled with the installed JDK for diagnosis. The direct Java runtime launch later reported `Invalid start location for AnyLogic Runtime` and produced no valid run. Do not retry by imitating launcher state or bypassing license checks.

## Stay within the edition

**Official at 8.9.10.** PLE is for learning/classroom use. Current limits include 10 agent types per model, 50,000 dynamically created agents, up to 200 agent populations and flowchart blocks per agent type, and a five-hour simulation horizon for the industry libraries other than Process Modeling. Standalone Java export is a Professional feature. The Python Design-time API is documented for Professional and University Researcher from 8.9.7. A package present in a PLE install does not establish connector entitlement. Use native model editing and local data interchange for the baseline. [Editions and current limits](https://anylogic.help/anylogic/ui/editions.html), [design-time API requirements](https://www.anylogic.help/advanced/code/dt-api.html).

**Pending.** The documented launcher switches and ALPX UI conversion were identified, but no automated PLE launcher invocation was validated for this skill. Optional Cloud or Professional flows need their own edition, access and deployment validation.
