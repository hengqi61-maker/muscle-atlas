import { useGrasp } from "./store";
import { DIGITS, CHAIN } from "./HandRigAdapter";
import { useAtlas } from "../stores/useAtlas";
export function GraspPanel() {
  const s = useGrasp(),
    a = useAtlas(),
    h = s.hands[s.side];
  const preset = (amount: number) =>
    s.hand(s.side, {
      joints: {},
      amount,
      digits: Object.fromEntries(
        DIGITS.map((d) => [d, amount]),
      ) as typeof h.digits,
      released: false,
      auto: false,
    });
  return (
    <details open={s.enabled} className="grasp-panel">
      <summary>Grasp Controller v2 · 实验</summary>
      <label>
        <input
          aria-label="启用抓握 v2"
          type="checkbox"
          checked={s.enabled}
          onChange={(e) => {
            s.set({ enabled: e.target.checked });
            if (e.target.checked)
              a.set({
                playbackKind: "training-unverified",
                model: "pulldown",
                exerciseId: "lat-pulldown",
                mode: "exercise",
                playing: false,
                time: 0,
              });
          }}
        />
        加载原有 30 指骨实验资产
      </label>
      {s.enabled && (
        <>
          <p className="muted">
            骨骼代理求解。真实组织 GEOMETRY_INSUFFICIENT，14
            根指骨无组织权重；非训练验收。
          </p>
          <select
            aria-label="抓握侧"
            value={s.side}
            onChange={(e) => s.set({ side: e.target.value as typeof s.side })}
          >
            <option>Left</option>
            <option>Right</option>
          </select>
          <select
            aria-label="抓握器械"
            value={s.kind}
            onChange={(e) => {
              s.set({ kind: e.target.value as typeof s.kind });
              a.set({
                model: e.target.value === "bar" ? "pulldown" : "rigged",
                exerciseId:
                  e.target.value === "bar" ? "lat-pulldown" : "dumbbell-curl",
                playing: false,
                time: 0,
              });
            }}
          >
            <option value="bar">高位下拉横杆</option>
            <option value="dumbbell">哑铃握柄</option>
            <option value="rope">绳索末端刚性握柄</option>
          </select>
          <div className="segmented">
            {[
              ["张开", 0],
              ["半握", 0.45],
              ["闭合", 1],
            ].map(([label, v]) => (
              <button key={label} onClick={() => preset(Number(v))}>
                {label}
              </button>
            ))}
          </div>
          <button
            onClick={() => {
              const amount =
                  s.kind === "bar" ? 0.72 : s.kind === "rope" ? 0.88 : 0.68,
                thumb =
                  s.kind === "bar" ? 0.62 : s.kind === "rope" ? 0.78 : 0.7;
              s.hand(s.side, {
                joints: {},
                amount,
                digits: {
                  Thumb: thumb,
                  Index: amount,
                  Middle: amount,
                  Ring: amount,
                  Little: amount,
                },
                opposition: thumb * 0.55,
                auto: false,
                released: false,
              });
            }}
          >
            器械握持预设
          </button>
          <label>
            <input
              type="checkbox"
              aria-label="自动抓握"
              checked={h.auto}
              onChange={(e) =>
                s.hand(s.side, { auto: e.target.checked, released: false })
              }
            />
            自动持续求解
          </label>
          <label>
            <input
              aria-label="保持器械参考"
              type="checkbox"
              checked={h.anchor}
              onChange={(e) => s.hand(s.side, { anchor: e.target.checked })}
            />
            保持器械参考（有界上肢修正）
          </label>
          <button onClick={() => s.hand(s.side, { released: !h.released })}>
            {h.released ? "保持抓握" : "释放"}
          </button>
          <label>
            半径 {Math.round(s.radius * 1000)} mm
            <input
              aria-label="握柄半径"
              type="range"
              min=".008"
              max=".04"
              step=".001"
              value={s.radius}
              onChange={(e) => s.set({ radius: +e.target.value })}
            />
          </label>
          <label>
            目标偏移
            <input
              aria-label="握柄移动"
              type="range"
              min="-.1"
              max=".1"
              step=".001"
              value={s.offset}
              onChange={(e) => s.set({ offset: +e.target.value })}
            />
          </label>
          <details>
            <summary>每根手指高级控制</summary>
            {DIGITS.map((d) => (
              <label key={d}>
                {d}
                <input
                  aria-label={`${s.side} ${d}`}
                  type="range"
                  min="0"
                  max="1"
                  step=".01"
                  value={h.digits[d]}
                  onChange={(e) =>
                    s.hand(s.side, {
                      joints: {},
                      digits: { ...h.digits, [d]: +e.target.value },
                      auto: false,
                      released: false,
                    })
                  }
                />
              </label>
            ))}
            <details>
              <summary>独立关节（弧度）</summary>
              {DIGITS.flatMap((d) =>
                CHAIN[d].map((j, i) => {
                  const name = `${s.side}${d}${j}`,
                    max =
                      d === "Thumb"
                        ? [0.35, 1.15, 1.05][i]
                        : [1.15, 1.25, 0.85][i];
                  return (
                    <label key={name}>
                      {d} {j}
                      <input
                        aria-label={name}
                        type="range"
                        min="0"
                        max={max}
                        step=".01"
                        value={h.joints[name] ?? h.digits[d] * max}
                        onChange={(e) =>
                          s.hand(s.side, {
                            joints: { ...h.joints, [name]: +e.target.value },
                            auto: false,
                            released: false,
                          })
                        }
                      />
                    </label>
                  );
                }),
              )}
            </details>
            <label>
              拇指对握
              <input
                aria-label="拇指对握"
                type="range"
                min="0"
                max=".55"
                step=".01"
                value={h.opposition}
                onChange={(e) =>
                  s.hand(s.side, { opposition: +e.target.value })
                }
              />
            </label>
          </details>
          <label>
            <input
              type="checkbox"
              checked={s.axes}
              onChange={(e) => s.set({ axes: e.target.checked })}
            />
            关节轴 / 接触代理
          </label>
          <div className="segmented">
            <button
              onClick={() => a.set({ focus: "grip", reset: a.reset + 1 })}
            >
              手部特写
            </button>
            <button
              onClick={() => a.set({ focus: "side", reset: a.reset + 1 })}
            >
              侧面
            </button>
            <button
              onClick={() => a.set({ focus: "full", reset: a.reset + 1 })}
            >
              正面
            </button>
          </div>
          <button onClick={s.reset}>重置抓握</button>
          <pre
            data-testid="grasp-report"
            style={{ whiteSpace: "pre-wrap", fontSize: 10 }}
          >
            {JSON.stringify(s.report, null, 1)}
          </pre>
        </>
      )}
    </details>
  );
}
