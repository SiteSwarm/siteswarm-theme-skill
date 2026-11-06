# Package and hand off a SiteSwarm theme

The authoring and preview workflow runs locally. Hosted upload needs a SiteSwarm account and authorization for the destination.

## ZIP handoff

From the skill directory, package the finished theme with Python 3.9 or newer:

```sh
python3 scripts/package-theme.py /path/to/my-theme /path/to/my-theme.zip
```

The archive opens directly to `layout/`, `templates/`, and other theme files. The helper includes supported theme paths and omits local configuration such as `.siteswarm.yml` and `.hostnet.yml`. Inspect the archive and check that sample data and assets are cleared for the receiving account. Upload it under **Themes** to a new theme when the user wants an isolated copy.

## CLI handoff

Use `swarm env add staging` to configure the account and server privately. Check the target account and existing theme mapping before a push. With authorization, create an isolated account theme:

```sh
swarm push ./my-theme --env staging --create --theme-name "My Theme"
```

Updating an existing theme requires a confirmed theme ID. A push changes shared theme source in the selected account. A numbered version is the review point. Confirm the version shown in the dashboard before assigning it to the intended site's **Staging** environment. The environment name in the CLI is a connection label. The dashboard assignment is what selects a version for a site's staging URL.

Review the staged site with its actual settings, records, assets, and URLs. For draft fields, save a temporary value for one record, reload its preview, check a second record and the production URL, then clear the test value. Use the site's publish action only with explicit production authorization.

See [validation and versioning](https://app.siteswarm.co/docs/theme-development/validation-and-versioning) and [ZIP uploads](https://app.siteswarm.co/docs/themes/upload-a-zip).
