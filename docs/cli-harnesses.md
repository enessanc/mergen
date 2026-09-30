# CLI agent harness contract

Mergen invokes an agent harness as a process inside the disposable workspace;
it does not call a model-provider API. Built-in adapter names are `codex`,
`claude-code`, and `aider`; any executable may be supplied through the project
contract when its argument list is explicit.

Harness processes receive a task instruction and workspace only. The Core never
passes Kubernetes credentials, Docker sockets, host mounts, Plane credentials,
or broad provider tokens. Validation commands are argv lists, never shell text.

The harness may change only its `agent/<work-item>-<slug>` task branch. Required
validation runs after harness exit; only a passing result may be committed and
pushed for human review.
