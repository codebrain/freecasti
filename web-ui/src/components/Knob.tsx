import { useCallback, useEffect, useRef, useState } from "react";

import { EditableValue } from "@/components/EditableValue";
import { PadlockIcon } from "@/components/PadlockIcon";

function polar(cx: number, cy: number, r: number, deg: number) {
  const rad = ((deg - 90) * Math.PI) / 180;
  return { x: cx + Math.cos(rad) * r, y: cy + Math.sin(rad) * r };
}

function arcPath(
  cx: number,
  cy: number,
  r: number,
  startDeg: number,
  endDeg: number,
): string {
  if (endDeg <= startDeg) return "";
  const start = polar(cx, cy, r, startDeg);
  const end = polar(cx, cy, r, endDeg);
  const sweep = endDeg - startDeg;
  const large = sweep > 180 ? 1 : 0;
  return `M ${start.x} ${start.y} A ${r} ${r} 0 ${large} 1 ${end.x} ${end.y}`;
}

/** Evenly spaced dial tick markers (angular), capped for dense controls. */
export function dialTickMarkers(
  stepCount: number,
  maxTicks: number,
  valuePct: number,
): { angle: number; active: boolean; key: number }[] {
  if (stepCount <= 0) return [];
  const displayTickCount = stepCount === 1 ? 1 : Math.min(stepCount, maxTicks);
  return Array.from({ length: displayTickCount }, (_, i) => {
    const t = displayTickCount > 1 ? i / (displayTickCount - 1) : 0;
    return {
      angle: -135 + t * 270,
      active: t <= valuePct + 0.0001,
      key: i,
    };
  });
}

interface KnobProps {
  value: number;
  min: number;
  max: number;
  step?: number;
  onChange: (v: number) => void;
  size?: number;
  label?: string;
  format?: (v: number) => string;
  /** Shown under the dial; click to type when editable. */
  displayValue?: string;
  onValueCommit?: (draft: string) => void;
  valueAriaLabel?: string;
  /** Larger hero styling — same palette, more presence (e.g. reverb time). */
  featured?: boolean;
  disabled?: boolean;
  /** Keyboard / click selection — glow on outer dial ring only. */
  selected?: boolean;
  /** Preset lock — show padlock in place of dial face; tick markers remain. */
  locked?: boolean;
  onDraggingChange?: (dragging: boolean) => void;
}

