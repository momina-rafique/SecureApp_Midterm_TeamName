import json, logging, sys
logger = logging.getLogger("audit")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler); logger.setLevel(logging.INFO)

def audit(event: str, **fields):
    safe = {k: v for k, v in fields.items() if k not in {"password","token"}}
    logger.info(json.dumps({"event": event, **safe}))
