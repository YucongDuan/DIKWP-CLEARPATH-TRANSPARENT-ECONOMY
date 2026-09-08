from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from . import __version__
from .api import serve
from .contribution import allocate_contribution_budget
from .demo import run_demo
from .interop import a2a_agent_card, mcp_tools, openapi_spec
from .ledger import append_event, verify_ledger
from .market import market_metrics
from .mcp import serve as serve_mcp
from .models import OpportunitySpec, PersonProfile
from .privacy import public_capability_card
from .portfolio import analyze_portfolio
from .report import render_markdown
from .util import ClearPathError, read_json, write_json
from .viability import analyze_opportunity


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clearpath", description="Find an evidence-bounded economic route or declare no current viable route.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("analyze")
    p.add_argument("person")
    p.add_argument("opportunity")
    p.add_argument("--output-dir", default=".clearpath-analysis")
    p.add_argument("--reset", action="store_true")

    p = sub.add_parser("portfolio")
    p.add_argument("person")
    p.add_argument("opportunities", nargs="+")
    p.add_argument("--output")

    p = sub.add_parser("audit-training")
    p.add_argument("opportunity")
    p.add_argument("--output")

    p = sub.add_parser("contribution-proposal")
    p.add_argument("input")
    p.add_argument("--output")

    p = sub.add_parser("public-card")
    p.add_argument("person")
    p.add_argument("--output")

    p = sub.add_parser("demo")
    p.add_argument("--workspace", default=".clearpath-demo")
    p.add_argument("--reset", action="store_true")

    p = sub.add_parser("verify-ledger")
    p.add_argument("path")

    p = sub.add_parser("serve")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--allow-nonloopback", action="store_true")

    sub.add_parser("mcp")

    p = sub.add_parser("interop")
    p.add_argument("kind", choices=["mcp", "a2a", "openapi"])
    p.add_argument("--output")
    return parser


def _emit(value, output=None):
    if output:
        write_json(Path(output), value)
    else:
        print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def run(args: argparse.Namespace) -> int:
    if args.command == "analyze":
        output = Path(args.output_dir).resolve()
        if args.reset and output.exists():
            shutil.rmtree(output)
        output.mkdir(parents=True, exist_ok=True)
        person = PersonProfile.from_dict(read_json(Path(args.person)))
        opportunity = OpportunitySpec.from_dict(read_json(Path(args.opportunity)))
        analysis = analyze_opportunity(person, opportunity)
        write_json(output / "analysis.json", analysis)
        write_json(output / "public-capability-card.json", public_capability_card(person))
        (output / "report.md").write_text(render_markdown(person.to_dict(), opportunity.to_dict(), analysis), encoding="utf-8")
        append_event(output / "responsibility-ledger.jsonl", "OPPORTUNITY_ANALYSIS", {"decision_status": analysis["decision_status"], "person_digest": person.digest, "opportunity_digest": opportunity.digest})
        _emit({"decision_status": analysis["decision_status"], "output_dir": str(output), "base_viability": analysis["base_viability"], "robust_floor": analysis["robust_floor"]})
        return 0
    if args.command == "portfolio":
        person = PersonProfile.from_dict(read_json(Path(args.person)))
        opportunities = [OpportunitySpec.from_dict(read_json(Path(path))) for path in args.opportunities]
        _emit(analyze_portfolio(person, opportunities), args.output)
        return 0
    if args.command == "audit-training":
        _emit(market_metrics(OpportunitySpec.from_dict(read_json(Path(args.opportunity)))), args.output)
        return 0
    if args.command == "contribution-proposal":
        data = read_json(Path(args.input))
        _emit(allocate_contribution_budget(data["budget"], data["contributions"], data.get("platform_rate", 0.08), data.get("commons_rate", 0.03), data.get("correction_reserve_rate", 0.03)), args.output)
        return 0
    if args.command == "public-card":
        _emit(public_capability_card(PersonProfile.from_dict(read_json(Path(args.person)))), args.output)
        return 0
    if args.command == "demo":
        _emit(run_demo(Path(args.workspace).resolve(), args.reset))
        return 0
    if args.command == "verify-ledger":
        result = verify_ledger(Path(args.path))
        _emit(result)
        return 0 if result["valid"] else 1
    if args.command == "serve":
        return serve(args.host, args.port, args.allow_nonloopback)
    if args.command == "mcp":
        return serve_mcp()
    if args.command == "interop":
        value = {"mcp": {"protocolVersion": "2026-07-28", "tools": mcp_tools()}, "a2a": a2a_agent_card(), "openapi": openapi_spec()}[args.kind]
        _emit(value, args.output)
        return 0
    raise ClearPathError("Unsupported command")


def main(argv: list[str] | None = None) -> int:
    try:
        return run(build_parser().parse_args(argv))
    except (ClearPathError, ValueError, KeyError) as exc:
        print(f"clearpath: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
