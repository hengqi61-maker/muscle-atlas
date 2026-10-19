# Mac implementation of Windows-owned exchange v1

This folder adopts `schemas/kinematics/packet-v1.schema.json` and executes the Windows-owned `scripts/biomechanics/kinematics.py` directly via `--contract-root`. It does not fork or redefine that contract. Packets describe actual experimental rig observations, not medical or physiological validation. All 27 bone frames are retained. The source meshes and source `.blend` are not edited.

`blender-rest.packet.json` is native armature rest (`model-default`); `gltf-default.packet.json` is default GLB node transforms; `gltf-bind.packet.json` derives frames from the actual skin inverse-bind matrices. The two Blender and two glTF clip packets use actual animation time-zero references plus measured evaluations at 0/25/50/75/100% of each authored diagnostic action. These references are separately named even when numerically close. Non-bone root ancestors are folded into root local transforms so root local equals root world, as required by the v1 validator.

The adapter derives each B from **actual** native rest S0 and GLB default T0, using `B = inverse(S0) * inverse(A) * T0`. A is the explicit proper rotation Rx(-pi/2) from Blender Z-up to glTF Y-up, s=1 metre/metre. `native-gltf-mapping.json` lists every source/target name and numeric B. The forward mapping is `A * S * B`, not an assumed shared Euler convention or a transpose-only conversion. Each native clip sample is numerically compared with the corresponding actual GLTFLoader/AnimationMixer sample, and the mathematical inverse is checked. Reference alignment does not establish anatomical axis, segment-length, shoulder-centre or physiological correctness.

Predeclared matrix-element tolerance is **2e-5** for float32 Blender pose write/save/reopen/read and actual native/glTF phase comparison. Pure double-precision mathematical fixtures use tighter tolerances. `native-observations.json` records actual Blender version, native source SHA, fps, rest and action samples. `validation-report.json` records untouched Windows schema/library hashes and validation results. `native-gltf-import-report.json` records actual glTF packet → inverse A/B → bpy pose import → new isolated native file → reopen/read comparison. The isolated `.blend` outputs are local verification artifacts, not formal asset replacements.

Reproduce native export with Blender Agent `execute_script` using an absolute path:

```python
import runpy, os
os.environ['RIG_EXCHANGE_BLEND'] = '/ABSOLUTE/SOURCE/artifacts/rig-v2/unified-rig-prototype.blend'
runpy.run_path('/ABSOLUTE/CHECKOUT/scripts/rig-v2/blender-exchange-v1.py', run_name='__main__')
```

Set `RIG_EXCHANGE_BLEND` to the original native source and `RIG_EXCHANGE_ROOT` to the adapter checkout when paths differ. Then run with Python containing the Windows requirements:

```sh
python scripts/rig-v2/exchange-v1.py --contract-root /ABSOLUTE/WINDOWS-CONTRACT-CHECKOUT
RIG_CONTRACT_ROOT=/ABSOLUTE/WINDOWS-CONTRACT-CHECKOUT python tests/rig-v2/exchange-v1.test.py
```

Actual packet import uses Blender Agent:

```python
import runpy, os
os.environ['RIG_EXCHANGE_BLEND'] = '/ABSOLUTE/SOURCE/artifacts/rig-v2/unified-rig-prototype.blend'
ns = runpy.run_path('/ABSOLUTE/CHECKOUT/scripts/rig-v2/blender-exchange-v1.py')
ns['import_gltf_packet']()
```

Source/producer commit fields identify the input asset generation and adapter checkout before its output commit; provenance does not recursively embed the packet's own future commit. The final GitHub handoff commit is recorded by the publishing PR. Empty `attachments` means this packet makes no calibrated muscle path-point assertion; the separate source attachment registry remains an uncalibrated authoring record. No synthetic animation, formal finger bending, OpenSim runtime result, or independent anatomical validation is asserted.

Executed results: seven v1 packets passed the unmodified Windows schema plus semantic validator; three Mac exchange tests and all 22 Windows contract tests passed. Actual native-to-glTF maximum element error was 6.998322887863395e-7; mathematical inverse error 6.661338147750939e-16; native save/reopen and imported glTF save/reopen errors were both 2.384185791015625e-7. Source native SHA was unchanged. These numerical results do not release R1 or validate medical motion quality.
