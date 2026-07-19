import { useCallback, useState } from "react";
import type { SavedUserPreset } from "@/presets/userPresets";
import {
  deleteUserPreset,
  listUserPresets,
  LS_USER_PRESETS,
  saveUserPreset,
  type StorageLike,
} from "@/presets/userPresets";
import type { ProgSerializeState } from "@/sysex/serialize";
import { downloadSyx, suggestSyxFilename } from "@/sysex/syxIo";
import { toolbarButtonClass } from "@/components/toolbarButtons";

const savedBtn = `${toolbarButtonClass(false)} text-xs`;

interface SavedPresetsPanelProps {
  progState: ProgSerializeState;
  progBytes: Uint8Array | null;
  sysState: Record<string, number>;
  sysBytes: Uint8Array | null;
  onLoad: (preset: SavedUserPreset) => void;
  onImportClick: () => void;
  storage?: StorageLike;
}

function defaultStorage(): StorageLike {
  return localStorage;
}

export function SavedPresetsPanel({
  progState,
  progBytes,
  sysState,
  sysBytes,
  onLoad,
  onImportClick,
  storage = defaultStorage(),
}: SavedPresetsPanelProps) {
  const [name, setName] = useState("");
  const [selectedId, setSelectedId] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [saved, setSaved] = useState<SavedUserPreset[]>(() =>
    listUserPresets(storage),
  );

  const refresh = useCallback(() => {
    setSaved(listUserPresets(storage));
  }, [storage]);

  const onSave = () => {
    if (!progBytes) return;
    try {
      const entry = saveUserPreset(
        storage,
        name || progState.programName,
        progState,
        progBytes,
        sysState,
        sysBytes ?? undefined,
      );
      setName("");
      setSelectedId(entry.id);
      refresh();
      setMessage(`Saved “${entry.name}”`);
    } catch (err) {
      setMessage(err instanceof Error ? err.message : String(err));
    }
  };

  const onLoadSelected = () => {
    const preset = saved.find((p) => p.id === selectedId);
    if (!preset) {
      setMessage("Select a saved preset");
      return;
    }
    onLoad(preset);
    setMessage(`Loaded “${preset.name}”`);
  };

  const onDelete = () => {
    if (!selectedId) return;
    const preset = saved.find((p) => p.id === selectedId);
    deleteUserPreset(storage, selectedId);
    setSelectedId("");
    refresh();
    setMessage(preset ? `Deleted “${preset.name}”` : "Deleted preset");
  };

  const onDownloadProg = () => {
    if (!progBytes) return;
    downloadSyx({
      bytes: progBytes,
      filename: suggestSyxFilename("prog", progState.programName),
    });
    setMessage("Downloaded program .syx");
  };

  const onDownloadSys = () => {
    if (!sysBytes) return;
    downloadSyx({
      bytes: sysBytes,
      filename: suggestSyxFilename("system"),
    });
    setMessage("Downloaded system .syx");
  };

  return (
    <div className="panel-raised flex h-full flex-col rounded-md px-4 py-5">
      <div className="label-caps mb-3 text-center">
        Saved presets
        <div className="panel-group-rule" aria-hidden />
      </div>
      <p className="text-xs text-center opacity-70 mb-4 max-w-md mx-auto">
        Store the current program (and system settings) in this browser via{" "}
        <code className="font-led">{LS_USER_PRESETS}</code>. Import or download
        .syx files to share or back up.
      </p>
      <div className="flex flex-wrap justify-center gap-2 items-end">
        <label className="flex flex-col gap-1 text-xs">
          <span className="label-caps">Name</span>
          <input
            type="text"
            className="rounded-lg border border-[oklch(0.28_0.012_252)] bg-[oklch(0.1_0.008_252)] px-2 py-1.5 min-w-[160px] font-led shadow-[inset_0_2px_5px_oklch(0_0_0/0.4)] focus:border-[color:var(--color-primary)]/45 focus:outline-none focus:ring-1 focus:ring-[color:var(--color-primary)]/25"
            placeholder={progState.programName}
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>
        <button type="button" className={savedBtn} onClick={onSave}>
          Save
        </button>
        <select
          className="rounded-lg border border-[oklch(0.28_0.012_252)] bg-[oklch(0.1_0.008_252)] px-2 py-1.5 text-xs min-w-[140px] font-led shadow-[inset_0_2px_5px_oklch(0_0_0/0.4)]"
          value={selectedId}
          onChange={(e) => setSelectedId(e.target.value)}
        >
          <option value="">Load saved…</option>
          {saved.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <button
          type="button"
          className={savedBtn}
          onClick={onLoadSelected}
          disabled={!selectedId}
        >
          Load
        </button>
        <button
          type="button"
          className={`${savedBtn} disabled:opacity-40`}
          onClick={onDelete}
          disabled={!selectedId}
        >
          Delete
        </button>
      </div>
      <div className="flex flex-wrap justify-center gap-2 mt-4">
        <button type="button" className={savedBtn} onClick={onDownloadProg}>
          Download prog .syx
        </button>
        <button type="button" className={savedBtn} onClick={onDownloadSys}>
          Download sys .syx
        </button>
        <button type="button" className={savedBtn} onClick={onImportClick}>
          Import .syx
        </button>
      </div>
      {message && (
        <div className="mt-3 text-center text-xs led-text opacity-90">{message}</div>
      )}
      {saved.length === 0 && (
        <div className="mt-2 text-center text-xs opacity-50">
          No saved presets yet
        </div>
      )}
    </div>
  );
}
