import { useCallback, useEffect, useRef, useState } from "react";
import { LS_DEBUG_WIDTH } from "@/app/storageKeys";

export const DEFAULT_DEBUG_PANEL_WIDTH = 352;
export const MIN_DEBUG_PANEL_WIDTH = 280;
export const MAX_DEBUG_PANEL_WIDTH = 720;

export function clampDebugPanelWidth(
  px: number,
  viewportWidth = typeof window !== "undefined" ? window.innerWidth : 1280,
): number {
  const max = Math.min(
    MAX_DEBUG_PANEL_WIDTH,
    Math.floor(viewportWidth * 0.92),
  );
  return Math.round(Math.min(max, Math.max(MIN_DEBUG_PANEL_WIDTH, px)));
}

export function loadDebugPanelWidth(): number {
  try {
    const raw = localStorage.getItem(LS_DEBUG_WIDTH);
    if (!raw) return DEFAULT_DEBUG_PANEL_WIDTH;
    const n = Number(raw);
    if (!Number.isFinite(n)) return DEFAULT_DEBUG_PANEL_WIDTH;
    return clampDebugPanelWidth(n);
  } catch {
    return DEFAULT_DEBUG_PANEL_WIDTH;
  }
}

export function useDebugPanelResize() {
  const [width, setWidth] = useState(loadDebugPanelWidth);
  const [isResizing, setIsResizing] = useState(false);
  const widthRef = useRef(width);
  widthRef.current = width;

  useEffect(() => {
    const onWindowResize = () => {
      setWidth((current) => clampDebugPanelWidth(current));
    };
    window.addEventListener("resize", onWindowResize);
    return () => window.removeEventListener("resize", onWindowResize);
  }, []);

  const persistWidth = useCallback((next: number) => {
    try {
      localStorage.setItem(LS_DEBUG_WIDTH, String(next));
    } catch {
      /* ignore */
    }
  }, []);

  const onResizePointerDown = useCallback(
    (e: React.PointerEvent<HTMLDivElement>) => {
      if (e.button !== 0) return;
      e.preventDefault();
      const handle = e.currentTarget;
      handle.setPointerCapture(e.pointerId);
      setIsResizing(true);

      const startX = e.clientX;
      const startWidth = widthRef.current;
      const prevCursor = document.body.style.cursor;
      const prevUserSelect = document.body.style.userSelect;
      document.body.style.cursor = "ew-resize";
      document.body.style.userSelect = "none";

      const onMove = (ev: PointerEvent) => {
        setWidth(clampDebugPanelWidth(startWidth + startX - ev.clientX));
      };

      const onEnd = () => {
        setIsResizing(false);
        setWidth((current) => {
          const clamped = clampDebugPanelWidth(current);
          persistWidth(clamped);
          return clamped;
        });
        document.body.style.cursor = prevCursor;
        document.body.style.userSelect = prevUserSelect;
        handle.removeEventListener("pointermove", onMove);
        handle.removeEventListener("pointerup", onEnd);
        handle.removeEventListener("pointercancel", onEnd);
      };

      handle.addEventListener("pointermove", onMove);
      handle.addEventListener("pointerup", onEnd);
      handle.addEventListener("pointercancel", onEnd);
    },
    [persistWidth],
  );

  return { width, isResizing, onResizePointerDown };
}
