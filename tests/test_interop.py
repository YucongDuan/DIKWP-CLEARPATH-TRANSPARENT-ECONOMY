from clearpath.interop import a2a_agent_card, mcp_tools, openapi_spec


def test_mcp_has_four_tools():
    assert len(mcp_tools()) == 4


def test_a2a_has_zero_external_authority():
    assert a2a_agent_card()["external_action_authority"] == 0


def test_openapi_has_analyze():
    assert "/analyze" in openapi_spec()["paths"]
