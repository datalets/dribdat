<div align="center">
  <img src="dribdat/static/img/logo/logo13.png" alt="Dribdat Logo" width="150">
  <h1>Dribdat</h1>
  <p><b>A playful platform for data-driven hackathons and creative sprints.</b></p>
</div>

![Github Actions build status](https://github.com/dribdat/dribdat/workflows/build/badge.svg)
[![codecov status](https://codecov.io/gh/dribdat/dribdat/branch/main/graph/badge.svg?token=Ccd1vTxRXg)](https://codecov.io/gh/dribdat/dribdat)
[![FOSSA status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Floleg%2Fdribdat.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Floleg%2Fdribdat?ref=badge_shield)
[![OpenCollective](https://opencollective.com/dribdat/backers/badge.svg)](#backers)
[![OpenCollective](https://opencollective.com/dribdat/sponsors/badge.svg)](#sponsors)

Dribdat is an open-source hackathon management application designed to bring your collaborative events to life. It provides a suite of tools to help you organize, run, and showcase hackathons, workshops, and creative sprints. Built on open data standards, Dribdat is your all-in-one solution for fostering innovation and collaboration.

## ✨ Key Features

*   **📅 Full Event Lifecycle:** From announcing your event and publishing challenges to forming teams and showcasing results, Dribdat has you covered.
*   **🧩 Project Curation:** A playful and engaging interface for participants to explore ideas and for organizers to manage projects.
*   **🔄 Data Aggregation:** Automatically sync project updates from GitHub, GitLab, Gitea, Etherpad, and more.
*   **🛠️ Rich Tool Integrations:** Connect with popular platforms like Slack, Mattermost, Discord, and others.
*   **🎨 Customizable & Themeable:** Tailor the platform to your event's brand with a customizable frontend and admin-configurable settings.
*   **📊 Progress Tracking:** Keep a pulse on all projects with real-time progress logs and updates.
*   **🚀 Alternative Frontends:** Use the standard Bootstrap UI, or try [Backboard](https://github.com/dribdat/backboard) (Vue.js) for a more modern feel.

## 🚀 Getting Started

Get a local instance of Dribdat up and running in just a few minutes with Docker.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dribdat/dribdat.git
    cd dribdat
    ```

2.  **Run with Docker Compose:**
    ```bash
    docker-compose -f docker-compose.sqlite.yml up
    ```
    This will start Dribdat using a simple, self-contained SQLite database.

3.  **Launch!**
    Open your browser and navigate to [http://localhost:5000](http://localhost:5000). The first user to register becomes an admin!

For more advanced installation options, including production setups, check out our [Deployment Guide](https://docs.dribdat.cc/deploy).

## 🌍 Live Demo & Showcase

*   **Live Demo:** See a demo of Dribdat in action at [demo.dribdat.cc](https://demo.dribdat.cc/event/1).
*   **Tour de Hack:** Explore a showcase of past events powered by Dribdat at the [Tour de Hack](https://dribdat.cc/tour).

## 🤖 The Dribdat Ecosystem

Dribdat is more than just a web application. It's an ecosystem of tools designed to work together:

*   **[dribdat/dribdat](https://github.com/dribdat/dribdat):** The core Flask-based web application.
*   **[dribdat/backboard](https://github.com/dribdat/backboard):** A responsive, modern alternative frontend built with Vue.js.
*   **[dribdat/dridbot](https://github.com/dribdat/dridbot):** A chatbot client that integrates with the Dribdat API.

## ❤️ Contributing

We welcome contributions of all kinds! Whether you're a developer, a designer, or a hackathon organizer, we'd love your help to make Dribdat even better.

*   **Code of Conduct:** We are committed to providing a welcoming and inclusive environment. Please read our [Code of Conduct](CODE_OF_CONDUCT.md).
*   **Contributor's Guide:** For information on how to contribute, please see our [Contributor's Guide](https://docs.dribdat.cc/contribute).
*   **Discussions:** Have a question or an idea? Join our [GitHub Discussions](https://github.com/orgs/dribdat/discussions).

## 🙏 Acknowledgements

Dribdat was originally based on [cookiecutter-flask](https://github.com/sloria/cookiecutter-flask). We are grateful to the many [contributors and supporters](CREDITS.md) who have helped shape this project.

The original `README.md` can be found [here](README_old.md).

## 📄 License

This project is open source under the [MIT License](LICENSE).
