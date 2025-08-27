# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube Batch Video Downloader - A Python tool for downloading multiple YouTube videos using YAML configuration files. Uses yt-dlp (not pytube) for reliable video downloading.

## Dependencies & Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Requirements:
- Python 3.6+
- yt-dlp >= 2023.12.30
- PyYAML >= 6.0

## Running the Tool

```bash
python get_video.py <config_file.yaml>
```

Example:
```bash
python get_video.py Files/Files_In/test_config.yaml
```

## Architecture

### Main Components
- `get_video.py`: Single-file implementation with `YouTubeDownloader` class
- Configuration: YAML files in `Files/Files_In/` directory
- Downloads saved to paths specified in config files

### Key Design Decisions
- Uses subprocess to call yt-dlp (more reliable than pytube)
- Object-oriented design with all functionality in YouTubeDownloader class
- Graceful error handling - continues processing if individual downloads fail
- Auto-creates target directories as needed

### YAML Configuration Schema
```yaml
videos:
  - url: "https://youtube.com/watch?v=..."
    save_as: "filename_without_extension"
    save_to: "/path/to/directory/"
```

## Testing & Development

### Manual Testing
Test with provided example configs:
```bash
python get_video.py Files/Files_In/example_gabrielfeo_config.yaml
python get_video.py Files/Files_In/example_ivanrosario_config.yaml
```

### Common Test Scenarios
- Invalid URLs: Tool reports error and continues
- Missing directories: Auto-created
- Invalid YAML: Clear error messages
- Network issues: Handled by yt-dlp with retry logic

## Code Conventions

- Type hints used throughout
- Docstrings for all methods
- PEP 8 compliant
- Clear error messages with context
- Uses pathlib for cross-platform path handling

## Important Notes

- The project was developed as a comparison across multiple AI assistants (see Reports/ folder)
- Production version uses yt-dlp instead of originally specified pytube
- Downloads best quality up to 1080p with embedded subtitles when available
- Uses advanced format selection to ensure video+audio merge for all content types
- No automated tests - rely on manual testing with example configs