"""Explicitly authorized, metered practice campaign; not a provider-side cost cap."""
import math

from builder.core import ContractError


def balance_usd(snapshot):
    values = [snapshot.get(k) for k in ("creditsLeft", "creditUsdRate")]
    if any(not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) or v < 0 for v in values):
        raise ContractError("Invalid credit balance")
    return round(values[0] * values[1], 6)


def check_campaign(policy, snapshot, case_count):
    if policy.get("monitored_campaign_authorized") is not True:
        raise ContractError("Monitored campaign requires explicit user authorization")
    cap = policy.get("total_authorized_usd")
    if not isinstance(cap, (int, float)) or isinstance(cap, bool) or not math.isfinite(cap) or not 0 < cap <= 100:
        raise ContractError("Campaign authorization must be within 100 USD")
    floor = policy.get("campaign_stop_balance_usd")
    if not isinstance(floor, (int, float)) or isinstance(floor, bool) or not math.isfinite(floor) or not 20 <= floor < cap:
        raise ContractError("Campaign must preserve at least 20 USD of credit as a billing buffer")
    if not 1 <= case_count <= 7:
        raise ContractError("At most seven practice cases may run in one simulation")
    balance = balance_usd(snapshot)
    used = snapshot.get("totalCreditsUsed")
    if used is not None:
        if not isinstance(used, (int, float)) or isinstance(used, bool) or not math.isfinite(used) or used < 0:
            raise ContractError("Invalid cumulative workspace usage")
        if used * snapshot["creditUsdRate"] >= cap - floor:
            raise ContractError("Authorized consumption buffer reached; added credit does not increase permission")
    if balance <= floor or (balance > 100 and used is None):
        raise ContractError("Credit buffer reached or balance changed unexpectedly; reconcile before continuing")
    return balance


def observed_spend(state, snapshot):
    balance = balance_usd(snapshot)
    used = snapshot.get("totalCreditsUsed")
    if used is not None:
        if not isinstance(used, (int, float)) or isinstance(used, bool) or not math.isfinite(used) or used < 0:
            raise ContractError("Invalid cumulative workspace usage")
        if used < state.get("last_total_credits_used", 0):
            raise ContractError("Usage counter decreased; reconcile before continuing")
    return max(state.get("observed_workspace_spend_usd", 0), 100 - balance,
               used * snapshot["creditUsdRate"] if used is not None else 0)


def reserve_campaign(policy, state, snapshot, case_count, repetitions, run_id):
    balance = check_campaign(policy, snapshot, case_count)
    spend = observed_spend(state, snapshot)
    if spend >= policy["total_authorized_usd"] - policy["campaign_stop_balance_usd"]:
        raise ContractError("Recorded consumption reached the authorized buffer")
    if state.get("monitored_pending_run") or state.get("reserved_usd", 0):
        raise ContractError("An earlier reservation is unresolved")
    if repetitions not in (1, 3): raise ContractError("Unsupported repetition count")
    for key, amount in (("case_runs", case_count * repetitions), ("simulations", repetitions)):
        if state.get(key, 0) + amount > policy["max_" + key]:
            raise ContractError("Campaign test quota reached")
    return {**state, "monitored_pending_run": run_id,
            "case_runs": state.get("case_runs", 0) + case_count * repetitions,
            "simulations": state.get("simulations", 0) + repetitions,
            "observed_workspace_spend_usd": spend,
            "last_total_credits_used": snapshot.get("totalCreditsUsed", state.get("last_total_credits_used", 0))}


def settle_campaign(state, snapshot, run_id):
    if state.get("monitored_pending_run") != run_id:
        raise ContractError("Cannot reconcile a different campaign run")
    balance = balance_usd(snapshot)
    return {**state, "monitored_pending_run": None,
            "observed_workspace_spend_usd": observed_spend(state, snapshot),
            "last_total_credits_used": snapshot.get("totalCreditsUsed", state.get("last_total_credits_used", 0)),
            "last_completed_run": run_id, "last_balance_usd": balance}
