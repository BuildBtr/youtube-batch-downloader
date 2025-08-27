# YouTube Batch Video Downloader

A robust Python script for downloading multiple YouTube videos based on YAML configuration files. Built with `yt-dlp` for reliable video downloading and batch processing capabilities.

## 🚀 Features

- **Batch Processing**: Download multiple videos from a single configuration file
- **YAML Configuration**: Human-readable configuration format with validation
- **Automatic Directory Management**: Creates target directories automatically
- **Robust Error Handling**: Continues processing even when individual downloads fail
- **Detailed Progress Reporting**: Real-time feedback and comprehensive summaries
- **High-Quality Downloads**: Downloads best available quality up to 1080p
- **Subtitle Support**: Automatically embeds available subtitles
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Requirements

- Python 3.6 or higher
- Internet connection for downloading videos
- Sufficient disk space for video files

## 🛠️ Installation

### 1. Clone or Download the Script

```bash
# Clone the repository (if using git)
git clone <repository-url>
cd youtube-batch-downloader

# Or download get_video.py directly
```

### 2. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Or install manually
pip install yt-dlp PyYAML
```

### 3. Verify Installation

```bash
# Check if yt-dlp is working
yt-dlp --version

# Test the script
python get_video.py --help
```

## 🎯 Quick Start

### 1. Create a Configuration File

Create a YAML file (e.g., `my_videos.yaml`) with your video specifications:

```yaml
videos:
  - url: https://www.youtube.com/watch?v=dQw4w9WgXcQ
    title: "Never Gonna Give You Up"
    author: "Rick Astley"
    save_directory: "./downloads/music"

  - url: https://www.youtube.com/watch?v=9bZkp7q19f0
    title: "PSY - GANGNAM STYLE"
    author: "officialpsy"
    save_directory: "./downloads/music/kpop"
```

### 2. Run the Script

```bash
python get_video.py my_videos.yaml
```

### 3. Monitor Progress

The script will provide detailed feedback:

```
Reading configuration from: my_videos.yaml
Found 2 videos in configuration
Using yt-dlp version: 2023.12.30

Processing video: 'Never Gonna Give You Up' (URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ)
  Fetching video information...
  Video: 'Rick Astley - Never Gonna Give You Up (Official Video)' by Rick Astley
  Duration: 03:33
  Downloading to: ./downloads/music
  Successfully downloaded 'Rick Astley - Never Gonna Give You Up (Official Video)' to './downloads/music'

Batch download process completed.
Successfully downloaded: 2/2 videos
```

## 📖 Usage

### Command Line Interface

```bash
python get_video.py <path_to_yaml_config>
```

**Examples:**
```bash
# Using relative path
python get_video.py videos_config.yaml

# Using absolute path
python get_video.py /home/user/configs/my_videos.yaml

# Show help
python get_video.py --help
```

### Configuration File Format

The YAML configuration file must follow this exact structure:

```yaml
videos:
  - url: <YouTube_URL>
    title: <Display_Title>
    author: <Channel_Name>
    save_directory: <Target_Directory>
  
  - url: <YouTube_URL>
    title: <Display_Title>
    author: <Channel_Name>
    save_directory: <Target_Directory>
```

#### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `url` | String | Full YouTube video URL | `https://www.youtube.com/watch?v=VIDEO_ID` |
| `title` | String | Video title for reference/logging | `"Learning Python Basics"` |
| `author` | String | Channel name for reference/logging | `"CodeMaster"` |
| `save_directory` | String | Target download directory | `"./downloads/tutorials"` |

#### Configuration Examples

**Basic Configuration:**
```yaml
videos:
  - url: https://www.youtube.com/watch?v=VIDEO_ID
    title: "My Video Title"
    author: "Channel Name"
    save_directory: "./downloads"
```

