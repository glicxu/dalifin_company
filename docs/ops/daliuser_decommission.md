# DaliUser Website Decommission

## Purpose

This checklist applies only after `dalifin.com` has been running from `dalifin_company` stably for one release window.

## Preconditions

- Apache for `dalifin.com` is still proxying to `127.0.0.1:5003`
- the process behind `127.0.0.1:5003` is now `dalifin_company`, not the legacy website-serving `dali_user`
- public smoke checks are clean
- rollback to `DaliUser` is no longer considered necessary

## Checklist

1. Confirm `dalifin.com` traffic no longer depends on the `dali_user` website process.
2. Document any remaining `DaliUser` responsibilities that are not part of the public site.
3. Remove the legacy website-serving `dali_user` start path from the nanny-managed process list.
4. Stop and disable the legacy public-site process if it has no remaining purpose.
5. Update operator docs to point to `dalifin_company` as the public-site repo.
6. Archive or narrow `DaliUser` only after the above is complete.
