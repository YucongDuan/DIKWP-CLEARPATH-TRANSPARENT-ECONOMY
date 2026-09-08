.PHONY: test demo model-check audit

test:
	PYTHONPATH=src python -m pytest -q

demo:
	PYTHONPATH=src python -m clearpath demo --workspace .clearpath-demo --reset

model-check:
	PYTHONPATH=src python scripts/bounded_model_check.py --output validation/TOEP_1000_BOUNDED_MODEL_CHECK_RECEIPT.json

audit:
	python scripts/static_audit.py --root src/clearpath --output validation/STATIC_AUDIT_RECEIPT.json
