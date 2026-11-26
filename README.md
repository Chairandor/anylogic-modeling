# AnyLogic Modeling Skill

An agent skill for developing native AnyLogic models on Windows. It focuses on pedestrian flows, multilevel buildings, stairs, elevators, and experiments under the Personal Learning Edition.

## Use the skill

Copy this directory as `anylogic-modeling` into your agent's local skills directory, or open [SKILL.md](SKILL.md) for the workflow. The [reference index](SKILL.md#workflow) links to notes on ALP and ALPX, native libraries, experiment data, and troubleshooting.

## Generate a local lab

Install AnyLogic and Python 3 with `lxml`. Use the official **Pedestrian Elevator** example included in your own AnyLogic installation. The PowerShell inventory helper lists matching examples, installed libraries, and optional Java signatures.

```powershell
python -m pip install -r requirements.txt
.\scripts\inspect-install.ps1

# Replace this path with the example listed by the inventory helper.
$example = 'C:\path\to\Pedestrian Elevator.alp'
python .\scripts\lab_models.py create .\lab-output\SingleLift.alp --example "$example" --cars 1
python .\scripts\lab_models.py inspect .\lab-output\SingleLift.alp
```

Open the generated model in AnyLogic, build it, and run its Simulation experiment to the set stop time. The lab can export a CSV, and the script can check it independently. See [lab workflow](references/lab-workflow.md) for pedestrian-only, three-car, and parameter-edit examples.

The model generator and local API inventory were checked on Windows with PLE 8.9.10 and its bundled examples. See [validation evidence](references/validation.md) for the scope of those checks and the remaining native run verification.

## License

The original Skill documentation and helper scripts are available under the [MIT License](LICENSE). AnyLogic is separate software. The generator uses a copy of the locally installed official example and saves a new file in your workspace. Vendor examples, runtime files, and generated models are outside the scope of this repository's license. See [AnyLogic's agreements](https://www.anylogic.com/downloads/legal-info/).
