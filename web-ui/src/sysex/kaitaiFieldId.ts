/** Map ``.spec.json`` snake_case field ids to Kaitai JavaScript property names. */
export function specIdToParserKey(id: string): string {
  const parts = id.split("_");
  if (parts.length === 1) return id;
  return (
    parts[0] +
    parts
      .slice(1)
      .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
      .join("")
  );
}
