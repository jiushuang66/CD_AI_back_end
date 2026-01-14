import time


def submit_ai_review(paper_id: int, user_payload: dict):
    """Stub: simulate submitting to AI service and storing a result.

    In real app: generate temporary OSS URL, call external AI (via requests or SDK),
    parse JSON, persist to DB and insert virtual annotations.
    """
    # simulate work / timeout behavior
    time.sleep(0.5)
    # Return a fake report (in real usage, persist to DB)
    return {"paper_id": paper_id, "issues": []}
