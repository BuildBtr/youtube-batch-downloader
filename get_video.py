#!/usr/bin/env python3
"""
YouTube Batch Video Downloader

This script downloads multiple YouTube videos based on a YAML configuration file.
The configuration file specifies video URLs, metadata, and target directories.

Usage:
    python get_video.py <path_to_yaml_config>

Example:
    python get_video.py videos_config.yaml
    python get_video.py /path/to/config/my_videos.yaml

Requirements:
    - yt-dlp
    - PyYAML
    - Python 3.6+

Author: Senior Automation Script Programmer
"""

import sys
import os
import yaml
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any


class YouTubeDownloader:
    """YouTube video downloader with batch processing capabilities using yt-dlp."""
    
    def __init__(self):
        self.success_count = 0
        self.error_count = 0
        self.total_videos = 0
        self._check_ytdlp_installation()
    
    def _check_ytdlp_installation(self):
        """Check if yt-dlp is installed and available."""
        try:
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"Using yt-dlp version: {result.stdout.strip()}")
        except subprocess.CalledProcessError:
            print("Error: yt-dlp is not installed or not working properly.")
            print("Please install yt-dlp using: pip install yt-dlp")
            sys.exit(1)
        except FileNotFoundError:
            print("Error: yt-dlp is not installed.")
            print("Please install yt-dlp using: pip install yt-dlp")
            sys.exit(1)
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load and validate YAML configuration file.
        
        Args:
            config_path (str): Path to the YAML configuration file
            
        Returns:
            Dict[str, Any]: Parsed configuration data
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML is invalid
            ValueError: If configuration structure is invalid
        """
        print(f"Reading configuration from: {config_path}")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML format in {config_path}: {e}")
        
        # Validate configuration structure
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")
        
        if 'videos' not in config:
            raise ValueError("Configuration must contain a 'videos' key")
        
        if not isinstance(config['videos'], list):
            raise ValueError("'videos' must be a list")
        
        # Validate each video entry
        required_keys = {'url', 'title', 'author', 'save_directory'}
        for i, video in enumerate(config['videos']):
            if not isinstance(video, dict):
                raise ValueError(f"Video entry {i+1} must be a dictionary")
            
            missing_keys = required_keys - set(video.keys())
            if missing_keys:
                raise ValueError(f"Video entry {i+1} missing required keys: {missing_keys}")
        
        self.total_videos = len(config['videos'])
        print(f"Found {self.total_videos} videos in configuration")
        
        return config
    
    def create_directory(self, directory_path: str) -> bool:
        """
        Create directory if it doesn't exist.
        
        Args:
            directory_path (str): Path to the directory to create
            
        Returns:
            bool: True if directory exists or was created successfully
        """
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            if not os.path.exists(directory_path):
                print(f"Creating directory: {directory_path}")
            return True
        except PermissionError:
            print(f"Error: Permission denied creating directory: {directory_path}")
            return False
        except OSError as e:
            print(f"Error creating directory {directory_path}: {e}")
            return False
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """
        Get video information using yt-dlp.
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            Dict[str, Any]: Video information
        """
        try:
            cmd = ['yt-dlp', '--dump-json', '--no-download', url]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to get video info: {e.stderr}")
        except json.JSONDecodeError:
            raise Exception("Failed to parse video information")
    
    def download_video(self, video_config: Dict[str, str]) -> bool:
        """
        Download a single video based on configuration.
        
        Args:
            video_config (Dict[str, str]): Video configuration containing url, title, author, save_directory
            
        Returns:
            bool: True if download was successful, False otherwise
        """
        url = video_config['url']
        yaml_title = video_config['title']
        author = video_config['author']
        save_directory = video_config['save_directory']
        
        print(f"\nProcessing video: '{yaml_title}' (URL: {url})")
        
        try:
            # Get video information
            print("  Fetching video information...")
            video_info = self.get_video_info(url)
            actual_title = video_info.get('title', 'Unknown Title')
            uploader = video_info.get('uploader', 'Unknown Author')
            duration = video_info.get('duration', 0)
            
            print(f"  Video: '{actual_title}' by {uploader}")
            if duration:
                minutes, seconds = divmod(duration, 60)
                print(f"  Duration: {minutes:02d}:{seconds:02d}")
            
            # Create save directory if it doesn't exist
            if not self.create_directory(save_directory):
                print(f"Error processing video '{yaml_title}' (URL: {url}): Cannot create directory")
                print(f"Skipping video '{yaml_title}' due to error.")
                return False
            
            print(f"  Downloading to: {save_directory}")
            
            # Build yt-dlp command
            cmd = [
                'yt-dlp',
                '--format', 'best[height<=1080]',  # Download best quality up to 1080p
                '--output', os.path.join(save_directory, '%(title)s.%(ext)s'),
                '--no-playlist',  # Only download single video even if URL is part of playlist
                '--embed-subs',   # Embed subtitles if available
                '--write-auto-sub',  # Write auto-generated subtitles
                url
            ]
            
            # Execute download
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Find the downloaded file
                output_lines = result.stdout.split('\n')
                downloaded_file = None
                for line in output_lines:
                    if 'has already been downloaded' in line or 'Destination:' in line:
                        # Extract filename from yt-dlp output
                        if 'Destination:' in line:
                            downloaded_file = line.split('Destination:')[1].strip()
                        break
                
                if not downloaded_file:
                    # Try to construct expected filename
                    safe_title = "".join(c for c in actual_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    downloaded_file = os.path.join(save_directory, f"{safe_title}.mp4")
                
                print(f"  Successfully downloaded '{actual_title}' to '{save_directory}'")
                return True
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error occurred"
                print(f"Error processing video '{yaml_title}' (URL: {url}): {error_msg}")
                print(f"Skipping video '{yaml_title}' due to error.")
                return False
                
        except Exception as e:
            error_msg = str(e)
            print(f"Error processing video '{yaml_title}' (URL: {url}): {error_msg}")
            print(f"Skipping video '{yaml_title}' due to error.")
            return False
    
    def download_batch(self, config_path: str) -> None:
        """
        Download all videos specified in the configuration file.
        
        Args:
            config_path (str): Path to the YAML configuration file
        """
        try:
            # Load and validate configuration
            config = self.load_config(config_path)
            
            # Process each video
            for video_config in config['videos']:
                if self.download_video(video_config):
                    self.success_count += 1
                else:
                    self.error_count += 1
            
            # Print summary
            print(f"\nBatch download process completed.")
            print(f"Successfully downloaded: {self.success_count}/{self.total_videos} videos")
            if self.error_count > 0:
                print(f"Failed downloads: {self.error_count}/{self.total_videos} videos")
            
        except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
            print(f"Configuration error: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print(f"\nDownload interrupted by user")
            print(f"Downloaded: {self.success_count}/{self.total_videos} videos before interruption")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)


def print_usage():
    """Print usage instructions."""
    print("Usage: python get_video.py <path_to_yaml_config>")
    print("\nExample:")
    print("  python get_video.py videos_config.yaml")
    print("  python get_video.py /path/to/config/my_videos.yaml")
    print("\nRequired dependencies:")
    print("  pip install yt-dlp PyYAML")
    print("\nYAML Configuration Format:")
    print("""
videos:
  - url: https://www.youtube.com/watch?v=video1_id
    title: Learning Python Basics
    author: CodeMaster
    save_directory: /home/user/Videos/PythonTutorials

  - url: https://www.youtube.com/watch?v=video2_id
    title: Advanced Data Structures
    author: AlgoExpert
    save_directory: /home/user/Videos/ComputerScience/DataStructures
""")


def main():
    """Main function to handle command-line execution."""
    # Check for correct number of arguments
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments")
        print_usage()
        sys.exit(1)
    
    # Check for help flags
    if sys.argv[1] in ['-h', '--help', 'help']:
        print_usage()
        sys.exit(0)
    
    config_path = sys.argv[1]
    
    # Create downloader instance and start batch download
    downloader = YouTubeDownloader()
    downloader.download_batch(config_path)


if __name__ == "__main__":
    main()