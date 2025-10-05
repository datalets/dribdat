![Github Actions build status](https://github.com/dribdat/dribdat/workflows/build/badge.svg)
[![codecov status](https://codecov.io/gh/dribdat/dribdat/branch/main/graph/badge.svg?token=Ccd1vTxRXg)](https://codecov.io/gh/dribdat/dribdat)
[![FOSSA status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Floleg%2Fdribdat.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Floleg%2Fdribdat?ref=badge_shield)

# Dribdat

**A playful platform for data-driven hackathons and hexagonal teams.**

Designed to bootstrap your [awesome hackathon](https://github.com/dribdat/awesome-hackathon) ⬡⬢⬡ Dribdat is a versatile open source toolbox for civic tech sprints and crowdsourcing. To get started, [install](#Quickstart) the software.
See 🚲 [Tour de Hack](https://dribdat.cc/tour) for examples, and 📖 [User handbook](https://dribdat.cc/usage) for screenshots.  
There are mirrors on 🏔️ [Codeberg](https://codeberg.org/dribdat/dribdat) and [GitHub](https://github.com/dribdat/dribdat). 

We aim to include people of all backgrounds in using + developing this tool - no matter your age, gender, race, ability, or sexual identity. Please review our 🏳️‍🌈 [Code of Conduct](CODE_OF_CONDUCT.md).

**Support us**: 🩵 [OpenCollective](https://opencollective.com/dribdat/updates)

# Purpose

Created in light of the [Hacker ethic](https://en.wikipedia.org/wiki/Hacker_ethic), the Zen of Dribdat is (in a nutshell):

- **Commit sustainably**: archive collected results in open, web-friendly data formats.
- **Live and let live**: share designs, dev-envs, docs accessible to your entire team.
- **Co-create in safe spaces**: promote safer conduct, balancing openness with privacy.
- **Appreciate hexagons:** 120° of symmetry imply community resilience and social good.

Key features include:

* **📅 Full Event Lifecycle:** From announcing your event and publishing challenges to forming teams and showcasing results, Dribdat has you covered.
* **🧩 Project Curation:** A playful and engaging interface for participants to explore ideas and for organizers to manage projects.
* **🔄 Data Aggregation:** Automatically sync project updates from Git, Forgejo, Etherpad, and more.
* **🛠️ Rich Tool Integrations:** Connect with popular platforms like Slack, Mattermost, Discord, and others.
* **🎨 Customizable & Themeable:** Tailor the platform to your event's brand with a customizable frontend and admin-configurable settings.
* **📊 Progress Tracking:** Keep a pulse on all projects with real-time progress logs and updates.
* **🚀 Alternative Frontends:** Use the standard Bootstrap UI, or try [Backboard](https://github.com/dribdat/backboard) (Vue.js) for a more modern feel.

**Live demo:** 🫀 [demo.dribdat.cc](https://demo.dribdat.cc/)

Visit the [Hackfinder](https://hackintegration.ch/hackfinder) to find events connected to current research, and join our [Hack:Org:X](https://hackorgx.dribdat.cc) meetings with hackathon organizers.
For more background and references, see the [User Handbook](https://docs.dribdat.cc/usage). If you need help in setting up, please get in touch via 🗣️ [Discussions](https://github.com/orgs/dribdat/discussions).

# Quickstart

The Dribdat project can be deployed to any server capable of serving [Python](https://python.org) applications, and is set up for fast deployment using [Ansible or Docker](https://dribdat.cc/deploy) 
🏀 The first user that registers becomes an admin, so don't delay when you make your play!

**Run with Docker Compose:**

```bash
    docker-compose -f docker-compose.sqlite.yml up
```

This will start Dribdat using a simple, self-contained SQLite database.

If you would like to run this application on any other cloud or local machine, there are instructions in the [Deployment guide](https://docs.dribdat.cc/deploy). Information on contributing and extending the code can be found in the [Contributors guide](https://docs.dribdat.cc/contribute), which includes API documentation, and other details.

See also **[backboard](https://github.com/dribdat/backboard)**: a responsive, modern alternative frontend, and our **[dridbot](https://github.com/dribdat/dridbot)** chat client. Both demonstrate reuse of the dribdat API. If you need support with your deployment, please reach out through [Discussions](https://github.com/orgs/dribdat/discussions). Pull Requests and Issues welcome!

| Development Status | ASCII Signature | Branding |
| --- | --- | --- |
| [Perpetual beta](https://en.wikipedia.org/wiki/Perpetual_beta) |  `d}}BD{t` | [logo folder](dribdat/static/img/logo/) |

<a href="https://opencollective.com/dribdat/donate" target="_blank"><img src="https://opencollective.com/dribdat/donate/button@2x.png?color=blue" width=300 /></a>

# Credits

This application was based on [cookiecutter-flask](https://github.com/sloria/cookiecutter-flask) by [Steven Loria](https://github.com/sloria), a more modern version of which is [cookiecutter-flask-restful](https://github.com/karec/cookiecutter-flask-restful). [Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html#available-templates) could also be a good bootstrap for your own hackathon projects!

♡ The [Open Data](https://opendata.ch), [Open Networking](https://opennetworkinfrastructure.org/) and [Open Source](https://dinacon.ch) communities in 🇨🇭 Switzerland gave this project initial form and direction through a hundred events. ♥-felt thanks to our [Contributors](https://github.com/dribdat/dribdat/graphs/contributors), and additionally: F. Wieser and M.-C. Gasser at [Swisscom](http://swisscom.com) for support at an early stage of this project, to [Alexandre Cotting](https://github.com/Cotting), [Anthony Ritz](https://github.com/RitzAnthony), [Chris Mutel](https://github.com/cmutel), [Fabien Schwob](https://github.com/jibaku), [Gonzalo Casas](https://github.com/gonzalocasas), [Iliya Tikhonenko](https://github.com/vleugelcomplement), [Janik von Rotz](https://janikvonrotz.ch/), [Jonathan Schnyder](https://github.com/jonHESSO), [Jonathan Sobel](https://github.com/JonathanSOBEL), [Philip Shemella](https://github.com/philshem), [Thomas Amberg](https://github.com/tamberg), [Yusuf Khasbulatov](https://github.com/khashashin) .. and all participants, donors and organizers sending in bugs and requests! You are all awesome `h`a`c`k`e`r`s` ♡

## License

This project is open source under the [MIT License](LICENSE).

The [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md) applies to interactions with the maintainers and support community of the project.

Due to the use of the [boto3](https://github.com/boto/boto3/) library for optional S3 upload support, there is a dependency on OpenSSL via awscrt. If you use these features, please note that the product includes cryptographic software written by Eric Young (eay@cryptsoft.com) and Tim Hudson (tjh@cryptsoft.com).
