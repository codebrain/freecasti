/** Frame chrome for a selectable parameter control (dial or button list). */
export function controlSelectFrameClass(disabled = false): string {
  const base = "rounded-lg outline-none transition-opacity";
  return disabled
    ? `${base} cursor-not-allowed opacity-45`
    : `${base} cursor-pointer`;
}
