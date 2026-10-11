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

20:54 remote verification: 617/617 exact HTTP/body comparisons passed through
the real public HTTPS Worker. Local system DNS returned 188.114.96.3/97.3, whose
TCP connection timed out; Cloudflare's 1.1.1.1 resolver returned 104.21.80.118 and
172.67.180.132. The diagnostic verifier used 104.21.80.118 while retaining the
original hostname, SNI and normal certificate validation. No machine DNS setting
or TLS protection was changed. Freya-side reachability still needs a live call.
Two sweeps that stalled on local network routing were stopped, not counted as
passes. Exact successful checks: reports/final-mock-contract.json.

20:55 first generation failed because the nested Codex session could not execute
even read-only file commands. No workflow or API mutation was produced. Its full
trace is preserved in runs/20261011T175422Z-4d4ce55d. The generic adapter now embeds
all business source text and PDF images in the model input and saves the model's
JSON reply itself. Large non-schema JSON datasets are represented by shape only;
actual fixture values remain in the mock and tests. This keeps task-specific facts
out of builder code and avoids requiring model filesystem access.

20:56 clean source checkpoint: 948da58. A second recorded production generation
has started; neither its output nor its success is yet assumed.
