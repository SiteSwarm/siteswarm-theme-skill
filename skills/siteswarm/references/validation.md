# Validate a SiteSwarm theme

## Set up the public client

Install Node.js 18 or newer and start Docker. Install the [official client](https://github.com/ClockworkEmpire/theme-dev) from its public source:

```sh
npm install -g 'https://codeload.github.com/ClockworkEmpire/theme-dev/tar.gz/2135a1c683e64d272eba651308b1973d102937db'
swarm version
```

If Docker reports no matching ARM manifest, enable AMD64 emulation in Docker and run the client with `DOCKER_DEFAULT_PLATFORM=linux/amd64`, for example `DOCKER_DEFAULT_PLATFORM=linux/amd64 swarm lint ./my-theme`.

## Check the theme

Run `swarm lint ./my-theme`. Read errors and warnings, correct the source, and rerun. If you use `--fix`, review the diff because it can infer fields and remove unused settings.

The current linter may flag the starter's `seo_title` and `seo_description` as unused. SiteSwarm reads those settings when it builds hosted metadata, so keep them when the theme supports record-scoped SEO drafts.

Start `swarm dev ./my-theme --port 4100`. Use a free port and keep the adjacent port available for live reload. Open the URL printed by the client in any browser or browser automation tool. Compare a conversion with its source at the same viewport widths.

| Check | What to verify |
| --- | --- |
| Home and navigation | Main heading, accessible links, expected destinations, responsive navigation |
| Collection and item routes | Correct records, links, empty states, pagination when present, and a real HTTP 404 for missing items |
| Assets and behavior | CSS, images, fonts, scripts, form behavior, and browser console errors relevant to the theme |
| Editable values | Reasonable defaults in local preview, then actual saved settings on a staging site |
| SEO | Correct title and description, and expected canonical, social, and robots metadata in the hosted environment |
| Layout | Check a desktop viewport and a narrow viewport around 390 px for overflow, legibility, and working controls |

The included starter uses `/`, `/services`, `/services/site-survey`, `/services/planting-plan`, and `/about`. Try `/services/no-such-service` and expect HTTP 404. Change a sample record or a section default and verify the edit after preview reload. Local preview uses sample data and can show site-wide metadata for a static route. Hosted staging is the check for actual datasets, customizer saves, and account settings.
