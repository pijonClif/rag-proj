# hitl.py
# This file handles Human-in-the-Loop escalation
# When the bot cannot answer confidently, this module
# logs the query and notifies a human agent

import json
import os
from datetime import datetime

# File where escalated queries are saved
ESCALATION_LOG = "./data/escalation_log.json"

def escalate_to_human(query: str, reason: str) -> str:
    """
    Escalates a query to a human agent.
    Logs the query and returns a user-facing message.
    """

    # Step 1: Create escalation record
    escalation_record = {
        "id": _get_next_id(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "reason": reason,
        "status": "pending",
        "handled_by": None,
        "resolution": None
    }

    # Step 2: Save to log file
    _save_escalation(escalation_record)

    # Step 3: Simulate notifying human agent
    print("\n[HITL MODULE] Query escalated to human agent.")
    print(f"[HITL MODULE] Reason: {reason}")
    print(f"[HITL MODULE] Escalation ID: {escalation_record['id']}")
    print(f"[HITL MODULE] Logged at: {escalation_record['timestamp']}")

    # Step 4: Return message to user
    user_message = (
        f"\nI'm sorry, I was unable to find a confident answer "
        f"to your question.\n"
        f"Your query has been escalated to a human support agent.\n"
        f"Escalation ID: {escalation_record['id']}\n"
        f"Our team will get back to you within 24 hours."
    )

    return user_message


def resolve_escalation(escalation_id: int, resolution: str):
    """
    Simulates a human agent resolving an escalated query.
    """
    log = _load_log()

    for record in log:
        if record["id"] == escalation_id:
            record["status"] = "resolved"
            record["handled_by"] = "Human Agent"
            record["resolution"] = resolution
            break

    _write_log(log)
    print(f"\n[HITL MODULE] Escalation {escalation_id} resolved.")


def view_pending_escalations():
    """
    Shows all pending escalations waiting for human review.
    """
    log = _load_log()
    pending = [r for r in log if r["status"] == "pending"]

    if not pending:
        print("\n[HITL MODULE] No pending escalations.")
        return

    print(f"\n[HITL MODULE] {len(pending)} pending escalation(s):")
    for record in pending:
        print(f"\n  ID       : {record['id']}")
        print(f"  Time     : {record['timestamp']}")
        print(f"  Query    : {record['query']}")
        print(f"  Reason   : {record['reason']}")
        print(f"  Status   : {record['status']}")


# ── Helper functions ──────────────────────────────────────

def _load_log():
    if not os.path.exists(ESCALATION_LOG):
        return []
    with open(ESCALATION_LOG, "r") as f:
        return json.load(f)


def _write_log(log):
    with open(ESCALATION_LOG, "w") as f:
        json.dump(log, f, indent=2)


def _save_escalation(record):
    log = _load_log()
    log.append(record)
    _write_log(log)


def _get_next_id():
    log = _load_log()
    if not log:
        return 1
    return max(r["id"] for r in log) + 1