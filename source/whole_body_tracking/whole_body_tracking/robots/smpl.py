import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

from whole_body_tracking.assets import ASSET_DIR

##
# Configuration
##

SMPL_HUMANOID = ArticulationCfg(
    prim_path="{ENV_REGEX_NS}/Robot",
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ASSET_DIR}/smpl/smpl_humanoid.usda",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=None,
            max_depenetration_velocity=10.0,
            enable_gyroscopic_forces=True,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=4,
            solver_velocity_iteration_count=0,
            sleep_threshold=0.005,
            stabilization_threshold=0.001,
        ),
        copy_from_source=True,
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.95),
        rot=(1.0, 0.0, 0.0, 0.0),
        joint_pos={".*": 0.0},
        joint_vel={".*": 0.0},
    ),
    actuators={
        "legs": ImplicitActuatorCfg(
            joint_names_expr=["L_Hip_.*", "R_Hip_.*", "L_Knee_.*", "R_Knee_.*", "L_Ankle_.*", "R_Ankle_.*"],
            stiffness=800.0, damping=80.0, effort_limit_sim=3000.0, velocity_limit_sim=50.0, armature=0.02,
        ),
        "toes": ImplicitActuatorCfg(
            joint_names_expr=["L_Toe_.*", "R_Toe_.*"],
            stiffness=500.0, damping=50.0, effort_limit_sim=3000.0, velocity_limit_sim=50.0, armature=0.02,
        ),
        "spine": ImplicitActuatorCfg(
            joint_names_expr=["Spine_.*"],
            stiffness=1000.0, damping=100.0, effort_limit_sim=3000.0, velocity_limit_sim=50.0, armature=0.02,
        ),
        "head": ImplicitActuatorCfg(
            joint_names_expr=["Neck_.*", "Head_.*"],
            stiffness=500.0, damping=50.0, effort_limit_sim=3000.0, velocity_limit_sim=50.0, armature=0.02,
        ),
        "shoulders": ImplicitActuatorCfg(
            joint_names_expr=["L_Thorax_.*", "R_Thorax_.*", "L_Shoulder_.*", "R_Shoulder_.*", "L_Elbow_.*", "R_Elbow_.*"],
            stiffness=500.0, damping=50.0, effort_limit_sim=3000.0, velocity_limit_sim=50.0, armature=0.02,
        ),
        "wrists": ImplicitActuatorCfg(
            joint_names_expr=["L_Wrist_.*", "R_Wrist_.*"],
            stiffness=300.0, damping=30.0, effort_limit_sim=3000.0, velocity_limit_sim=50.0, armature=0.02,
        ),
        "fingers": ImplicitActuatorCfg(
            joint_names_expr=[".*Index.*", ".*Middle.*", ".*Ring.*", ".*Pinky.*", ".*Thumb.*"],
            stiffness=100.0, damping=10.0, effort_limit_sim=3000.0, velocity_limit_sim=50.0, armature=0.02,
        ),
    },
)
