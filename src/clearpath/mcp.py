from __future__ import annotations

import json
import sys

from .contribution import allocate_contribution_budget
from .interop import mcp_tools
from .market import market_metrics
from .models import OpportunitySpec, PersonProfile
from .portfolio import analyze_portfolio
from .viability import analyze_opportunity


def _reply(request_id, result=None, error=None):
    message = {"jsonrpc": "2.0", "id": request_id}
    if error is not None:
        message["error"] = {"code": -32000, "message": str(error)}
    else:
        message["result"] = result
    print(json.dumps(message, ensure_ascii=False), flush=True)


def serve() -> int:
    for raw in sys.stdin:
        try:
            request = json.loads(raw)
            method = request.get("method")
            rid = request.get("id")
            if method == "initialize":
                _reply(rid, {"protocolVersion": "2026-07-28", "serverInfo": {"name": "clearpath", "version": "1.0.0"}, "capabilities": {"tools": {}}})
            elif method == "tools/list":
                _reply(rid, {"tools": mcp_tools()})
            elif method == "tools/call":
                params = request.get("params", {})
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "clearpath_analyze_opportunity":
                    value = analyze_opportunity(PersonProfile.from_dict(args["person"]), OpportunitySpec.from_dict(args["opportunity"]))
                elif name == "clearpath_analyze_portfolio":
                    value = analyze_portfolio(PersonProfile.from_dict(args["person"]), [OpportunitySpec.from_dict(item) for item in args["opportunities"]])
                elif name == "clearpath_audit_training_offer":
                    value = market_metrics(OpportunitySpec.from_dict(args["opportunity"]))
                elif name == "clearpath_allocate_contribution":
                    value = allocate_contribution_budget(float(args["budget"]), list(args["contributions"]))
                else:
                    raise ValueError("unknown tool")
                _reply(rid, {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False, sort_keys=True)}], "isError": False})
            else:
                _reply(rid, error="unsupported method")
        except Exception as exc:
            _reply(None, error=exc)
    return 0
