# Dali Chatty privacy publication - November 10, 2026

The requested public policy is `/privacy/chatty`, discoverable from `/privacy`.
The isolated branch starts at published website commit `f91888b`, preserving
the Audio, Cam, Job, Bible and other existing policies and unrelated local QR work.

Content evidence includes Chatty's published privacy/deletion pages; the local
character/history/memory implementation; Secretary's credential broker and
processing qualification; notes and scheduled-work storage; approved-action
receipts; and the reusable-search contract/device acceptance. The policy
distinguishes local chats from server notebooks/tasks, sign-in from connected
account consent, schedule approval periods from content retention, and
Chatty-only deletion from shared-account or external-provider deletion.

The current release is adult-only. Do not replace this with the template's
default under-13 audience, imply all assistant features are generally released,
claim Google verification, promise instant universal deletion, or describe
unverified provider retention/training restrictions as established facts.
Account-specific pilot sharing terms still require separate consent. Publishing
this page does not enable a feature, renew a processing pilot, or change access.

Use the existing company website workflow: a Git bundle imported into the
existing us3 repository, an isolated Git worktree, full website regression, and
`check_and_deploy.sh` through the canonical deployment driver scoped to this
website only. The existing repo has no separate pre/post hook files; pytest
inside the build and `scripts/verify_deploy.py` are its documented fallbacks.
Keep the live source/configuration and other policies intact. Back up the prior
binary and metadata privately before installation; restart only the website
parent/worker pair, preserving unrelated cron and services.

The generic driver's trading/AI integration jobs are outside this task. As in
the Job/Bible policy rollouts, substitute bounded read-only website/API smoke
checks, including exact build ID, public GET/HEAD for the new route, privacy-index
discovery, existing policies, deletion/terms links, downloads and support config.
Do not claim the global host trading suite passed. Use Playwright for desktop
and mobile layout/navigation checks. Public pages require no account or cookies
to read. No Chatty app/server rollout is included; its About source points to
the new URL for the next app build.

Candidate verification: all 46 website tests passed, compileall passed, and Playwright
confirmed the title, adult audience, deletion/terms/contact links and complete
content at 1280px and 390px. No horizontal content overflow was found. The About
widget regression passed and targeted Dart analysis found no issues. Source
changes are limited to this policy, registry/index/route documentation and its
public rendering/other-policy preservation checks. The website-only host
integration gate is explicit; no broad trading regression is claimed.
