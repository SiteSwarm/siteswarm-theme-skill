# SiteSwarm Theme Skill

Build a theme from a brief, turn an HTML mockup into Liquid, or update an existing SiteSwarm theme. The skill includes a working example with a homepage, service listing and detail pages, editable settings, sample records, and a 404 page.

## Install

1. Install Node.js 18 or newer and [Docker](https://docs.docker.com/get-docker/). Start Docker before running theme lint or preview.
2. Install the official client from its public source and check the version.

   ```sh
   npm install -g 'https://codeload.github.com/ClockworkEmpire/theme-dev/tar.gz/2135a1c683e64d272eba651308b1973d102937db'
   swarm version
   ```

3. Copy the entire [skills/siteswarm](skills/siteswarm) folder to your agent's personal skills directory. In Codex, use `~/.codex/skills/siteswarm` (or `$CODEX_HOME/skills/siteswarm` if set). In Claude Code, use `~/.claude/skills/siteswarm`. Restart the agent if the skill does not appear. On Codex you can invoke it explicitly with `$siteswarm`.

The example and local workflow use sample data and run without SiteSwarm account credentials. An account is needed for hosted uploads, previews, and staging assignment.

On Apple Silicon or another ARM host, the current preview image requires AMD64 emulation. Enable it in Docker and prefix `swarm lint` and `swarm dev` with `DOCKER_DEFAULT_PLATFORM=linux/amd64` in the commands below.

## Build your first theme

Ask your agent to use the SiteSwarm skill to build a theme from a brief or from an HTML folder. Give it an output directory and tell it which pages need to be editable. For a quick look at the included starter, run these commands from this repository on macOS or Linux:

```sh
cp -R skills/siteswarm/assets/starter ./field-notes-demo
swarm lint ./field-notes-demo
swarm dev ./field-notes-demo --port 4100
```

Open [the local preview](http://localhost:4100) and try **Services**. The [authoring guide](skills/siteswarm/references/authoring.md) covers conversion and editing, the [validation guide](skills/siteswarm/references/validation.md) lists checks to run, and the [staging guide](skills/siteswarm/references/staging.md) explains how to hand off a tested version.

The [official SiteSwarm theme documentation](https://app.siteswarm.co/docs/theme-development/getting-started) covers additional platform features.
