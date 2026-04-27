# Pediatrix SDBI Pre-commit Hooks

## record_precommit_ran

This hook will add the github username to a file in the .github directory that contains their github username, github email, if they have signed commits active, and the last date (Y-m-d) this was run.

The purpose of this hook is to as a second layer of enforcement that pre-commit has been installed on a users local machine. If they do not have it installed and have run it, their name will not be added to this list. 

Combine this with the github action found at [https://github.com/mednax-it/devsecops-tools/tree/main/.github/workflows](https://github.com/mednax-it/devsecops-tools/blob/main/.github/workflows/check_for_precommit.yml)  will enable an On PR action that checks if the person making the latest commit to trigger the PR git action has their git user in the file. If so, then good - theyve run pre-commit at least once. If not, then bad, they need to run it (and the pipeline will fail)

### Add to pre-commit-config.yaml hooks

```yaml
repos:
-   repo: https://github.com/mednax-it/sdbi-devsecops-precommithooks
    rev: enforcement.v1.0.4
    hooks:
    - id: record-precommit-ran
```

and run `pre-commit autoupdate` to get the latest version

Then run `pre-commit run --all-files` or make a change and a normal commit to add your username to the file naturally. Include the linked github action in your own repo and this will verify it.