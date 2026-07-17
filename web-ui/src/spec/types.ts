export interface ValueMapEntry {
  encoded: number;
  name?: string;
  label: string;
}

export interface ValueMap {
  enum_id?: string;
  entries: ValueMapEntry[];
}

export interface SpecField {
  id: string;
  label: string;
  parameter?: string;
  offsets: number[];
  start: number;
  end: number;
  encoding?: string | null;
  kind?: string;
  size?: number;
  value_map?: ValueMap;
  contents?: number[];
}

export interface DumpSpec {
  format: string;
  version: number;
  message_length: number;
  fields: SpecField[];
}
