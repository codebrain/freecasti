import manifest from "@/generated/param-manifest.json";

interface ManifestEntry {
  id: string;
  description?: string;
}

function buildDescriptionMap(entries: ManifestEntry[]): Map<string, string> {
  const map = new Map<string, string>();
  for (const entry of entries) {
    if (entry.description) {
      map.set(entry.id, entry.description);
    }
  }
  return map;
}

export const progDescriptions = buildDescriptionMap(manifest.prog);
export const systemDescriptions = buildDescriptionMap(manifest.system);
