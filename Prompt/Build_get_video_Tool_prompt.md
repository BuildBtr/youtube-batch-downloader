Hello! Please act as a senior automation script programmer specializing in developing Python automations for use in the CLI. 

Today, I need you to build a script named "get_video.py" based on the following PRD:

Okay, that's a clear and well-structured YAML format!

I will now update the Product Requirements Document to reflect this specific YAML structure.

---

## Product Requirements Document: "get_video.py"

### 1. Introduction
This document outlines the requirements for the "get_video.py" Python script that allows users to download YouTube videos. The script will take input from a YAML configuration file specifying multiple videos to download, their metadata, and target download directories. This project builds upon a simpler concept of a YouTube downloader that takes a single URL via command-line.

### 2. Goals
* To create a Python script that can download multiple YouTube videos as specified in a YAML configuration file.
* To allow users to specify output directories for downloaded videos.
* To automatically create download directories if they do not exist.
* To provide a user-friendly command-line interface for script execution.
* To utilize the `pytube` library for interacting with YouTube.

### 3. Target User
Individuals who need to download multiple YouTube videos efficiently and organize them into specific folders. This could include researchers, educators, content creators, or general users archiving videos.

### 4. Functional Requirements

#### 4.1. Video Downloading
* The script **must** be able to download YouTube videos given their URLs.
* The script **must** download the highest resolution available for each video.
* The script **must** support batch downloading of multiple videos specified in the input YAML file.

#### 4.2. Input Configuration File (YAML)
* The script **must** accept a path to a YAML input configuration file as a command-line argument.
* The YAML file **must** have a top-level key named `videos`.
* The value of the `videos` key **must** be a list of video entries.
* Each video entry in the list **must** be a dictionary containing the following keys:
    * `url`: (String) The full URL of the YouTube video (e.g., "[https://www.youtube.com/watch?v=your_video_id](https://www.youtube.com/watch?v=your_video_id)").
    * `title`: (String) The title of the video (primarily for user reference and logging; the script may also use `pytube` to fetch the title).
    * `author`: (String) The author or channel name of the video (primarily for user reference and logging).
    * `save_directory`: (String) The specified folder path where the video should be saved.
* **Example YAML Structure:**
    ```yaml
    videos:
      - url: https://www.youtube.com/watch?v=video1_id
        title: Learning Python Basics
        author: CodeMaster
        save_directory: /home/user/Videos/PythonTutorials

      - url: https://www.youtube.com/watch?v=video2_id
        title: Advanced Data Structures
        author: AlgoExpert
        save_directory: /home/user/Videos/ComputerScience/DataStructures
    ```
* The script **must** correctly parse this YAML structure to retrieve the video details for processing.

#### 4.3. Directory Management
* The script **must** save the downloaded video to the `save_directory` specified for that video in the input YAML file.
* If the specified `save_directory` does not exist, the script **must** automatically create it (including any necessary parent directories).

#### 4.4. Command-Line Interface (CLI)
* The script **must** be executable from the command line.
* The script **must** accept a single argument: the absolute or relative path to the input YAML configuration file.
    * Example usage: `python your_script_name.py "/path/to/your/config_file.yaml"` or `python your_script_name.py "configs/my_videos.yaml"`

#### 4.5. Error Handling
* The script **should** provide informative error messages if:
    * The input YAML file is not found, is not valid YAML, or does not conform to the expected structure.
    * A video `url` is invalid, the video is unavailable, or `pytube` cannot process it.
    * A download fails for any reason (e.g., network issue, disk full).
    * There are issues creating a directory (e.g., insufficient permissions).
* The script **should** attempt to continue downloading other videos in the `videos` list if one video entry causes an error.

#### 4.6. Feedback
* The script **should** provide clear feedback to the user during operation, such as:
    * "Reading configuration from: [file_path]"
    * "Processing video: '[title specified in YAML]' (URL: [url])"
    * "Attempting to download '[fetched video title from pytube]'..."
    * "Creating directory: [save_directory]"
    * "Successfully downloaded '[fetched video title]' to '[save_directory/filename]'"
    * "Error processing video '[title specified in YAML]' (URL: [url]): [Error message]"
    * "Skipping video '[title specified in YAML]' due to error."
    * "Batch download process completed."

### 5. Non-Functional Requirements
* **Usability**: The script should be easy to use with clear instructions for creating the YAML configuration file and running the script.
* **Reliability**: The script should reliably download videos and handle common errors gracefully.
* **Performance**: Downloads should be performed efficiently. For batch operations, sequential downloading of videos is acceptable.
* **Maintainability**: The code should be well-structured, commented, and easy to understand for future modifications. Pythonic best practices should be followed.

### 6. Technical Specifications (Recommendations)
* **Language**: Python 3.x
* **Key Libraries**:
    * `pytube`: For interfacing with YouTube and downloading videos.
    * `sys` or `argparse`: For command-line argument parsing.
    * `PyYAML` (or a similar YAML parsing library): For parsing the YAML configuration file.
    * `os`: For directory and file path manipulations (e.g., `os.makedirs`, `os.path.join`, `os.path.exists`).
---


The script would report its success by printing the above results in the CLI or report its failure back to the user in the CLI.