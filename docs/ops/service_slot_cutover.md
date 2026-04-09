# Service Slot Cutover

## Production Reality

`dalifin.com` already reverse-proxies to:

- `http://127.0.0.1:5003`

Apache does not need a new target if `dalifin_company` replaces the current website process on that same port.

## Intended Cutover Model

1. keep `/etc/apache2/sites-enabled/dalifin.com` unchanged
2. stop serving the public website from the current `dali_user` process
3. start `dalifin_company` on the existing `5003` slot
4. let Apache continue proxying to `127.0.0.1:5003`

## Config Model

The repo now supports:

```bash
python ./dalifin_company.py -c /data/dali/prod/config/app_ops.ini
```

Expected config resolution:

- bind host/port from `[dali_user]` unless a dedicated `[dalifin_company]` section is added later
- `app_server` API base from `[app_server]`

With the current `app_common.ini`, that means:

- website bind port: `5003`
- backend API base: `http://127.0.0.1:5005/account/api`

## Nanny Integration

The current nanny control point is:

- `B:\src\workspaces\DaliConfigFile\prod\bin\dali_service_nanny.sh`

Today it manages the old website slot through:

- `dali_user:/data/dali/prod/bin/run_user_service.sh`

The operational cutover should replace the command behind that website slot with a `dalifin_company` runner, or add a dedicated `dalifin_company` process entry and remove the old one after stability is proven.
