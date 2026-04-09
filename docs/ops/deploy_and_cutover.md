# Dalifin Company Deploy And Cutover

## Purpose

This repo-local guide turns the migration plan into executable staging and cutover steps.

The shared SRE runbook remains the primary service guide:

- [shared service runbook](B:\src\workspaces\sre\docs\services\dalifin_company.md)

## Stage On `us3`

1. Sync the repo to `/home/dali-op/dali/dalifin_company`.
2. Create or refresh the venv.
3. Copy `env/stage.env.example` to a host-local env file and fill the real values.
4. Start the staging runtime with:

```bash
cd /home/dali-op/dali/dalifin_company
source .venv/bin/activate
./scripts/run_site.sh restart --env-file ./env/stage.env
```

5. Verify the staged app and staged API:

```bash
source .venv/bin/activate
python ./scripts/verify_deploy.py \
  --base-url http://127.0.0.1:5103 \
  --api-url http://127.0.0.1:8100/account/api
```

6. Compare the staged homepage against the live `dalifin.com` surface.

## Production Cutover

The preferred production model is now:

- keep Apache pointing at `127.0.0.1:5003`
- replace the website process behind that slot

1. Start `dalifin_company` from the existing config model:

```bash
cd /home/dali-op/dali/dalifin_company
source .venv/bin/activate
python ./dalifin_company.py -c /data/dali/prod/config/app_ops.ini
```

2. Verify locally behind the existing port:

```bash
source .venv/bin/activate
python ./scripts/verify_deploy.py \
  --base-url http://127.0.0.1:5003 \
  --api-url http://127.0.0.1:5005/account/api
```

3. Re-run smoke checks through the public hostname.
4. Keep the old `DaliUser` rollback path available for one release window.

## Rollback

If cutover fails:

1. restart the old `dali_user` website process behind `5003`
2. keep `dalifin_company` isolated for investigation
3. capture:
   - `/tmp/dalifin_company.out`
   - `/tmp/dalifin_company.err`
   - `python ./scripts/verify_deploy.py ...` output
   - local `curl` results for `/healthz`, `/version`, and `/downloads`
