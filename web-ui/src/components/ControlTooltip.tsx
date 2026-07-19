import {
  useCallback,
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  useState,
  type CSSProperties,
  type ReactNode,
} from "react";
import { createPortal } from "react-dom";

interface ControlTooltipProps {
  description?: string;
  placement?: "top" | "bottom" | "auto";
  /** Hide while true (e.g. dial drag in progress). */
  suppressed?: boolean;
  showDelayMs?: number;
  children: ReactNode;
}

const GAP = 8;
const VIEWPORT_PAD = 8;
const DEFAULT_SHOW_DELAY_MS = 500;

const HIDDEN_STYLE: CSSProperties = {
  position: "fixed",
  top: 0,
  left: 0,
  visibility: "hidden",
  zIndex: 9999,
};

export function ControlTooltip({
  description,
  placement = "auto",
  suppressed = false,
  showDelayMs = DEFAULT_SHOW_DELAY_MS,
  children,
}: ControlTooltipProps) {
  const id = useId();
  const anchorRef = useRef<HTMLSpanElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const enterTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pointerInsideRef = useRef(false);
  const [open, setOpen] = useState(false);
  const [tooltipStyle, setTooltipStyle] = useState<CSSProperties>(HIDDEN_STYLE);
  const [visible, setVisible] = useState(false);

  const clearEnterTimer = useCallback(() => {
    if (enterTimerRef.current) {
      clearTimeout(enterTimerRef.current);
      enterTimerRef.current = null;
    }
  }, []);

  const hide = useCallback(() => {
    clearEnterTimer();
    setOpen(false);
    setVisible(false);
    setTooltipStyle(HIDDEN_STYLE);
  }, [clearEnterTimer]);

  const scheduleShow = useCallback(() => {
    if (suppressed) return;
    clearEnterTimer();
    enterTimerRef.current = setTimeout(() => {
      enterTimerRef.current = null;
      if (!suppressed) setOpen(true);
    }, showDelayMs);
  }, [clearEnterTimer, showDelayMs, suppressed]);

  const positionTooltip = useCallback(() => {
    const anchor = anchorRef.current;
    const tooltip = tooltipRef.current;
    if (!anchor || !tooltip) return;

    const anchorRect = anchor.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();
    const needed = tooltipRect.height + GAP;

    let side: "top" | "bottom";
    if (placement === "auto") {
      const spaceAbove = anchorRect.top - VIEWPORT_PAD;
      const spaceBelow = window.innerHeight - anchorRect.bottom - VIEWPORT_PAD;
      if (spaceAbove >= needed) side = "top";
      else if (spaceBelow >= needed) side = "bottom";
      else side = spaceBelow >= spaceAbove ? "bottom" : "top";
    } else {
      side = placement;
      if (side === "top" && anchorRect.top - needed < VIEWPORT_PAD) side = "bottom";
      else if (
        side === "bottom" &&
        anchorRect.bottom + needed > window.innerHeight - VIEWPORT_PAD
      ) {
        side = "top";
      }
    }

    const top =
      side === "top"
        ? anchorRect.top - tooltipRect.height - GAP
        : anchorRect.bottom + GAP;

    let left = anchorRect.left + anchorRect.width / 2 - tooltipRect.width / 2;
    left = Math.max(
      VIEWPORT_PAD,
      Math.min(left, window.innerWidth - tooltipRect.width - VIEWPORT_PAD),
    );

    setTooltipStyle({
      position: "fixed",
      top: Math.max(VIEWPORT_PAD, top),
      left,
      zIndex: 9999,
    });
    setVisible(true);
  }, [placement]);

  useLayoutEffect(() => {
    if (!open) {
      setVisible(false);
      setTooltipStyle(HIDDEN_STYLE);
      return;
    }

    positionTooltip();

    const onReposition = () => positionTooltip();
    window.addEventListener("scroll", onReposition, true);
    window.addEventListener("resize", onReposition);
    return () => {
      window.removeEventListener("scroll", onReposition, true);
      window.removeEventListener("resize", onReposition);
    };
  }, [open, description, positionTooltip]);

  useEffect(() => {
    if (suppressed) {
      hide();
      return;
    }
    if (pointerInsideRef.current) {
      scheduleShow();
    }
  }, [suppressed, hide, scheduleShow]);

  useEffect(() => () => clearEnterTimer(), [clearEnterTimer]);

  if (!description) return <>{children}</>;

  return (
    <>
      <span
        ref={anchorRef}
        className="inline-flex max-w-full justify-center"
        onMouseEnter={() => {
          pointerInsideRef.current = true;
          scheduleShow();
        }}
        onMouseLeave={() => {
          pointerInsideRef.current = false;
          hide();
        }}
        onFocusCapture={() => {
          pointerInsideRef.current = true;
          scheduleShow();
        }}
        onBlurCapture={() => {
          pointerInsideRef.current = false;
          hide();
        }}
        aria-describedby={open ? id : undefined}
      >
        {children}
      </span>
      {open &&
        createPortal(
          <div
            ref={tooltipRef}
            id={id}
            role="tooltip"
            style={tooltipStyle}
            className={`pointer-events-none w-[min(15rem,72vw)] rounded-md border border-border bg-[oklch(0.12_0.009_252)] px-3 py-2 text-xs font-normal normal-case leading-relaxed tracking-normal text-[color:var(--color-foreground)] shadow-xl transition-opacity duration-150 ${
              visible ? "opacity-100" : "opacity-0"
            }`}
          >
            {description}
          </div>,
          document.body,
        )}
    </>
  );
}
