"""Independent two-link SI model; validates mechanics, never human measurements."""
import json

import mujoco
import numpy as np

XML = """<mujoco><option timestep="0.001" gravity="0 0 -9.81"/>
<worldbody><body pos="0 0 1"><joint name="shoulder" axis="0 1 0"/>
<geom type="capsule" fromto="0 0 0 0 0 -.3" size=".025" mass="1"/>
<body pos="0 0 -.3"><joint name="elbow" axis="0 1 0"/>
<geom type="capsule" fromto="0 0 0 0 0 -.25" size=".02" mass=".7"/>
<site name="tip" pos="0 0 -.25"/></body></body></worldbody></mujoco>"""


def run():
    model = mujoco.MjModel.from_xml_string(XML)
    data = mujoco.MjData(model)
    data.qpos[:] = [.3, -.5]
    mujoco.mj_forward(model, data)
    tip = data.site_xpos[0].copy()
    jac = np.zeros((3, model.nv))
    mujoco.mj_jacSite(model, data, jac, None, 0)
    finite_difference = np.zeros_like(jac)
    for i in range(model.nv):
        data.qpos[i] += 1e-6
        mujoco.mj_forward(model, data)
        finite_difference[:, i] = (data.site_xpos[0] - tip) / 1e-6
        data.qpos[i] -= 1e-6
    np.testing.assert_allclose(jac, finite_difference, atol=1e-6)
    data.qvel[:] = [.2, -.1]
    data.qacc[:] = [.4, -.3]
    mujoco.mj_inverse(model, data)
    torque = data.qfrc_inverse.copy()
    data.qfrc_applied[:] = torque
    mujoco.mj_forward(model, data)
    np.testing.assert_allclose(data.qacc, [.4, -.3], atol=1e-9)
    for _ in range(1000):
        mujoco.mj_step(model, data)
    assert np.isfinite(data.qpos).all() and abs(data.time - 1) < 1e-10
    return {"version": mujoco.__version__, "dof": model.nv,
            "jacobian_max_error": float(np.max(np.abs(jac - finite_difference))),
            "inverse_torque_Nm": torque.tolist(), "simulation_seconds": data.time,
            "scope": "Synthetic rigid links, CPU dynamics; no muscles, EMG or human calibration."}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
