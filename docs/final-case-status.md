# Final case implementation status

The final case supersedes the practice task and the old two-workflow submission
template. Authoritative evidence: organizer e-mail dated 2026-10-11 20:07 Istanbul,
BRIEF.md from the case folder, and the event Submit/Rules sections read live.
Deadline: 23:00 Istanbul. Planned artifact freeze: 22:40.

The user requested one operator for code, Worker deployment, generation and Freya
tests. Team member e-mails: mmansuroglu24@ku.edu.tr and mbirlik24@ku.edu.tr.
Submission e-mail requires a separate final user approval.

At 20:20 the Drive folder contained BRIEF.md and a call-flow PDF only. The
integration section 6, test customers, updated analyses and example conversations
were not yet available. No service endpoint or customer fixture has been inferred.
The diagram and brief contain potential discrepancies about extra authentication
and currency coverage; these remain evidence questions until the full pack arrives.

Folder generation uses a recorded Codex run against a frozen input manifest and
the unmodified official platform references. Source code does not contain the
final case's business rules. It requires a fresh successful remote mock contract
report and refuses missing evidence or unresolved conflicts before publishing.

The previous A/B practice runner remains available. Its pass rates do not measure
the final task. New folder unit tests use an unrelated library API to check that
the adapter does not depend on practice bank tool names or hostnames.

20:42 update: the full folder is now available and preserved under cases/final.
The October 9 recap explicitly amends the October 8 analysis. Extra identity
verification is explicitly rejected by the bank; missing GBP is omitted rather
than treated as zero. Outstanding capability gaps (yearly-change eligibility
flag, routing implementation and masked-number distinction) must be recorded by
the generation rather than filled with invented APIs.

Worker deployed at https://freya-final-bank.freya-final-bank-mock.workers.dev,
version 2a2d8bb2-f3a2-4509-9f05-9dce354f83e0. Local: 617 fixture responses
passed; Python: 127 tests. First remote sweep: 464 passed, 153 connection errors
during initial reachability; preserved under runs/final-live/mock-first-remote.json.
A full second sweep is running; generation remains gated on its result.
Freya preflight: zero active simulations, 481.5331 credits at 0.5 USD/credit.
This is available trial balance, not a per-call tariff or measured final cost.
