import { lazy, Suspense, type PointerEvent as ReactPointerEvent } from "react";
import type { DebugPanelBodyProps } from "./DebugPanelBody";

const DebugPanelBody = lazy(() =>
  import("./DebugPanelBody").then((m) => ({ default: m.DebugPanelBody })),
);

interface DebugPanelProps extends DebugPanelBodyProps {
  open: boolean;
  onToggle: () => void;
  width: number;
  onResizePointerDown: (e: ReactPointerEvent<HTMLDivElement>) => void;
}

export function DebugPanel({
  open,
  onToggle,
  width,
  onResizePointerDown,
  ...body
}: DebugPanelProps) {
  return (
    <>
      <div
        className={`fixed inset-0 z-40 bg-black/40 transition-opacity duration-300 md:hidden ${
          open ? "cursor-pointer opacity-100" : "pointer-events-none opacity-0"
        }`}
        aria-hidden={!open}
        onClick={onToggle}
      />
      <aside
        className={`fixed inset-y-0 right-0 z-50 flex flex-col border-l border-border panel-raised shadow-2xl transition-transform duration-300 ease-out ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
        style={{ width }}
        aria-hidden={!open}
        aria-label="Debug panel"
      >
        <div
          role="separator"
          aria-orientation="vertical"
          aria-label="Resize debug panel"
          className="absolute inset-y-0 -left-1 z-10 w-2 touch-none cursor-ew-resize before:absolute before:inset-y-0 before:left-1/2 before:w-px before:-translate-x-1/2 before:bg-border/60 hover:before:bg-primary/70 active:before:bg-primary"
          onPointerDown={onResizePointerDown}
        />
        <header className="flex shrink-0 items-center justify-between gap-3 border-b border-border px-4 py-3">
          <h2 className="label-caps">Debug</h2>
          <button
            type="button"
            className="rounded border border-border px-2 py-1 text-xs label-caps hover:bg-secondary/50"
            onClick={onToggle}
            aria-label="Close debug panel"
          >
            Close
          </button>
        </header>
        <div className="min-h-0 flex-1 overflow-y-auto">
          {open && (
            <Suspense
              fallback={
                <div className="panel-recess px-4 py-4 text-xs opacity-70">
                  Loading debug panel…
                </div>
              }
            >
              <DebugPanelBody {...body} />
            </Suspense>
          )}
        </div>
      </aside>
      {!open && (
        <button
          type="button"
          className="fixed right-0 top-1/2 z-30 -translate-y-1/2 rounded-l-md border border-r-0 border-border panel-raised px-2 py-4 label-caps text-[0.6rem] leading-tight hover:bg-secondary/40 [writing-mode:vertical-rl]"
          onClick={onToggle}
          aria-label="Open debug panel"
        >
          Debug
        </button>
      )}
    </>
  );
}
