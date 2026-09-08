from __future__ import annotations


def mcp_tools() -> list[dict]:
    return [
        {"name": "clearpath_analyze_opportunity", "description": "Evaluate a person-opportunity fit without creating a person-level worth score.", "inputSchema": {"type": "object", "required": ["person", "opportunity"], "properties": {"person": {"type": "object"}, "opportunity": {"type": "object"}}}},
        {"name": "clearpath_analyze_portfolio", "description": "Compare multiple opportunity routes and return a route-set decision without scoring human worth.", "inputSchema": {"type": "object", "required": ["person", "opportunities"], "properties": {"person": {"type": "object"}, "opportunities": {"type": "array"}}}},
        {"name": "clearpath_audit_training_offer", "description": "Compare marketed training seats with declared funded paid opportunities.", "inputSchema": {"type": "object", "required": ["opportunity"], "properties": {"opportunity": {"type": "object"}}}},
        {"name": "clearpath_allocate_contribution", "description": "Create a transparent no-payment contribution allocation proposal.", "inputSchema": {"type": "object", "required": ["budget", "contributions"], "properties": {"budget": {"type": "number"}, "contributions": {"type": "array"}}}},
    ]


def a2a_agent_card() -> dict:
    return {
        "name": "DIKWP ClearPath Transparent Economy Agent",
        "description": "Produces bounded opportunity truth reports, saturation audits, and contribution proposals.",
        "version": "1.0.0",
        "capabilities": {"streaming": False, "pushNotifications": False},
        "skills": [
            {"id": "opportunity-truth", "name": "Opportunity Truth", "description": "Find a testable route or declare no current viable route."},
            {"id": "training-integrity", "name": "Training Integrity", "description": "Expose late-entry and opportunity-laundering risk."},
        ],
        "external_action_authority": 0,
    }


def openapi_spec() -> dict:
    return {
        "openapi": "3.1.0",
        "info": {"title": "DIKWP ClearPath Local API", "version": "1.0.0"},
        "paths": {
            "/health": {"get": {"responses": {"200": {"description": "healthy"}}}},
            "/analyze": {"post": {"responses": {"200": {"description": "opportunity analysis"}, "400": {"description": "invalid request"}}}},
            "/portfolio": {"post": {"responses": {"200": {"description": "opportunity portfolio analysis"}, "400": {"description": "invalid request"}}}},
        },
    }
