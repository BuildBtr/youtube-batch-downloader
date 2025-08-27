# Fix Video+Audio Download Issue - Execution Plan

## Problem Statement
Videos downloaded using `get_video.py` are audio-only (no visual content) due to incorrect yt-dlp format selection. The issue affects long videos like the 3.5-hour GamersNexus video in `my_videos7.yaml`.

## Root Cause Analysis
- Current format string: `'best[height<=1080]'` in `get_video.py:189`
- This can select video-only streams without ensuring audio is merged
- YouTube uses adaptive streaming with separate video/audio tracks for long content
- No explicit merge format specified

## Solution Overview
Update yt-dlp format selection to ensure video+audio streams are properly merged into playable files.

## Execution Plan

### Phase 1: Analysis & Research
**Task 1**: Analyze current yt-dlp format selection causing audio-only downloads
- Review `get_video.py:187-195` format command construction
- Identify why `best[height<=1080]` fails for video+audio

**Task 2**: Research optimal yt-dlp format strings for video+audio downloads
- Test format strings that ensure video+audio merge
- Research best practices for long video downloads

### Phase 2: Code Implementation
**Task 3**: Update format selection in get_video.py to ensure video+audio merge
- Replace `'best[height<=1080]'` with proper format string
- Target format: `'best[height<=1080][ext=mp4]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best'`

**Task 4**: Add format fallback options and merge settings for long videos
- Add `--merge-output-format mp4` parameter
- Include additional fallback options for edge cases

### Phase 3: Documentation Updates
**Task 5**: Update documentation with format fix details
- Update README.md section on yt-dlp download settings (lines 227-241)
- Update get_video_docs.md with technical details
- Update CLAUDE.md with new format selection info

**Task 6**: Save execution plan to Prompt folder
- Document the complete fix process for future reference

### Phase 4: Testing & Validation
**Task 7**: Test updated script with my_videos7.yaml (3.5 hour GamersNexus video)
- Run: `python get_video.py Files/Files_In/my_videos7.yaml`
- Monitor download process for proper video+audio handling

**Task 8**: Verify downloaded video has both video and audio tracks
- Check file properties to confirm video+audio streams
- Test playback to ensure visual content is present

### Phase 5: Quality Assurance & Deployment
**Task 9**: Run any existing linting/type checking if available
- Check for Python linting tools in project
- Ensure code quality standards are maintained

**Task 10**: Create git commit with the video+audio fix
- Descriptive commit message explaining the format fix
- Include all modified files

**Task 11**: Push changes to GitHub repository
- Deploy the fix to the remote repository

## Expected Changes

### Code Changes
```python
# Before (get_video.py:189)
'--format', 'best[height<=1080]'

# After
'--format', 'best[height<=1080][ext=mp4]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
'--merge-output-format', 'mp4'
```

### Documentation Updates
- README.md: Update yt-dlp configuration section
- CLAUDE.md: Update format selection guidance
- get_video_docs.md: Add technical details about the fix

## Success Criteria
1. Downloaded videos contain both video and audio tracks
2. Long videos (3+ hours) download successfully with visual content
3. Playback shows video content, not just audio
4. All documentation reflects the changes
5. Changes are committed and pushed to GitHub

## Test Case
- Configuration: `Files/Files_In/my_videos7.yaml`
- Video: GamersNexus "THE NVIDIA AI GPU BLACK MARKET Investigation" (3.5 hours)
- Expected: Full video+audio download with visual content playable

## Rollback Plan
If issues arise, revert to original format string and investigate alternative solutions.

---
**Created**: August 26, 2025
**Status**: Ready for execution
**Priority**: High - Fixes core functionality issue