export function Knob({
  value,
  min,
  max,
  step = 1,
  onChange,
  size = 68,
  label,
  format,
  displayValue,
  onValueCommit,
  valueAriaLabel,
  featured = false,
  disabled = false,
  selected = false,
  locked = false,
  onDraggingChange,
}: KnobProps) {
  const [dragging, setDragging] = useState(false);
  const startY = useRef(0);
  const startVal = useRef(value);

  const range = max - min;
  const pct = range > 0 ? (value - min) / range : 0;
  const angle = -135 + pct * 270;

  const interactive = !disabled && !locked;

  useEffect(() => {
    onDraggingChange?.(dragging);
  }, [dragging, onDraggingChange]);

  const onPointerDown = (e: React.PointerEvent) => {
    if (!interactive) return;
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
    startY.current = e.clientY;
    startVal.current = value;
    setDragging(true);
  };

  const onPointerMove = useCallback(
    (e: PointerEvent) => {
      if (!dragging) return;
      const dy = startY.current - e.clientY;
      const sensitivity = e.shiftKey ? 500 : 150;
      const delta = (dy / sensitivity) * range;
      let next = startVal.current + delta;
      next = Math.round(next / step) * step;
      next = Math.max(min, Math.min(max, next));
      onChange(next);
    },
    [dragging, range, step, min, max, onChange],
  );

  const onPointerUp = useCallback(() => setDragging(false), []);

  useEffect(() => {
    if (!dragging) return;
    window.addEventListener("pointermove", onPointerMove);
    window.addEventListener("pointerup", onPointerUp);
    return () => {
      window.removeEventListener("pointermove", onPointerMove);
      window.removeEventListener("pointerup", onPointerUp);
    };
  }, [dragging, onPointerMove, onPointerUp]);

  const onDoubleClick = () => {
    if (!interactive) return;
    const midpoint = min + range / 2;
    onChange(Math.round(midpoint / step) * step);
  };

  const tickStroke = featured ? 2.4 : 1.6;
  const pointerW = featured ? 4.5 : 3;
  const pad = featured ? 24 : 12;
  const neutralDialFace = disabled
    ? "radial-gradient(circle at 35% 30%, oklch(0.34 0.012 250) 0%, oklch(0.19 0.009 252) 55%, oklch(0.11 0.007 255) 100%)"
    : "radial-gradient(circle at 32% 26%, oklch(0.38 0.018 250) 0%, oklch(0.2 0.011 252) 52%, oklch(0.11 0.008 255) 100%)";
  const neutralDialShadow = disabled
    ? "inset 0 2px 4px oklch(0.45 0.012 250 / 0.3), inset 0 -6px 12px oklch(0 0 0 / 0.7), 0 6px 14px oklch(0 0 0 / 0.55)"
    : "inset 0 2px 5px oklch(0.5 0.02 250 / 0.22), inset 0 -8px 14px oklch(0 0 0 / 0.75), 0 8px 20px oklch(0 0 0 / 0.5), 0 0 24px oklch(0.62 0.24 27 / 0.06)";
  const dialFace = disabled
    ? neutralDialFace
    : featured
      ? "radial-gradient(circle at 38% 26%, oklch(0.46 0.06 27) 0%, oklch(0.22 0.015 252) 46%, oklch(0.1 0.008 255) 100%)"
      : neutralDialFace;
  const dialShadow = disabled
    ? neutralDialShadow
    : featured
      ? "inset 0 2px 8px oklch(0.58 0.06 27 / 0.28), inset 0 -12px 22px oklch(0 0 0 / 0.82), 0 0 40px oklch(0.64 0.245 27 / 0.28), 0 14px 36px oklch(0 0 0 / 0.72)"
      : neutralDialShadow;
  const dialBorder = disabled
    ? "1px solid oklch(0.1 0.008 252)"
    : "1px solid oklch(0.22 0.012 250 / 0.65)";

  const stepCount = range > 0 ? Math.floor(range / step) + 1 : 1;
  const maxTicks = featured ? 37 : 25;
  const ticks = dialTickMarkers(stepCount, maxTicks, pct).map((t) => ({
    a: t.angle,
    active: !disabled && t.active,
    key: t.key,
  }));

  const disabledTickStroke = "oklch(0.52 0.012 85)";
  const disabledTickStrokeDim = "oklch(0.4 0.01 252)";

  const radius = size / 2;
  const frame = size + pad * 2;
  const outerRingR = radius + (featured ? 16 : 11);
  const arcR = radius + (featured ? 9 : 8);
  const arcStart = -135;
  const arcEnd = -135 + pct * 270;

  const resolvedDisplay =
    displayValue ?? (format ? format(value) : value.toFixed(0));

  return (
    <div className="flex flex-col items-center gap-2 select-none">
      {label && (
        <div
          className={`${featured ? "text-[0.72rem] tracking-[0.22em]" : ""} ${
            disabled ? "label-caps-muted" : "label-caps"
          }`}
        >
          {label}
        </div>
      )}
      <div
        className={`relative ${
          interactive ? "touch-none cursor-ns-resize" : locked ? "pointer-events-none" : "cursor-not-allowed pointer-events-none"
        }`}
        style={{ width: frame, height: frame }}
        onPointerDown={onPointerDown}
        onDoubleClick={onDoubleClick}
      >
        <svg
          className="absolute inset-0"
          width={frame}
          height={frame}
          viewBox={`0 0 ${frame} ${frame}`}
        >
          {featured && !locked && !disabled && arcEnd > arcStart && (
            <path
              d={arcPath(frame / 2, frame / 2, arcR, arcStart, arcEnd)}
              fill="none"
              stroke="var(--color-led)"
              strokeWidth={3.5}
              strokeLinecap="round"
              opacity={0.9}
              style={{
                filter:
                  "drop-shadow(0 0 6px var(--color-led)) drop-shadow(0 0 14px oklch(0.62 0.24 27 / 0.65))",
              }}
            />
          )}
          {selected && !disabled && (
            <circle
              cx={frame / 2}
              cy={frame / 2}
              r={outerRingR}
              fill="none"
              stroke="var(--color-primary)"
              strokeWidth={featured ? 2 : 1.75}
              opacity={0.9}
              style={{
                filter:
                  "drop-shadow(0 0 6px var(--color-led)) drop-shadow(0 0 14px oklch(0.62 0.24 27 / 0.55))",
              }}
            />
          )}
          {ticks.map((t) => {
            const cx = frame / 2;
            const cy = frame / 2;
            const rOuter = radius + (featured ? 14 : 10);
            const rInner = radius + (featured ? 7 : 5);
            const rad = (t.a - 90) * (Math.PI / 180);
            const x1 = cx + Math.cos(rad) * rInner;
            const y1 = cy + Math.sin(rad) * rInner;
            const x2 = cx + Math.cos(rad) * rOuter;
            const y2 = cy + Math.sin(rad) * rOuter;
            return (
              <line
                key={t.key}
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke={
                  disabled
                    ? t.active
                      ? disabledTickStroke
                      : disabledTickStrokeDim
                    : t.active
                      ? "var(--color-led)"
                      : "var(--color-led-dim)"
                }
                strokeWidth={tickStroke}
                opacity={
                  disabled
                    ? t.active
                      ? 0.55
                      : 0.35
                    : t.active
                      ? featured
                        ? 1
                        : 0.95
                      : featured
                        ? 0.4
                        : 0.35
                }
                style={
                  !disabled && t.active
                    ? {
                        filter: featured
                          ? "drop-shadow(0 0 5px var(--color-led)) drop-shadow(0 0 10px oklch(0.62 0.24 27 / 0.5))"
                          : "drop-shadow(0 0 3px var(--color-led))",
                      }
                    : undefined
                }
              />
            );
          })}
        </svg>
        {locked ? (
          <div
            className={`absolute flex items-center justify-center ${
              disabled
                ? "text-[color:var(--color-label)] opacity-40"
                : "text-[color:var(--color-led)]"
            }`}
            style={{
              top: pad,
              left: pad,
              width: size,
              height: size,
              filter: disabled
                ? undefined
                : "drop-shadow(0 0 8px var(--color-led)) drop-shadow(0 0 16px oklch(0.62 0.24 27 / 0.55))",
            }}
          >
            <PadlockIcon
              locked
              className=""
              style={{ width: size * (featured ? 0.38 : 0.36), height: size * (featured ? 0.38 : 0.36) }}
            />
          </div>
        ) : (
        <div
          className="absolute rounded-full"
          style={{
            top: pad,
            left: pad,
            width: size,
            height: size,
            background: dialFace,
            boxShadow: dialShadow,
            border: dialBorder,
          }}
        >
          {featured && !locked && !disabled && (
            <div
              className="pointer-events-none absolute inset-0 rounded-full opacity-40"
              style={{
                background:
                  "radial-gradient(circle at 35% 28%, oklch(0.75 0.08 27 / 0.35), transparent 55%)",
              }}
            />
          )}
          <div
            className="absolute left-1/2 top-1/2"
            style={{
              transform: `translate(-50%, -50%) rotate(${angle}deg)`,
              width: pointerW,
              height: size * 0.44,
              transformOrigin: "50% 50%",
              pointerEvents: "none",
            }}
          >
            <div
              className="mx-auto rounded-sm"
              style={{
                width: pointerW,
                height: size * 0.22,
                background: disabled
                  ? "oklch(0.55 0.01 252)"
                  : featured
                    ? "linear-gradient(180deg, oklch(0.98 0.04 60), oklch(0.88 0.12 27))"
                    : "oklch(0.95 0.03 60)",
                boxShadow: disabled
                  ? "none"
                  : featured
                    ? "0 0 10px oklch(0.9 0.1 27 / 0.9), 0 0 4px oklch(0.95 0.05 60 / 0.8)"
                    : "0 0 6px oklch(0.9 0.05 60 / 0.7)",
              }}
            />
          </div>
        </div>
        )}
      </div>
      {onValueCommit ? (
        <EditableValue
          displayValue={resolvedDisplay}
          disabled={!interactive}
          dimmed={disabled}
          featured={featured}
          size={size}
          ariaLabel={valueAriaLabel ?? label}
          onCommit={onValueCommit}
        />
      ) : (
        <div
          className={`tabular-nums min-h-[1.25rem] ${
            disabled ? "control-value-inactive" : "led-text"
          } ${
            featured
              ? "text-2xl font-medium tracking-wide"
              : size >= 100
                ? "text-lg"
                : "text-sm"
          }`}
        >
          {resolvedDisplay}
        </div>
      )}
    </div>
  );
}
