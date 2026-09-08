from clearpath.cli import main
from clearpath.demo import run_demo


def test_demo_creates_three_results(tmp_path):
    result = run_demo(tmp_path / "demo", reset=True)
    assert len(result["results"]) == 3
    assert result["ledger"]["valid"] is True


def test_cli_demo(tmp_path):
    code = main(["demo", "--workspace", str(tmp_path / "cli"), "--reset"])
    assert code == 0


def test_cli_analyze(tmp_path):
    from clearpath.demo import demo_opportunities, demo_person
    from clearpath.util import write_json
    person = tmp_path / "person.json"
    opp = tmp_path / "opp.json"
    write_json(person, demo_person())
    write_json(opp, demo_opportunities()[1])
    output = tmp_path / "out"
    assert main(["analyze", str(person), str(opp), "--output-dir", str(output), "--reset"]) == 0
    assert (output / "analysis.json").exists()
    assert (output / "report.md").exists()
