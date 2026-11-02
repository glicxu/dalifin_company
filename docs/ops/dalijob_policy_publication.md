# Dali Job privacy publication — November 2, 2026

Adds `/privacy/dalijob` with `/privacy/dali-job` as an alias and a link on `/privacy`. Based on the currently deployed website commit 6ccc2a4; preserves the other app policies.

Content evidence: DaliJob README, docs/DATA_LIFECYCLE.md, account_deletion.py, guest_trials service and purge implementation, resume-import privacy tests, and report schemas. The policy distinguishes soft deletion from physical erasure, retained match snapshots from their source records, and guest access expiry from cleanup. Proposed 30/90-day retention targets are not represented as implemented guarantees. AI-provider retention is not asserted to be zero.

Validation: 44 website tests passed; compileall passed; direct TestClient checks verified the index link, both routes, GET/HEAD, effective date, contact and deletion disclosures.

Publication uses an isolated Git worktree and the canonical us3 deploy driver scoped to this website. The driver's broad host trading tests are replaced with read-only website/API integration verification, following the existing Bible policy rollout precedent. Shared cron and unrelated processes remain running. The repo has no pre/post hook scripts: check_and_deploy.sh runs pytest before installation and scripts/verify_deploy.py provides post-restart integration checks. Previous binary/config/metadata are retained in a restricted rollback snapshot.
