
# py42

This is a simple Python module for running simulations using `42`. This is intended to be used in a devcontainer. `42` will be cloned at `/42` within the container. 

This is a work-in-progress and is very much subject to change. For now, the only functional component is the Monte Carlo simulation script. Future additions will be based on need.





# Monte Carlo Simulations

## Usage

`monte_carlo.py` handles all of the input and output from `42`, while `42` does all of the heavy lifting.  

```bash
./monte_carlo.py --help
```

`--num_cores` threads will be spawned to run simulations. `runner(...)` is the entry point for each thread and spawns subprocesses to run `42`. 

`def preprocess(...)` is used to configure the inputs for the given run of the simulation. Any randomization or customization should be done here.

`def postprocess(...)` is used to handle the outputs for the given run of the simulation. It cleans up the output directory and can be used to do any summary statistics or other post-processing.

`save_list` is a list of files in the output directory to keep. All other files will be deleted.


## Simulation performance

For 100 runs of a simple test case (one full orbit):

| Device       | # of cores | Time (s)  |
|:-------------|:----------:|:---------:|
| PC (Native)  |      1     |    425    |
| PC (Native)  |      2     |    219    |
| PC (Native)  |      4     |    105    |
| PC (Native)  |      8     |    56     |
| PC (Native)  |      16    |    38     |
| PC (Devcont) |      1     |    527    |
| PC (Devcont) |      2     |    268    |
| PC (Devcont) |      4     |    125    |
| PC (Devcont) |      8     |    63     |
| PC (Devcont) |      16    |    40     |
| PC (DinD)    |      8     |    63     |
| Pi4 (Native) |      4     |    400    |
| Pi4 (Docker) |      4     |    406    |

\*PC has 8 hyperthreaded cores.

# 42 config

`/42/InOut/` contains a simple example configuration for `42`. If the given template directory does not exist, `./monte_carlo.py` will copy the contents of `/42/InOut/` to the template directory (default is `mc_template/`). The format for the config files is extremely rigid and you must follow the format exactly (even empty lines will break it). `preprocess(...)` makes use of `ReplaceLineInFile(...)` to modify the configuration files.

- `Inp_Sim.txt`   - Top-level simulation configuration
- `SC_Simple.txt` - Spacecraft configuration
- `Orb_LEO.txt`   - Default orbit configuration



# 42 source

The 42 source code is cloned to `/42` and built by the Dockerfile. You can add `/42` to your VSCode workspace to browse the source code. In VSCode, right-click in the Explorer and select "Add Folder to Workspace...". Then select `/42`. 



# Data files

The output files from 42 are not really documented. Some information can be found in the PDFs in the `docs/` folder; the rest needs to be reverse-engineered from the source code. 
The following files are good places to start:

- https://github.com/ericstoneking/42/tree/master/Docs

- Nomenclature.pdf
- 42 Overview.pdf
- 42 Intro to Simulation.pdf
- `/42/Source/42report.c` - Handles writin the output files
- `/42/Include/42types.h` - Defines the data structures

This section summarizes some of the information that has been reverse-engineered thus far.

Output files are written to the directory specified by `--outdir` (default: `./mc_data`). Data files are space-delimited text files, with the extension `.42`. Most files contain only truth-data, while other contain truth-data and "measured" data. 

```c
fprintf(PosNfile,"%le %le %le\n", SC[0].PosN[0],SC[0].PosN[1],SC[0].PosN[2]);
...
fprintf(AccFile,"%le %le ",SC[0].Accel[i].TrueAcc,SC[0].Accel[i].MeasAcc);
```

## Coordinate frames

- N - Inertial frame (ECI)
- W - Rotating frame (ECEF)
- B - Body frame
- R - Reference frame
- L - Local Vertical-Local Horizontal frame


## Data file definitions

Here are descriptions of **some** of the output files.

- `time.42` - Simulation time in seconds (starts at 0)
- `PosX.42` - Position in X frame
- `VelX.42` - Velocity in X frame
- `qbn.42`  - Quaternion of B in N frame
- `wbn.42`  - Angular Velocity of B wrt N expressed in B frame (rad/sec)
- `svn.42`  - Sun-pointing unit vector, expressed in N 
- `svb.42`  - Sun-pointing unit vector, expressed in B 
- `RPY.42`  - Roll, Pitch, Yaw (I believe it's B to R?)
- `HWhl.42` - Wheel angular momentum, (Nms)
- `Hvn.42`  - Total SC angular momentum (Nms) expressed in N
- `Hvb.42`  - Total SC angular momentum (Nms) expressed in B
- `x##.42`  - Kinematic States of spacecraft ##
- `u##.42`  - Dynamic States of spacecraft ##

## Optional data files

Some output files only get written if a payload is included on the spacecraft. For example, you must add an accelerometer to `SC_Simple.txt` to get `Acc.42`.

- `Acc.42` - Accelerometer data
- `MTB.42` - Magnetorquer data
- `Thr.42` - Thruster data
- `Abedo.42` & `Illum.42` - Coarse sun sensor data

Other files are commented out in the source (`//GyroReport();` and `//MagReport();`). These can be enabled by uncommenting the lines in `42report.c` and rebuilding 42.

```bash
cd /42
make
```

# Flight Control Software (FSW)

`FSW Models.pdf` provides info on the flight control options in 42. Here is a brief summary.

- PASSIVE_FSW - No control, forces, or torques. 
- PROTOTYPE_FSW - Simple attitude control using `Inp_Cmd.txt`. Does not use actuators.
- AD_HOC_FSW - Proportional-derivative linear feedback to align the spacecraft with the inertial frame (N). Uses ideal torquers for actuation and we need to modify sensor inputs, commanded attitude, control law, and actuator commanding.
- THREE_AXIS_FSW - More realistic. Wheels and magnetic torquers in LVLH frame, with a single-axis solar array gimbal tracking the Sun. 
- Custom - You can define your own by modifying the source. See `FSW Models.pdf` for more info.

## Sensor Models

`42sensors.c` contains a few basic sensor models, that basically copy the truth data into the flight software data structure and maybe add some noise or bias.

## Actuator Models

`42actuators.c` contains a few basic actuator models. In addition to the normal actuators, it also includes `IdealFrc` and `IdealTrq` which can be used to apply forces and torques directly to the spacecraft (these are used by `PROTOTYPE_FSW` and `AD_HOC_FSW`).