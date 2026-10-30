# DaliBible policy publication, 2026-10-30

Public routes: `/privacy/dalibible`, `/terms/dalibible`, and `/account-deletion/dalibible`. The privacy index links the Bible page. These pages use the existing company templates and support address; the deletion page collects no credentials and requires no app installation or login. It describes manual support follow-up without claiming that the currently blocked shared-account cleanup is complete.

Source is isolated in branch `codex/dalibible-policy-20261030`, based on the running website commit `4f475e91a5a99f2588185e126d20719c412c2390`. Unrelated local policy changes were not included. A Git bundle is fetched into the existing us3 repository and built from its dedicated Git worktree, preserving a verifiable source commit and the unchanged main checkout.

Pre-deploy regression: `python -m compileall -q app tests scripts` and `python -m pytest -q`. Desktop and 390-pixel browser checks verify readable pages, working route links and no horizontal content overflow. The website currently lacks standard pre/post hook files; its fallback is the pytest gate in `check_and_deploy.sh` and the explicit post-deploy verifier below.

Use the canonical us3 deployment driver with a list containing only `dalifin_company_bible_20261030`. The scoped configuration leaves the old website process running while building and uses an unused website-specific cron-service name so shared cron is not stopped. Restart only the website parent/worker pair after the new artifact is installed. Retain a root-only snapshot of the previous binary, configuration and runtime metadata for rollback, and restore it if health/version checks fail.

The generic driver's host test script includes live trading and unrelated AI jobs. The user's authorization covers website policy publication, not financial workflows. The website-only rollout therefore substitutes scoped, read-only host integration checks for that broad script; it must not claim the global trading suite passed. Pre-deploy regression is not waived. Run:

```sh
python scripts/verify_deploy.py --base-url http://127.0.0.1:5003 --api-url http://127.0.0.1:5005/account/api --expected-build-id SOURCE_COMMIT
python scripts/verify_deploy.py --base-url https://dalifin.com --api-url http://127.0.0.1:5005/account/api --expected-build-id SOURCE_COMMIT
```

Also verify GET and HEAD for all three public policy URLs, public privacy-index discovery, existing app-policy pages including Apache-served policies, and `/support/api/config`. These checks validate the website and its download API integration without creating payment intents, sending email or running trading tasks. Record actual results in the DaliBible release progress document.

Publishing these pages closes their hosting/discovery work only. Moderation ownership, Data Safety declarations, retention-operation acceptance and complete cross-service account deletion remain separate release gates.