**Advanced Configuration with Multiple Categories:**
```yaml
videos:
  # Educational Content
  - url: https://www.youtube.com/watch?v=TUTORIAL_ID
    title: "Python Tutorial #1"
    author: "TechChannel"
    save_directory: "./downloads/education/python"
  
  - url: https://www.youtube.com/watch?v=TUTORIAL_ID2
    title: "JavaScript Basics"
    author: "WebDev Pro"
    save_directory: "./downloads/education/javascript"
  
  # Entertainment
  - url: https://www.youtube.com/watch?v=MUSIC_ID
    title: "Favorite Song"
    author: "Artist Name"
    save_directory: "./downloads/music"
  
  # Documentaries
  - url: https://www.youtube.com/watch?v=DOC_ID
    title: "Nature Documentary"
    author: "Documentary Channel"
    save_directory: "/home/user/Videos/documentaries"
```

## Template Files

This repository includes template configuration files for different users:
- `Files/Files_In/my_videos-TEMPLATE-Ivan.yaml` - Template for Ivan
- `Files/Files_In/my_videos-TEMPLATE-Gabriel.yaml` - Template for Gabriel

Copy and customize these templates for your own use.

## 🏗️ Technical Architecture

### Class Structure

#### `YouTubeDownloader`
Main class responsible for batch video downloading operations.

**Key Methods:**
- `load_config(config_path)`: Validates and loads YAML configuration
- `download_video(video_config)`: Downloads individual video
- `download_batch(config_path)`: Orchestrates batch download process
- `create_directory(directory_path)`: Handles directory creation
- `get_video_info(url)`: Fetches video metadata using yt-dlp

### Dependencies

- **yt-dlp**: Core video downloading functionality
- **PyYAML**: Configuration file parsing
- **subprocess**: Interface with yt-dlp command-line tool
- **pathlib**: Modern path handling
- **json**: Video metadata parsing

### Download Process Flow

1. **Configuration Loading**: Parse and validate YAML file
2. **Dependency Check**: Verify yt-dlp installation
3. **Batch Processing**: Iterate through video list
4. **Video Processing**: For each video:
   - Fetch metadata
   - Create target directory
   - Execute download with yt-dlp
   - Report results
5. **Summary Report**: Display final statistics

## ⚙️ Configuration Options

### yt-dlp Download Settings

The script uses these yt-dlp options by default:

```python
cmd = [
    'yt-dlp',
    '--format', 'best[height<=1080][ext=mp4]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',  # Ensure video+audio merge
    '--merge-output-format', 'mp4',   # Force mp4 container for compatibility
    '--output', '%(title)s.%(ext)s',  # Filename format
    '--no-playlist',                  # Single video only
    '--embed-subs',                   # Embed subtitles
    '--write-auto-sub',              # Auto-generated subtitles
    url
]
```

**Format Selection Explanation:**
- `best[height<=1080][ext=mp4]`: Prefers single files with video+audio in mp4 format
- `bestvideo[height<=1080]+bestaudio`: Falls back to merging separate video and audio streams
- `best[height<=1080]`: General fallback for quality-limited downloads
- `best`: Final fallback for any available format
- `--merge-output-format mp4`: Ensures proper video+audio container format

This format selection ensures downloaded videos contain both video and audio tracks, preventing audio-only downloads that can occur with long-form content.

### Customization Points

To modify download behavior, edit the `download_video` method:

```python
# Example: Change quality to 720p maximum
'--format', 'best[height<=720]'

# Example: Include video description
'--write-description'

# Example: Download audio only
'--format', 'bestaudio/best'
```

## 🚨 Error Handling

### Common Issues and Solutions

#### 1. HTTP Error 400/403
**Cause**: YouTube blocking requests or video restrictions
**Solution**: 
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Check if video is available in your region
- Verify URL format

#### 2. Permission Denied
**Cause**: Insufficient permissions to create directories
**Solution**: 
- Check directory permissions
- Use absolute paths
- Run with appropriate user permissions

#### 3. No Space Left on Device
**Cause**: Insufficient disk space
**Solution**: 
- Free up disk space
- Choose different target directory
- Download smaller format

#### 4. yt-dlp Not Found
**Cause**: yt-dlp not installed or not in PATH
**Solution**: 
```bash
pip install yt-dlp
# Or reinstall if corrupted
pip uninstall yt-dlp && pip install yt-dlp
```

