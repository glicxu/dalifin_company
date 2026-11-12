# Restore published policies after Camera deployment

Google Play rejected Dali Bible build 607020811 on November 12 because privacy
and account/data deletion URLs returned 404. Camera branch `1434d7e` was based
on `e4496af` and omitted the already published Bible, Job, and Chatty commits.
Runtime configuration still advertised `fb132ab`, masking the source regression.

Combined source commit `dc47560320b129532953dd254c831d7fd07bf79d` merges Camera
`1434d7e` into published combined site `fb132ab`. All 46 tests and compileall
passed. Existing preservation tests include Bible, Job, Chatty, and other app
policy routes. Future website releases must descend from this combined history
and check the full policy inventory, rather than deploy an older app-specific
branch. The main shared working tree contains unrelated local changes and was
left intact.

Imported the Git bundle into us3 and built the isolated Git worktree using
`/data/dali/deployment/deploy_driver.sh`, scoped to
`dalifin_company_bible_restore_20261112`. A private rollback snapshot of binary,
metadata, configuration and existing policy pages is retained at
`/data/dali/prod/backup/company-policy-20261112`. The generic host trading/AI
suite was outside this task; the established bounded website/API integration
checks substituted for that suite. No unrelated processes or cron were stopped.

Packaged staging on 5103, production loopback on 5003, and public smoke passed.
The runtime build ID now matches the combined source. Public GET/HEAD passed
for Bible privacy, terms, deletion, Chatty privacy, and Job privacy. Nine
existing application privacy pages retained identical normalized HTML. Privacy
index discovery and public deletion contact were verified in browser. Downloads,
API dependency and support config checks passed. Staging was stopped afterward.

Dali Bible production release 5 / build 607020811 was resubmitted without a
rebuild. Play Console confirmed Changes in review / Start full rollout at
approximately 2:28 PM Pacific. Approval remains pending.
