---
name: siteswarm
description: Build, convert, edit, validate, or stage SiteSwarm Liquid themes. Use for theme briefs, HTML mockups, theme ZIPs, Liquid routes, datasets, editable settings, or a numbered theme version handoff in SiteSwarm.
---

# SiteSwarm theme development

Use the official `swarm` theme client. Check `swarm version` and `swarm help` before choosing commands. If it is unavailable, follow [setup](references/validation.md#set-up-the-public-client). Local lint and preview need a running Docker engine. A browser or browser automation tool is enough for visual checks.

- **New theme**. Copy [the working starter](assets/starter/) to a new directory, or use `swarm new <directory> --example`. Set the manifest identity, replace the sample copy and data, and adapt the design to the brief.
- **Convert HTML**. Preserve the source and use it as the visual reference. Follow [authoring](references/authoring.md#convert-an-html-mockup) to map routes, assets, shared components, and editable content into a theme directory.
- **Edit an existing theme**. Inspect the layout, manifest, routes, settings, and dataset aliases before changing files. Preserve setting IDs, record fields, and existing URLs unless the user requests a change. Use [authoring](references/authoring.md#edit-an-existing-theme) for targeted edits.
- **Verify**. Run `swarm lint <theme-directory>` and `swarm dev <theme-directory>`. Use the [validation guide](references/validation.md) to test rendered routes, content, assets, and layout. Report any checks the environment prevented.
- **Hand off or stage**. Follow [staging](references/staging.md) for ZIP packaging, account upload, version selection, and an optional staging assignment. Identify the account, theme, version, and site before changing a hosted resource. Create a separate theme when the requested work must leave a shared theme alone. Publish a site only when the user specifically authorizes that production action.

Keep credentials in local configuration. Keep hosted content edits separate from source changes. For record-scoped draft fields, follow [record settings](references/authoring.md#add-record-scoped-draft-settings) and verify changes on the actual staging URL.
