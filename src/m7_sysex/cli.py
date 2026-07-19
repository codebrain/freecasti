"""CLI for analyzing Bricasti M7 SysEx parameter dump folders."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from .analyze import (
    analyze_parameter_folder,
    analyze_tree,
    clear_analysis_outputs,
    write_analysis,
)
from .byte_map import build_byte_map
from .cross import cross_analyze, write_cross_analysis
from .decode_preset import enrich_names_with_parameters
from .export import (
    clear_export_dir,
    export_sysex_format,
    export_system_format,
    prog_export_dir,
    remove_legacy_export_roots,
    resolve_export_dir,
)
from .markdown_links import MarkdownLinksError, check_markdown_links
from .paths import (
    prog_byte_map_path,
    prog_cross_analysis_path,
    prog_menus_root,
    prog_unseen_values_path,
    resolve_sysex_root,
    specification_root,
    system_byte_map_path,
)
from .names import analyze_names_folder, find_names_folder, format_bank_map_by_index, write_names_analysis
from .preset_inventory import (
    analyze_preset_inventory,
    inventory_summary_line,
    render_preset_inventory_markdown,
    write_preset_inventory,
)
from .preset_sheet import format_report, run_compare, write_sheet_markdown
from .system import (
    analyze_system_tree,
    build_system_byte_map,
    write_system_analysis,
    write_system_summary,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="m7-sysex",
        description=(
            "Diff Bricasti M7 program dumps and export reverse-engineering docs. "
            "Every run overwrites previous analysis.json / specification/ outputs."
        ),
    )
    sub = parser.add_subparsers(dest="command")

    analyze_p = sub.add_parser(
        "analyze",
        help="Diff dumps and overwrite analysis.json (default if no subcommand)",
    )
    _add_analyze_args(analyze_p)

    export_p = sub.add_parser(
        "export",
        help="Analyze all parameters, then overwrite specification/",
    )
    export_p.add_argument(
        "--sysex",
        type=Path,
        default=Path("sysex"),
        help="Parent folder of parameter dump folders (default: sysex)",
    )
    export_p.add_argument(
        "--out",
        type=Path,
        default=specification_root(),
        help="Specification docs folder (default: specification/)",
    )
    export_p.add_argument(
        "--no-write-json",
        action="store_true",
        help="Skip writing per-folder analysis.json files",
    )
    export_p.add_argument(
        "--no-web-ui",
        action="store_true",
        help="Skip syncing specification assets into web-ui/public/",
    )

    cross_p = sub.add_parser(
        "cross",
        help=(
            "Cross-series meta-analysis (stable bytes, secondary movers, "
            "conflicts, coverage, checksum search); refreshes docs folder"
        ),
    )
    cross_p.add_argument(
        "--sysex",
        type=Path,
        default=Path("sysex"),
        help="Parent folder of parameter dump folders (default: sysex)",
    )
    cross_p.add_argument(
        "--out",
        type=Path,
        default=specification_root(),
        help="Specification docs folder to refresh (default: specification/)",
    )
    cross_p.add_argument(
        "--no-docs",
        action="store_true",
        help="Only write sysex/cross_analysis.json; do not rewrite markdown",
    )

    sheet_p = sub.add_parser(
        "sheet",
        help=(
            "Compare decoded sysex/prog/presets/ dumps to Bricasti's published "
            "preset sheet (uses docs/reference/preset_sheet.json)"
        ),
    )
    sheet_p.add_argument(
        "--sysex",
        type=Path,
        default=Path("sysex"),
        help="Parent folder containing _presets/ (default: sysex)",
    )
    sheet_p.add_argument(
        "--sheet-json",
        type=Path,
        help="Parsed sheet JSON (default: docs/reference/preset_sheet.json)",
    )
    sheet_p.add_argument(
        "--pdf",
        type=Path,
        help="Local preset_sheet.pdf (only used with --refresh)",
    )
    sheet_p.add_argument(
        "--analysis",
        type=Path,
        help="Path to _presets/analysis.json (default: auto-detect)",
    )
    sheet_p.add_argument(
        "--refresh",
        action="store_true",
        help="Re-parse the PDF into docs/reference/preset_sheet.json (needs pymupdf)",
    )
    sheet_p.add_argument(
        "--force-download",
        action="store_true",
        help="With --refresh, re-download the PDF even if cached",
    )
    sheet_p.add_argument(
        "--json",
        action="store_true",
        help="Print the full comparison result as JSON",
    )
    sheet_p.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Include soft (table/rounding) diffs in the text report",
    )
    sheet_p.add_argument(
        "--out",
        type=Path,
        default=specification_root() / "prog" / "preset-sheet.md",
        help="Write errata markdown here (default: specification/prog/preset-sheet.md)",
    )
    sheet_p.add_argument(
        "--no-docs",
        action="store_true",
        help="Print report only; do not write preset-sheet.md",
    )

    decode_p = sub.add_parser(
        "decode",
        help="Decode one .syx dump (program or system) to JSON / summary",
    )
    decode_p.add_argument(
        "file",
        type=Path,
        help="A .syx file holding one or more M7 dumps",
    )
    decode_p.add_argument(
        "--json",
        action="store_true",
        help="Print full JSON to stdout instead of the summary",
    )
    decode_p.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Also write the decoded JSON document(s) to this path",
    )

    encode_p = sub.add_parser(
        "encode",
        help="Rebuild a .syx dump (checksum recomputed) from decoded JSON",
    )
    encode_p.add_argument(
        "file",
        type=Path,
        help="JSON document produced by `m7-sysex decode` (single message)",
    )
    encode_p.add_argument(
        "output",
        type=Path,
        help="Destination .syx path",
    )

    inventory_p = sub.add_parser(
        "inventory",
        help="Compare captured presets to V2 addendum factory lists",
    )
    inventory_p.add_argument(
        "--sysex",
        type=Path,
        default=Path("sysex"),
        help="Parent folder containing prog/presets/ (default: sysex)",
    )
    inventory_p.add_argument(
        "--markdown",
        action="store_true",
        help="Print full preset-inventory markdown to stdout",
    )
    inventory_p.add_argument(
        "--write",
        action="store_true",
        help="Write specification/prog/preset-inventory.md only",
    )
    inventory_p.add_argument(
        "--out",
        type=Path,
        default=specification_root(),
        help="Docs root when using --write (default: specification/)",
    )

    # Backward compatible: `m7-sysex sysex` still means analyze.
    if argv is None:
        argv = sys.argv[1:]

    if not argv or argv[0] not in {
        "analyze",
        "export",
        "cross",
        "sheet",
        "inventory",
        "decode",
        "encode",
        "-h",
        "--help",
    }:
        argv = ["analyze", *argv]

    args = parser.parse_args(argv)

    if args.command == "export":
        return _cmd_export(args)
    if args.command == "cross":
        return _cmd_cross(args)
    if args.command == "sheet":
        return _cmd_sheet(args)
    if args.command == "inventory":
        return _cmd_inventory(args)
    if args.command == "decode":
        return _cmd_decode(args)
    if args.command == "encode":
        return _cmd_encode(args)
    return _cmd_analyze(args)


def _cmd_sheet(args: argparse.Namespace) -> int:
    try:
        result = run_compare(
            sysex_root=Path(args.sysex),
            pdf_path=Path(args.pdf) if args.pdf else None,
            analysis_path=Path(args.analysis) if args.analysis else None,
            sheet_json=Path(args.sheet_json) if args.sheet_json else None,
            refresh=bool(args.refresh),
            force_download=bool(args.force_download),
        )
    except (FileNotFoundError, ValueError, ImportError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_report(result, verbose=bool(args.verbose)), end="")
        print(
            f"sheet: {result.get('sheet_json')} "
            f"(source={result.get('sheet_source')})"
        )
        if result.get("pdf_path"):
            print(f"pdf: {result.get('pdf_path')}")
        print(f"analysis: {result.get('analysis_path')}")

    if not args.no_docs:
        from datetime import date

        from .export import _page_nav

        out = Path(args.out)
        write_sheet_markdown(
            result,
            out,
            today=date.today().isoformat(),
            nav=_page_nav(depth=0, current="Preset sheet"),
        )
        print(f"overwrote {out}")
        return _finish_doc_generation(Path(args.sysex))
    return 0


def _add_analyze_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "path",
        nargs="?",
        default="sysex",
        help="Parameter folder, or parent folder containing parameter folders (default: sysex)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional explicit output JSON path (single-folder mode only)",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print JSON to stdout instead of/in addition to writing analysis.json",
    )
    parser.add_argument(
        "--no-write",
        action="store_true",
        help="Do not write analysis.json files",
    )


def _cmd_analyze(args: argparse.Namespace) -> int:
    path = Path(args.path)
    try:
        cleared = [] if args.no_write else _clear_before_run(path)
        results = _run_analysis(path)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for path_cleared in cleared:
        print(f"removed {path_cleared}")

    written: list[Path] = []
    for result in results:
        if not args.no_write:
            out = args.output if args.output and len(results) == 1 else None
            written.append(write_analysis(result, out))
        _print_summary(result)

    if args.stdout:
        payload = results[0] if len(results) == 1 else results
        print(json.dumps(payload, indent=2))

    if written:
        print()
        for path_written in written:
            print(f"overwrote {path_written}")

    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    sysex = Path(args.sysex)
    out = resolve_export_dir(Path(args.out))
    byte_map_path = prog_byte_map_path(sysex)
    cross_path = prog_cross_analysis_path(sysex)
    try:
        cleared = [] if args.no_write_json else clear_analysis_outputs(sysex)
        cleared.extend(remove_legacy_export_roots())
        cleared.extend(clear_export_dir(out))
        results = _run_analysis(sysex)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for path_cleared in cleared:
        print(f"removed {path_cleared}")

    written: list[Path] = []
    for result in results:
        if not args.no_write_json:
            written.append(write_analysis(result))
        _print_summary(result)

    system_results: list[dict] = []
    system_byte_map = None
    try:
        system_results = analyze_system_tree(sysex)
    except ValueError as exc:
        print(f"error: system analysis: {exc}", file=sys.stderr)
        return 1
    for result in system_results:
        if not args.no_write_json:
            written.append(write_system_analysis(result))
        print(
            f"[system] {result['parameter']}: "
            f"{result['dump_count']} dumps, "
            f"changing offsets {result['changing_offsets']}"
        )
    if system_results and not args.no_write_json:
        summary_path = write_system_summary(system_results, sysex)
        if summary_path is not None:
            written.append(summary_path)

    if system_results:
        try:
            system_byte_map = build_system_byte_map(
                system_results, sysex_root=sysex
            )
            if not args.no_write_json:
                sys_map_path = system_byte_map_path(sysex)
                if sys_map_path.exists():
                    sys_map_path.unlink()
                sys_map_path.write_text(
                    json.dumps(system_byte_map, indent=2) + "\n",
                    encoding="utf-8",
                )
                written.append(sys_map_path)
            counts = system_byte_map["counts"]
            print(
                f"[system byte map] known={counts['known_or_frame']} "
                f"secondary={counts['secondary']} "
                f"unknown={counts['unknown']}"
            )
        except ValueError as exc:
            print(f"warning: system byte map skipped: {exc}", file=sys.stderr)

    names = None
    names_folder = find_names_folder(sysex)
    if names_folder is not None:
        try:
            names = analyze_names_folder(names_folder)
            names = enrich_names_with_parameters(names, results)
            if not args.no_write_json:
                written.append(write_names_analysis(names))
            _print_names_summary(names)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    byte_map = None
    try:
        byte_map = build_byte_map(results, names=names)
        if not args.no_write_json:
            if byte_map_path.exists():
                byte_map_path.unlink()
            byte_map_path.write_text(
                json.dumps(byte_map, indent=2) + "\n", encoding="utf-8"
            )
            written.append(byte_map_path)
        counts = byte_map["counts"]
        print(
            f"[byte map] independent series merged by offset - "
            f"known={counts['known_or_frame']} "
            f"secondary={counts['secondary']} "
            f"unknown={counts['unknown']}"
        )
    except ValueError as exc:
        print(f"warning: byte map skipped: {exc}", file=sys.stderr)

    cross = None
    try:
        cross = cross_analyze(results, sysex)
        if not args.no_write_json:
            written.append(write_cross_analysis(cross, cross_path))
        _print_cross_summary(cross)
    except ValueError as exc:
        print(f"warning: cross analysis skipped: {exc}", file=sys.stderr)

    menus_analysis = None
    menus_root = prog_menus_root(sysex)
    if menus_root.is_dir() and any(menus_root.glob("*.syx")):
        try:
            from .prog.menus import analyze_menus_folder, write_menus_analysis

            menus_analysis = analyze_menus_folder(menus_root, sysex)
            if not args.no_write_json:
                written.extend(write_menus_analysis(menus_analysis, menus_root))
            print(
                f"[menus] {menus_analysis['capture_count']} UI captures, "
                f"idle={menus_analysis['idle_stem']!r}"
            )
        except ValueError as exc:
            print(f"warning: menu analysis skipped: {exc}", file=sys.stderr)

    if byte_map:
        try:
            from .prog.unseen_values import build_unseen_values

            unseen_values = build_unseen_values(
                results,
                byte_map,
                menus_analysis,
                sysex,
            )
            if not args.no_write_json:
                unseen_path = prog_unseen_values_path(sysex)
                if unseen_path.exists():
                    unseen_path.unlink()
                unseen_path.write_text(
                    json.dumps(unseen_values, indent=2) + "\n",
                    encoding="utf-8",
                )
                written.append(unseen_path)
            s = unseen_values.get("summary") or {}
            print(
                f"[unseen values] documented_unseen={s.get('total_documented_unseen_rows', 0)} "
                f"encoded_gaps={s.get('total_encoded_gaps', 0)} "
                f"offset_nibble_gaps={s.get('offsets_with_unseen_nibbles', 0)}"
            )
        except ValueError as exc:
            print(f"warning: unseen values skipped: {exc}", file=sys.stderr)

    sheet_compare = None
    if names is not None:
        try:
            sheet_compare = run_compare(sysex_root=sysex)
            print(
                f"[preset sheet] matched={sheet_compare['matched_count']}/"
                f"{sheet_compare['dump_count']} "
                f"hard={sheet_compare['hard_count']} "
                f"soft-only={sheet_compare['soft_only_count']} "
                f"missing={len(sheet_compare.get('missing_on_sheet') or [])}"
            )
        except (FileNotFoundError, ValueError, ImportError) as exc:
            print(f"warning: preset sheet compare skipped: {exc}", file=sys.stderr)

    doc = export_sysex_format(
        results,
        out,
        byte_map=byte_map,
        cross=cross,
        names=names,
        sheet_compare=sheet_compare,
        menus_analysis=menus_analysis,
    )
    system_doc = export_system_format(
        system_results, out, byte_map=system_byte_map
    )
    prog_out = prog_export_dir(out)

    if names is not None:
        repo_root = sysex.resolve().parent
        inventory, _inv_path = write_preset_inventory(
            names, prog_out, repo_root=repo_root
        )
        print(inventory_summary_line(inventory))

    print()
    for path_written in written:
        print(f"overwrote {path_written}")
    from .export.nav import PROG_BYTES_DIR, SYSTEM_BYTES_DIR

    print(f"overwrote {doc}")
    print(
        f"overwrote {prog_out / PROG_BYTES_DIR} "
        f"({len(results)} parameter pages)"
    )
    if (prog_out / "program-identity.md").is_file():
        print(f"overwrote {prog_out / 'program-identity.md'}")
    if (prog_out / "preset-sheet.md").is_file():
        print(f"overwrote {prog_out / 'preset-sheet.md'}")
    presets_root = prog_out / "presets"
    if presets_root.is_dir():
        bank_pages = list(presets_root.glob("*/README.md"))
        preset_pages = [
            p for p in presets_root.glob("*/*.md") if p.name != "README.md"
        ]
        print(
            f"overwrote {presets_root} "
            f"({len(bank_pages)} bank indexes, {len(preset_pages)} preset pages, presets.json)"
        )
    if (prog_out / "byte-map-overview.md").is_file():
        print(f"overwrote {prog_out / 'byte-map-overview.md'}")
    if (prog_out / "ui-state.md").is_file():
        print(f"overwrote {prog_out / 'ui-state.md'}")
    if (prog_out / "byte-map.md").is_file():
        print(f"overwrote {prog_out / 'byte-map.md'}")
    if (prog_out / "m7_program_dump.ksy").is_file():
        print(f"overwrote {prog_out / 'm7_program_dump.ksy'}")
    if (prog_out / "m7_program_dump.spec.json").is_file():
        print(f"overwrote {prog_out / 'm7_program_dump.spec.json'}")
    if (prog_out / "cross.md").is_file():
        print(f"overwrote {prog_out / 'cross.md'}")
    if (prog_out / "preset-inventory.md").is_file():
        print(f"overwrote {prog_out / 'preset-inventory.md'}")
    if system_doc is not None:
        print(f"overwrote {system_doc}")
        sys_params = out / "system" / SYSTEM_BYTES_DIR
        if sys_params.is_dir():
            print(
                f"overwrote {sys_params} "
                f"({len(list(sys_params.glob('*.md')))} system series pages)"
            )
        sys_byte_map = out / "system" / "byte-map.md"
        if sys_byte_map.is_file():
            print(f"overwrote {sys_byte_map}")
        sys_byte_overview = out / "system" / "byte-map-overview.md"
        if sys_byte_overview.is_file():
            print(f"overwrote {sys_byte_overview}")
        if (out / "system" / "m7_system_dump.ksy").is_file():
            print(f"overwrote {out / 'system' / 'm7_system_dump.ksy'}")
    if not args.no_web_ui:
        from .export.web_ui import sync_web_ui_assets

        repo_root = sysex.resolve().parent
        web_written = sync_web_ui_assets(repo_root)
        print(f"overwrote web-ui/public (runtime bundle, param manifest)")
        for path_written in web_written:
            if path_written.parent.name == "public" or "public" in path_written.parts:
                print(f"  {path_written.relative_to(repo_root)}")
    from .export.nav import write_export_index

    preset_count = len((names or {}).get("dumps") or [])
    write_export_index(
        out,
        today=date.today().isoformat(),
        prog_byte_map=byte_map,
        system_byte_map=system_byte_map,
        prog_parameter_count=len(results),
        system_parameter_count=len(system_results),
        preset_count=preset_count,
    )
    print(f"overwrote {out / 'README.md'}")
    print(f"overwrote {out / 'open-items.md'}")
    return _finish_doc_generation(sysex)


def _cmd_inventory(args: argparse.Namespace) -> int:
    sysex = Path(args.sysex)
    names_folder = find_names_folder(sysex)
    if names_folder is None:
        print("error: no prog/presets/ folder under sysex", file=sys.stderr)
        return 1
    try:
        names = analyze_names_folder(names_folder)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    inventory = analyze_preset_inventory(names)
    print(inventory_summary_line(inventory))

    if args.markdown:
        print()
        print(render_preset_inventory_markdown(inventory))

    if args.write:
        out = resolve_export_dir(Path(args.out))
        prog_out = prog_export_dir(out)
        _, path = write_preset_inventory(
            names, prog_out, repo_root=sysex.resolve().parent
        )
        print(f"overwrote {path}")
        return _finish_doc_generation(sysex)

    return 0


def _cmd_decode(args: argparse.Namespace) -> int:
    from .dump_codec import decode_dump
    from .frame import iter_sysex_messages

    path = Path(args.file)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1
    try:
        messages = list(iter_sysex_messages(path.read_bytes()))
        docs = [decode_dump(msg) for msg in messages]
    except (ValueError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not docs:
        print(f"error: no SysEx messages in {path}", file=sys.stderr)
        return 1

    payload: object = docs[0] if len(docs) == 1 else docs
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for i, doc in enumerate(docs):
            if len(docs) > 1:
                print(f"--- message {i + 1}/{len(docs)} ---")
            _print_decoded_dump(doc)

    if args.output:
        out = Path(args.output)
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out}")

    if not all(doc["checksum_ok"] for doc in docs):
        return 1
    return 0


def _print_decoded_dump(doc: dict) -> None:
    kind = doc["kind"]
    checksum = "OK" if doc["checksum_ok"] else "INVALID"
    print(f"[{kind}] {doc['format']} ({doc['message_length']} bytes)")
    if doc.get("program_name"):
        print(f"  name: {doc['program_name']}")
    print(f"  checksum: {checksum}")
    for field_id, entry in doc["fields"].items():
        if "text" in entry:
            continue  # name already shown
        if "encoded" in entry:
            display = entry.get("display")
            if display is None and entry.get("value") is not None:
                display = entry["value"]
            shown = display if display is not None else f"encoded {entry['encoded']}"
            print(f"  {entry['label']}: {shown}")
        elif entry.get("blob_kind") == "register_basis":
            reg = entry["register"]
            print(
                f"  {entry['label']}: register basis "
                f"(name {reg['name']!r}, store counter {reg['values']['store_counter']})"
            )


def _cmd_encode(args: argparse.Namespace) -> int:
    from .dump_codec import encode_dump

    path = Path(args.file)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(doc, list):
            raise ValueError(
                "encode expects a single decoded document, not a list"
            )
        raw = encode_dump(doc)
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    out = Path(args.output)
    out.write_bytes(raw)
    print(f"wrote {out} ({len(raw)} bytes)")
    return 0


def _cmd_cross(args: argparse.Namespace) -> int:
    """Re-analyze tree (or load fresh), write cross_analysis.json, refresh docs."""
    sysex = Path(args.sysex)
    out = resolve_export_dir(Path(args.out))
    cross_path = prog_cross_analysis_path(sysex)
    try:
        results = _run_analysis(sysex)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        cross = cross_analyze(results, sysex)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    written = write_cross_analysis(cross, cross_path)
    _print_cross_summary(cross)
    print(f"overwrote {written}")

    if not args.no_docs:
        names = None
        names_folder = find_names_folder(sysex)
        if names_folder is not None:
            try:
                names = analyze_names_folder(names_folder)
                names = enrich_names_with_parameters(names, results)
            except ValueError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 1
        byte_map = None
        try:
            byte_map = build_byte_map(results, names=names)
        except ValueError:
            pass
        clear_export_dir(out)
        sheet_compare = None
        if names is not None:
            try:
                sheet_compare = run_compare(sysex_root=sysex)
            except (FileNotFoundError, ValueError, ImportError):
                pass
        doc = export_sysex_format(
            results,
            out,
            byte_map=byte_map,
            cross=cross,
            names=names,
            sheet_compare=sheet_compare,
        )
        print(f"overwrote {doc}")
        print(
            f"overwrote {prog_export_dir(out) / 'bytes'} "
            f"({len(results)} field pages)"
        )
        return _finish_doc_generation(sysex)

    return 0


def _repo_root_from_sysex(sysex: Path) -> Path:
    return resolve_sysex_root(sysex).parent


def _finish_doc_generation(sysex: Path) -> int:
    """Verify relative links after writing specification markdown."""
    try:
        file_count = check_markdown_links(_repo_root_from_sysex(sysex))
    except MarkdownLinksError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"markdown links ok ({file_count} files)")
    return 0


def _clear_before_run(path: Path) -> list[Path]:
    """Remove prior analysis.json for the target folder or tree."""
    path = path.resolve()
    syx_here = list(path.glob("*.syx")) + list(path.glob("*.SYX"))
    if syx_here:
        analysis = path / "analysis.json"
        if analysis.is_file():
            analysis.unlink()
            return [analysis]
        return []
    return clear_analysis_outputs(path)


def _run_analysis(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"path not found: {path}")
    if path.is_file():
        raise ValueError("expected a folder of .syx dumps, not a file")

    syx_here = list(path.glob("*.syx")) + list(path.glob("*.SYX"))
    if syx_here:
        return [analyze_parameter_folder(path)]

    results = analyze_tree(path)
    if not results:
        raise ValueError(f"no parameter folders with .syx files under {path}")
    return results


def _print_summary(result: dict) -> None:
    hyp = result.get("hypothesis", {})
    best = result.get("best_encoding")
    value_range = result.get("value_range")
    print(f"[{result['parameter']}] {result['dump_count']} dumps, "
          f"{result['message_length']} bytes each")
    print(f"  changing offsets: {result['changing_offsets']}")
    if best:
        print(
            f"  best encoding: {best['encoding']} @ {best['offsets']} "
            f"(score {best['score']:.0%} - {best.get('notes')})"
        )
    if value_range and value_range.get("summary"):
        print(f"  range: {value_range['summary']}")
    official = result.get("official") or {}
    if official.get("matched"):
        exp = official.get("expected") or {}
        print(
            f"  catalog hint: {official.get('name')} "
            f"{exp.get('manual_min')}...{exp.get('manual_max')}"
            f"{(' ' + exp['unit']) if exp.get('unit') else ''} "
            f"[{official.get('agreement')}]"
        )
        for note in official.get("notes_from_check") or []:
            print(f"  catalog note: {note}")
        for warn in official.get("warnings") or []:
            print(f"  catalog warning: {warn}")
    elif official.get("warning"):
        print(f"  catalog: {official['warning']}")
    print(f"  confidence: {hyp.get('confidence')} - {hyp.get('summary')}")


def _print_names_summary(result: dict) -> None:
    hyp = result.get("hypothesis") or {}
    bank = (result.get("fields") or {}).get("bank_index") or {}
    bank_map = bank.get("map") or {}
    name = (result.get("fields") or {}).get("program_name") or {}
    print(
        f"[_presets] {result['dump_count']} preset dumps - "
        f"confidence={hyp.get('confidence')} "
        f"banks={{{format_bank_map_by_index(bank_map)}}} "
        f"name_bytes={name.get('bytes_match_count', '?')}/{result['dump_count']}"
    )
    print(f"  {hyp.get('summary')}")
    for mm in result.get("name_mismatches") or []:
        detail = mm.get("mismatch") or {}
        print(
            f"  NAME MISMATCH {mm.get('file')}: "
            f"filename preset={mm.get('preset')!r} "
            f"field={mm.get('name_field')!r} "
            f"offset={detail.get('offset')}"
        )


def _print_cross_summary(cross: dict) -> None:
    print(
        f"[cross] {cross['message_count']} messages / {cross['series_count']} series - "
        f"stable_payload={len(cross['stable_payload_offsets'])} "
        f"recurrent_secondary={len(cross['recurrent_secondary'])} "
        f"conflicts={len(cross['primary_conflicts'])} "
        f"coverage_gaps={len(cross['coverage_gaps'])} "
        f"checksum_matches={len((cross.get('checksum') or {}).get('matches') or [])}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
