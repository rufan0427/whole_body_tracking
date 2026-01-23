# Motion Retargeting and Motion Tracking for Humanoid Robot

> **Note**: Before making your hands dirty, please read the corresponding part (even including troubleshooting) in the README.md file carefully.

In this homework, you will retarget human motion to a specific humanoid robot (Unitree G1) and then train a motion tracking policy to track the retargeted motion in simulator (IsaacSim 4.5).

## Content
+ 1.Motion Retargeting
    + A. Data preparation
    + B. Fitting motion data from AMASS
    + C. Visualizing the fitted motion data
+ 2.Motion Tracking
    + A. Install Isaacsim 4.5
    + B. Install IsaacLab
    + C. Install BeyondMimic
    + D. Run the example
    + E. Train your own motion tracking policy


## 1. Motion Retargeting (Windows/Linux available)

Motion retargeting is regarded as mapping the human motion sequences to the robot's motion trajectory, which taking human pose parameters (beta, pose, etc.) as input and output the robot's DoF parameters through [optimization-based method](https://github.com/YanjieZe/GMR) or gradient-based method (this homework).

Here we use [uv](https://docs.astral.sh/uv/) to manage the retarget project, make sure you have installed uv first.

Please clone [Retarget repo](https://github.com/xiaohu-art/phc-retarget) for complete homework and then follow the instructions to finish the motion retargeting.

### A. Data preparation

Download the smpl model first:
```bash
uv run gdown --folder https://drive.google.com/drive/folders/1eSfJma_5VuNqaw_IRE8xVn6UgAmvjoeT\?usp\=drive_link -O ./data/smpl
```

Under the `data/AMASS` folder, I have downloaded one motion file for instance:
```bash
|-- data
|   |-- AMASS
|       |-- SFU                                 # sub-dataset name
|           |-- 0005                            # subject id
|               |-- 0005_Walking001_poses.npz   # motion file name
|               |-- ...
```
Of course, you can download the other motion files you like from the [AMASS](https://amass.is.tue.mpg.de/) website, of which body model is [SMPL](https://smpl.is.tue.mpg.de/). SMPL model consists of body shape parameters (beta) and body pose parameters (pose), and describes the human body motion with the root translation. For more details, please refer to the [SMPLX repository](https://github.com/vchoutas/smplx/blob/1265df7ba545e8b00f72e7c557c766e15c71632f/smplx/body_models.py#L76).

### B. Fitting motion data from AMASS

First we need to fit the smpl shape to the humanoid robot:
```bash
uv run scripts/1-fit_smpl_shape.py
```
It will save the fitted smpl `beta` parameters and the corresponding `scale` parameters in the `data/g1_29dof/shape_optimized_v1.pkl` folder.

Then we need to fit the motion data to the humanoid robot:
```bash
uv run scripts/2-fit_smpl_motion.py +amass_root=./data/AMASS
```
If you only have one motion file, it will save the fitted motion data in the `data/g1_29dof/v1/singles` folder.
Otherwise, it will save the fitted motion data in the `data/g1_29dof/v1/amass_all.pkl`.

Finally, we can visualize the fitted motion data:
```bash
# for single motion file
uv run scripts/3-vis_q_mj.py +motion_file=./data/g1_29dof/v1/singles/0005_Walking001_poses.pkl

# for multiple motion files
uv run scripts/3-vis_q_mj.py +motion_file=./data/g1_29dof/v1/amass_all.pkl
```

After the fitting process, you will get the motion data in the `.pkl` file.

## 2. Motion Tracking (Linux recommended)

Motion tracking learns a control policy by reinforcement learning, that is, given the retargeted reference motion and the robot’s current observations/state as inputs, outputs low-level actions (e.g., target joint positions / torques) to make the robot follow that reference motion.

Here we refer to [BeyondMimic](https://github.com/HybridRobotics/whole_body_tracking) as the motion tracking framework.

### A. Install Isaacsim 4.5
You can install Isaacsim 4.5 by first download package:
```bash
wget https://download.isaacsim.omniverse.nvidia.com/isaac-sim-standalone%404.5.0-rc.36%2Brelease.19112.f59b3005.gl.linux-x86_64.release.zip
```
and then unzip it following the instructions in [isaacsim installation](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/installation/install_workstation.html).

You can also set `ISAACSIM_PATH` for convenience.

### B. Install IsaacLab
Install IsaacLab and setup a conda environment:
```bash
conda create -n <your_env_name> python=3.10
conda activate <your_env_name>

# install IsaacLab to the exisiting conda environment
# git clone https://github.com/isaac-sim/IsaacLab.git
git clone git@github.com:isaac-sim/IsaacLab.git # SSH recommended
git checkout v2.1.1
cd IsaacLab
ln -s $ISAACSIM_PATH _isaac_sim
./isaaclab.sh -c <your_env_name>
./isaaclab.sh -i rsl_sl skrl # install rsl_sl and skrl for this homework
# reactivate the environment
deactivate
conda activate <your_env_name>
echo $PYTHONPATH 
```
You should see the isaac-sim related dependencies are added to `PYTHONPATH`.

### C. Install BeyondMimic

After we create the conda environment, we can install `whole_body_tracking` by: 
```bash
# here we use the motion tracking repo from the instructor
# which bypass the complex setup with wandb
git clone https://github.com/xiaohu-art/whole_body_tracking.git
```

Then follow the instructions in **Installation** and **Motion preprocessing** in the `README.md` file to install the package and prepare the retargeted motion data.

### D. Run the example

You can now train the motion tracking policy to track a specific motion clip:
```bash
# Change the project name and run name to your own

# Motion Preprocessing
python scripts/csv_to_npz.py --input_file LAFAN1/g1/dance1_subject1.csv --input_fps 30 --output_dir LAFAN1/g1/output --output_name dance1_subject1 --headless

# Make sure the motion data is correct
python scripts/replay_npz.py --motion_file LAFAN1/g1/output/dance1_subject1.npz

# Train
python scripts/rsl_rl/train.py --task=Tracking-Flat-G1-v0 \
--motion_file LAFAN1/g1/output/dance1_subject1.npz \
--headless --logger wandb --log_project_name {project_name} --run_name {run_name}

# Play
python scripts/rsl_rl/play.py --task=Tracking-Flat-G1-v0 --num_envs=2 --motion_file LAFAN1/g1/output/dance1_subject1.npz

# If you want to render in real-time, you can try:
python scripts/rsl_rl/play.py --task=Tracking-Flat-G1-v0 --num_envs=1 --motion_file LAFAN1/g1/output/dance1_subject1.npz --device cpu --real-time
```

### E. Train your own motion tracking policy
Now you have the retargeted motion data of your own in Part A, and you have the motion tracking framework to train the motion tracking policy. You are supposed to change the input retargeted motion file to your own retargeted motion data `{phc retargeted motion}.pkl`.

```bash
python scripts/pkl_to_npz.py --input_file {phc retargeted motion}.pkl --input_fps 30 --output_dir phc-retarget/output --output_name {output_name} --headless

python scripts/replay_npz.py --motion_file phc-retarget/output/{output_name}.npz

# Train
python scripts/rsl_rl/train.py --task=Tracking-Flat-G1-v0 \
--motion_file phc-retarget/output/{output_name}.npz \
--headless --logger wandb --log_project_name {project_name} --run_name {run_name}

# Play
python scripts/rsl_rl/play.py --task=Tracking-Flat-G1-v0 --num_envs=2 --motion_file phc-retarget/output/{output_name}.npz
```

You are also highly encouraged to modify observation space, reward function, etc. to achieve better performance.

# Submission

1. [Credits 30] For motion retargeting, please submit the retargeted motion `.pkl` data and the video
2. [Credits 30] For motion tracking, please submit the play video of the example motion tracking task
3. [Credits 30] For your own motion tracking task, please submit the play video of your retargeted motion
4. [Credits 10] A short report on what you have done to 
    + modify retargeting process for better numerical accuracy and stability
    + finetune the motion tracking policy and the improvements you have made
5. [Bonus][Credits 5] The robot description file used in retargeting is from [Unitree](https://github.com/unitreerobotics/unitree_ros) but we have modified it in some way. Find the modified part and explain it to earn extra credits 

If you have any problems / bugs, feel free to contact us TA / Prof in WeChat group / Web Learning QWQ.

# Troubleshooting
 > **Note**: We highly recommend you to use Linux for **Motion Tracking** part. But if you only have Windows system, or you find the installation process too complicated, you can try with `uv` instead:

> ```bash
> uv venv --python=3.10
> source ./.venv/bin/activate
> 
> uv pip install torch==2.5.1 torchvision==0.20.1
> uv pip install 'isaacsim[all,extscache]==4.5.0' --extra-index-url https://pypi.nvidia.com
> uv pip install isaaclab[isaacsim,all]==2.1.0 --extra-index-url https://pypi.nvidia.com
> 
> # after clone the motion tracking repo
> uv pip install -e ./source/whole_body_tracking
> ```
> 
> *(Tested on Ubuntu 20.04 LTS, CUDA 12.4, Python 3.10)*

Other potential issues:
 - https://github.com/HybridRobotics/whole_body_tracking/issues/34
 - ...
