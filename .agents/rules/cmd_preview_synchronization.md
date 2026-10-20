# CMD Output & Social Preview Synchronization Rule

This is a workspace-local rule for the `run-9router` repository.

## 1. Mandatory Text & Image Synchronization
Whenever code or terminal output messages are modified in:
- `9Router.cmd`
- `auto-mitm.js`
- Any related startup, verification, or runner scripts

You **MUST** perform the following synchronization actions immediately:
1. **Update `generate_social_preview.py`**:
   - Update the `.cmd-body` HTML content inside `generate_social_preview.py` so that the displayed terminal lines, prompt, step indicators, status labels, and closing messages match the runtime script output **100% identically character-by-character**.
2. **Re-render `social-preview.png`**:
   - Execute `python generate_social_preview.py` to regenerate `social-preview.png` with the updated console output.
3. **Verify Generated Image**:
   - Ensure the image rendered correctly at `1280x640` resolution without text clipping or unintended wrapping.

## 2. Mandatory User Notification & Reminder
Whenever `social-preview.png` is updated due to code or console changes, you **MUST ALWAYS explicitly notify and remind the user** in your final response:
- Remind the user to upload/update the new `social-preview.png` on the GitHub repository settings page:
  `GitHub Repository -> Settings -> General -> Social preview`
