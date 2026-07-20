import { useEffect, useId, useRef, type ReactNode } from "react";
import { LEGAL_DISCLAIMER } from "@/content/legalDisclaimer";

interface HelpDialogProps {
  open: boolean;
  onClose: () => void;
}

function HelpSection({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <section className="space-y-2">
      <h3 className="label-caps text-[0.7rem] text-[color:var(--color-led)]">{title}</h3>
      <div className="space-y-2 text-sm leading-relaxed opacity-90">{children}</div>
    </section>
  );
}

export function HelpDialog({ open, onClose }: HelpDialogProps) {
  const titleId = useId();
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) return;
    closeRef.current?.focus();

    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-[60] flex items-start justify-center overflow-y-auto p-4 sm:p-8"
      role="presentation"
    >
      <button
        type="button"
        className="fixed inset-0 bg-[oklch(0.04_0.006_258/0.72)] backdrop-blur-md"
        aria-label="Close help"
        onClick={onClose}
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        className="panel-raised relative z-10 my-auto w-full max-w-2xl rounded-xl border border-[oklch(0.34_0.014_250/0.55)] shadow-[0_28px_80px_oklch(0_0_0/0.65),0_0_60px_oklch(0.62_0.24_27/0.08)]"
      >
        <header className="flex items-center justify-between gap-4 border-b border-border px-5 py-4">
          <h2 id={titleId} className="font-display text-sm tracking-[0.18em] uppercase">
            Help
          </h2>
          <button
            ref={closeRef}
            type="button"
            className="rounded border border-border px-3 py-1 text-xs label-caps hover:bg-secondary/50"
            onClick={onClose}
          >
            Close
          </button>
        </header>

        <div className="max-h-[min(70vh,42rem)] space-y-6 overflow-y-auto px-5 py-5">
          <HelpSection title="Overview">
            <p>
              Freecasti is a browser editor for the Bricasti M7. Pick a preset, adjust
              the controls, and hear your changes reflected immediately. You can save your
              work in this browser, download patch files, or send them to your M7 when MIDI
              is connected.
            </p>
            <p className="text-xs opacity-70">
              This is a community project, not an official Bricasti app. If something
              matters for a session, confirm it on the unit before you trust it.
            </p>
          </HelpSection>

          <HelpSection title="A / B compare">
            <p>
              Two program slots let you load and tweak two presets, then switch
              with <strong>A</strong> and <strong>B</strong> (right of the patch
              name). Bank/program picks and dial edits apply to the active slot
              only. MIDI send and the debug dump always reflect the active slot.
            </p>
          </HelpSection>

          <HelpSection title="Program tab">
            <ul className="list-disc space-y-1.5 pl-5">
              <li>
                <strong>Banks &amp; presets</strong> — Pick a factory bank (Halls, Plates, Rooms,
                …) and a program slot. Loading a preset replaces unlocked parameters with the
                factory values.
              </li>
              <li>
                <strong>Core</strong> — Reverb time (large dial), size, predelay, diffusion,
                density, and modulation.
              </li>
              <li>
                <strong>Reflections, Rolloff, Delay</strong> — Early reflections, HF rolloff /
                VLF, and delay block.
              </li>
              <li>
                <strong>Frequency-dependent decay</strong> — LF/HF RT crossover and multiply
                pairs.
              </li>
              <li>
                <strong>NonLin bank</strong> — Only size, predelay, rolloff, early select, early
                to reverb mix, and early rolloff affect the sound. Other controls are greyed out
                and cannot be edited.
              </li>
            </ul>
          </HelpSection>

          <HelpSection title="System tab">
            <p>Wet/dry gain, audio routing, audio format, output level, display level, MIDI
            channel, and MIDI bank. Some parameters use knobs; routing, format, bank select,
            and level steps use button lists. Hover a label for a short manual-style
            description.</p>
          </HelpSection>

          <HelpSection title="Controls">
            <ul className="list-disc space-y-1.5 pl-5">
              <li>
                <strong>Click a control</strong> to select it (highlight ring). Click empty
                space to deselect.
              </li>
              <li>
                <strong>Click a dial value</strong> — Type a new setting (dB, ms, Hz,
                and so on). Invalid input is ignored; numeric values snap to the nearest
                device step. Button-list parameters are chosen by clicking a button only.
              </li>
              <li>
                <strong>Drag a dial</strong> up/down, scroll the mouse wheel, or double-click to
                reset to the loaded preset&apos;s value (mid-range when no preset value exists).
              </li>
              <li>
                <strong>Padlock</strong> — Locked parameters keep their values when you change
                bank or preset. Toggle the lock under the parameter name.
              </li>
              <li>
                <strong>Metronome</strong> — On predelay, reverb time, and delay time, toggle
                tempo mode to edit in musical divisions (1/4, 1/8T, 1/8D, …). Set BPM in the
                header; arrow keys step through tempo grid positions when tempo mode is on.
              </li>
              <li>
                <strong>Reverb time display</strong> — With tempo mode off, values show as
                seconds or milliseconds. With tempo mode on, values show as note lengths at the
                current BPM.
              </li>
            </ul>
          </HelpSection>

          <HelpSection title="Keyboard">
            <ul className="list-disc space-y-1.5 pl-5">
              <li>
                <strong>↑ / ↓</strong> — Step the selected control (hold Shift for smaller
                steps on large ranges).
              </li>
              <li>
                <strong>Escape</strong> — Clear selection.
              </li>
            </ul>
          </HelpSection>

          <HelpSection title="Saved presets &amp; files">
            <ul className="list-disc space-y-1.5 pl-5">
              <li>
                <strong>Save</strong> — Stores the current program (and system state if present)
                in this browser&apos;s local storage.
              </li>
              <li>
                <strong>Load / Delete</strong> — Restore or remove saved snapshots.
              </li>
              <li>
                <strong>Export .syx</strong> — Download a SysEx file to share or back up.
              </li>
              <li>
                <strong>Import .syx</strong> — Load a program or system dump from disk; the
                editor detects the dump type and switches tabs.
              </li>
            </ul>
          </HelpSection>

          <HelpSection title="MIDI">
            <p>
              MIDI is <strong>off by default</strong>. Turn it on in the toolbar (Chromium-based
              browsers work best), choose output and input ports, then use <strong>Send now</strong>{" "}
              or enable <strong>Send on change</strong> to push each edit to the M7. Incoming
              SysEx on the selected input replaces the matching program or system state.
            </p>
          </HelpSection>

          <HelpSection title="Debug panel">
            <p>
              Opens a side panel with the live hex dump, checksum status, SysEx structure parse,
              last edit summary, byte diff highlights, tempo discrepancy notes, and MIDI traffic
              log. Useful for verifying what the editor is about to send.
            </p>
          </HelpSection>

          <HelpSection title="Known limitations">
            <ul className="list-disc space-y-1.5 pl-5 text-xs opacity-80">
              <li>Saved presets are per-browser; use Export .syx to move between machines.</li>
              <li>EDIT bank receive path (bank index 118) is not implemented.</li>
            </ul>
          </HelpSection>

          <HelpSection title="Legal">
            <p className="text-xs leading-relaxed opacity-80">{LEGAL_DISCLAIMER}</p>
          </HelpSection>
        </div>
      </div>
    </div>
  );
}
