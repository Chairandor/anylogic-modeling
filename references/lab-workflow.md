# Native pedestrian smoke-test labs

The generator reads the official **Pedestrian Elevator** example from a local AnyLogic installation and builds a lab with two navigable floors, editable native markup, and three independently connected elevator lanes. The generator uses Python 3 and lxml offline. It writes a separate model file. Use `--seed-file` in place of `--example` if you already have a compatible lab seed.

```powershell
# Point to the skill and run from a writable project workspace.
$tool = 'C:\path\to\anylogic-modeling\scripts\lab_models.py'
$example = 'C:\path\to\Pedestrian Elevator.alp'
$lab = Join-Path (Get-Location) 'lab-output'
python $tool create "$lab\PedestrianWalk.alp" --example "$example" --cars 0
python $tool create "$lab\SingleLift.alp" --example "$example" --cars 1
python $tool create "$lab\ThreeLifts.alp" --example "$example" --cars 3
python $tool configure "$lab\ThreeLifts.alp" "$lab\ThreeLiftsTuned.alp" --capacity 2 --rate 24
python $tool inspect "$lab\ThreeLiftsTuned.alp"
```

- Defaults are seed 42, 360 simulation seconds, 10 arrivals per minute per lane and capacity 4 per active car. Each elevator serves both floors. All boarding and alighting are native.
- The walk case uses one navigable floor and a display layer. Elevator cases use two navigable floors plus a display layer; the latter is excluded explicitly from Elevator service.
- Open each generated ALP in PLE, build with **F7**, and run its Simulation with **F5** through the final time. The optional **1F** and **2F** buttons change which floor is shown. The lab runs in virtual time. Change the experiment's execution mode temporarily for close visual inspection.
- The generator puts a per-model absolute CSV path in **After simulation run**. Generate at the final location, or update this action after moving a generated lab. Reruns replace the CSV with that model's latest result. Archive previous results separately if needed.
- The automatic output includes the observed peak load per active car and verifies capacity during boarding. It includes total wait and ride means by their respective sample counts, plus cross-checks against the native transported count. To verify a finished export independently, use the command below with the appropriate car count.

```powershell
python $tool verify-csv "$lab\ThreeLiftsTuned.csv" --cars 3
```

The `inspect` command is a structural preflight for single-file ALP. It checks sampled identity/reference invariants and reports block counts, capacities, and the lab rate, experiment seed and time properties. It cannot certify arbitrary ALP schemas, compiled Java, animation or model results.

See [validation evidence](validation.md) for recorded runs and pending checks.
