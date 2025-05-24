<p align="center">
  <img src="assets/logo.png" alt="robofuse" width="400" />
</p>

<p align="center">
  <a href="https://github.com/Renoria/robofuse/stargazers"><img src="https://img.shields.io/github/stars/Renoria/robofuse?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/Renoria/robofuse/issues"><img src="https://img.shields.io/github/issues/Renoria/robofuse?style=flat-square" alt="Issues"></a>
  <a href="https://github.com/Renoria/robofuse/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Renoria/robofuse?style=flat-square" alt="License"></a>
  <a href="https://github.com/Renoria/robofuse"><img src="https://img.shields.io/badge/docker-ready-blue?style=flat-square" alt="Docker"></a>
</p>

<p align="center">
  A Python service that interacts with the Real-Debrid API to generate .strm files<br>for media players like Infuse, Jellyfin, and Emby.
</p>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

robofuse connects to your Real-Debrid account and efficiently manages your media files by:

1. Retrieving your torrents and downloads
2. Repairing dead torrents when needed
3. Unrestricting links automatically
4. Generating .strm files for streamable content
5. Maintaining your library by updating or removing stale entries
6. Intelligently organizing media files based on parsed metadata

## Features

- **Efficient API Integration**: Smart rate limiting to prevent API throttling
- **Parallel Processing**: Fast operations with concurrent API requests
- **Smart Organization**: Automatic categorization of media into appropriate folders
- **Metadata Parsing**: Intelligent filename parsing for proper media organization
- **Watch Mode**: Continuous monitoring for new content
- **Caching System**: Reduces redundant API calls
- **Link Management**: Handles expired links and refreshes them automatically
- **Health Checks**: Ensures content integrity
- **Clean UI**: Colorful terminal interface with progress bars
- **Docker Support**: Run in containers for easy deployment
- **Background Services**: Deploy with systemd, launchd, or Docker
- **Log Rotation**: Built-in log management for continuous operation
- **Anime Detection**: Automatically identifies and categorizes anime content

## Quick Start

1. **Install robofuse**:
   ```bash
   git clone https://github.com/Renoria/robofuse.git
   cd robofuse
   pip install -e .
   ```

2. **Configure your Real-Debrid API token** in the existing `config.json` file

3. **Run robofuse**:
   ```bash
   # Show help
   robofuse --help
   
   # Test with dry run first
   robofuse --debug dry-run
   
   # Run once to process all content
   robofuse run
   
   # Start watch mode for continuous monitoring
   robofuse watch
   
   # Watch mode with custom interval
   robofuse watch --interval 300
   ```

4. **Deploy for continuous operation** (optional):
   - See our [Deployment Guide](https://github.com/Renoria/robofuse/wiki/Deployment) for systemd, launchd, or Docker setup

## Documentation

📚 **Complete documentation is available in our [GitHub Wiki](https://github.com/Renoria/robofuse/wiki)**

### Quick Links:
- **[🏠 Home](https://github.com/Renoria/robofuse/wiki/Home)** - Documentation overview and navigation
- **[📦 Installation](https://github.com/Renoria/robofuse/wiki/Installation)** - Complete installation instructions and setup
- **[⚙️ Configuration](https://github.com/Renoria/robofuse/wiki/Configuration)** - API setup, settings, and metadata parsing
- **[🚀 Usage](https://github.com/Renoria/robofuse/wiki/Usage)** - Command reference and usage patterns
- **[🔧 Deployment](https://github.com/Renoria/robofuse/wiki/Deployment)** - Background services, Docker, and production deployment
- **[🛠️ Troubleshooting](https://github.com/Renoria/robofuse/wiki/Troubleshooting)** - Common issues and debugging solutions

> 💡 **Need help?** Start with the [Troubleshooting Guide](https://github.com/Renoria/robofuse/wiki/Troubleshooting) or [open an issue](https://github.com/Renoria/robofuse/issues) if you encounter problems.

## Contributing

Contributions to robofuse are welcome! Here's how you can help:

1. **Bug Reports**: Open an issue describing the bug with steps to reproduce
2. **Feature Requests**: Open an issue describing the new feature and why it would be useful
3. **Code Contributions**: Submit a pull request with your improvements
   - Fork the repository
   - Create a feature branch (`git checkout -b feature/amazing-feature`)
   - Commit your changes (`git commit -m 'Add some amazing feature'`)
   - Push to the branch (`git push origin feature/amazing-feature`)
   - Open a Pull Request

Please ensure your code follows the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.