### Error Recovery

The script implements robust error recovery:
- **Individual Failures**: Continues processing remaining videos
- **Configuration Errors**: Provides specific validation messages
- **Network Issues**: Reports connection problems clearly
- **File System Errors**: Handles permission and space issues gracefully

## 🧪 Testing

### Manual Testing

1. **Basic Functionality**:
```bash
# Test with single video
echo "videos:
  - url: https://www.youtube.com/watch?v=dQw4w9WgXcQ
    title: Test Video
    author: Test Author  
    save_directory: ./test_downloads" > test_config.yaml

python get_video.py test_config.yaml
```

2. **Error Handling**:
```bash
# Test with invalid URL
echo "videos:
  - url: https://invalid-url
    title: Invalid Test
    author: Test
    save_directory: ./test" > error_test.yaml

python get_video.py error_test.yaml
```

3. **Directory Creation**:
```bash
# Test with non-existent directory
echo "videos:
  - url: https://www.youtube.com/watch?v=dQw4w9WgXcQ
    title: Directory Test
    author: Test
    save_directory: ./new/nested/directory" > dir_test.yaml

python get_video.py dir_test.yaml
```

### Integration Testing

For automated testing, consider:
- Mock yt-dlp responses for consistent testing
- Test configuration file validation
- Verify directory creation behavior
- Test error handling scenarios

## 🔒 Security Considerations

### Input Validation
- URLs are validated by yt-dlp before processing
- File paths are sanitized using pathlib
- YAML parsing uses safe_load to prevent code injection

### File System Safety
- Creates directories with appropriate permissions
- Handles path traversal safely
- Validates write permissions before download

### Network Security
- Uses yt-dlp's built-in security features
- No direct network programming (delegated to yt-dlp)
- Handles SSL/TLS through yt-dlp

## 📈 Performance Considerations

### Download Speed
- Sequential processing (not parallel)
- Network bandwidth is the primary bottleneck
- File I/O optimized by yt-dlp

### Memory Usage
- Minimal memory footprint
- Video data streamed directly to disk
- Configuration loaded once at startup

### Scalability
- Suitable for batches up to ~100 videos
- For larger batches, consider splitting configuration files
- Monitor disk space usage

## 🤝 Contributing

### Development Setup

1. **Clone Repository**:
```bash
git clone <repository-url>
cd youtube-batch-downloader
```

2. **Install Development Dependencies**:
```bash
pip install -r requirements.txt
pip install black flake8 pytest  # Development tools
```

3. **Code Style**:
- Follow PEP 8 guidelines
- Use Black for code formatting: `black get_video.py`
- Use type hints where applicable

### Contribution Guidelines

1. **Bug Reports**: Include configuration file, error messages, and system info
2. **Feature Requests**: Describe use case and proposed implementation
3. **Pull Requests**: Include tests and documentation updates
4. **Code Review**: All changes require review before merging

### Testing New Features

```bash
# Run basic tests
python get_video.py test_configs/basic_test.yaml

# Test error conditions
python get_video.py test_configs/error_test.yaml

# Validate code style
black --check get_video.py
flake8 get_video.py
```

## 📝 License

MIT License - see LICENSE file for details.

## 🆘 Support

### Getting Help

1. **Check Documentation**: Review this README thoroughly
2. **Common Issues**: See Error Handling section above
3. **Update Dependencies**: `pip install --upgrade yt-dlp PyYAML`
4. **Report Bugs**: Create an issue with detailed information

### Issue Template

When reporting issues, please include:
- Operating system and Python version
- Complete error message
- YAML configuration file (remove sensitive URLs)
- yt-dlp version (`yt-dlp --version`)

### Useful Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(yt-dlp|PyYAML)"

# Test yt-dlp directly
yt-dlp --simulate https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Verbose output for debugging
python get_video.py config.yaml 2>&1 | tee debug.log
```

---

**Last Updated**: July 2025  
**Version**: 1.0.0  
**Maintainer**: Ivan & Gabriel