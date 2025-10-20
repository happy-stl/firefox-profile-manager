# Firefox Profile Manager

A beautiful and responsive GUI application for managing Firefox profiles. This tool allows you to easily create, rename, delete, and launch Firefox profiles with a modern interface built using Python's built-in tkinter library.

## Features

- 🎨 **Modern GUI** - Clean, responsive interface with modern styling
- ➕ **Create Profiles** - Easily create new Firefox profiles with custom names
- ✏️ **Rename Profiles** - Change profile names without losing data
- 🗑️ **Delete Profiles** - Safely remove profiles and their data
- 🚀 **Launch Profiles** - Start Firefox with specific profiles
- 🔄 **Refresh** - Update the profile list in real-time
- 📱 **Desktop Integration** - Install as a desktop application launcher

## Requirements

- **Python 3.6+** - The application uses only built-in Python libraries
- **Firefox** - Must be installed and accessible from your PATH
- **Linux Desktop Environment** - For desktop launcher integration (GNOME, KDE, XFCE, etc.)

## Installation

### Quick Install

1. **Clone or download** this repository:
   ```bash
   git clone https://github.com/happy-stl/firefox-profile-manager.git
   cd firefox-profile-manager
   ```

2. **Make the install script executable**:
   ```bash
   chmod +x install-firefox-profile-manager.sh
   ```

3. **Run the installer**:
   ```bash
   ./install-firefox-profile-manager.sh
   ```

The installer will:
- Copy the Python script to `~/.local/bin/firefox-profiles`
- Create a desktop launcher in your applications menu
- Make the script executable
- Update your desktop database

## Usage

### Launching the Application

After installation, you can launch the Firefox Profile Manager in several ways:

1. **From Applications Menu** - Look for "Firefox Profile Manager" in your desktop environment's application menu
2. **From Terminal** - Run `firefox-profiles` or `python3 firefox_profile_manager.py`
3. **From File Manager** - Double-click the `firefox_profile_manager.py` file

### Managing Profiles

1. **View Profiles** - The main window shows all your Firefox profiles with their names, paths, and creation dates
2. **Create New Profile** - Click "➕ Create Profile" and enter a name
3. **Launch Profile** - Select a profile and click "🚀 Launch Profile" to start Firefox with that profile
4. **Rename Profile** - Select a profile and click "✏️ Rename" to change its name
5. **Delete Profile** - Select a profile and click "🗑️ Delete" to remove it permanently
6. **Refresh List** - Click "🔄 Refresh" to update the profile list

### Profile Names

Profile names can contain:
- Letters (a-z, A-Z)
- Numbers (0-9)
- Spaces
- Hyphens (-)
- Underscores (_)

## Uninstallation

To remove the Firefox Profile Manager:

```bash
rm ~/.local/bin/firefox-profiles
rm ~/.local/share/applications/firefox-profile-manager.desktop
update-desktop-database ~/.local/share/applications
```

## How It Works

The Firefox Profile Manager works by:

1. **Reading Firefox Configuration** - Parses `~/.mozilla/firefox/profiles.ini` to discover existing profiles
2. **Managing Profile Data** - Creates, modifies, and deletes profile directories and configuration entries
3. **Launching Firefox** - Uses the `firefox -P <profile-name>` command to start Firefox with specific profiles
4. **Desktop Integration** - Provides a desktop launcher for easy access from your applications menu

## File Locations

- **Firefox Profiles**: `~/.mozilla/firefox/`
- **Installed Script**: `~/.local/bin/firefox-profiles`
- **Desktop Launcher**: `~/.local/share/applications/firefox-profile-manager.desktop`

## Troubleshooting

### Firefox Not Found
If you get a "Firefox not found" error:
- Make sure Firefox is installed: `which firefox`
- Add Firefox to your PATH if it's installed in a non-standard location

### Permission Denied
If you get permission errors:
- Make sure the install script is executable: `chmod +x install-firefox-profile-manager.sh`
- Check that you have write permissions to `~/.local/bin` and `~/.local/share/applications`

### Desktop Launcher Not Appearing
If the application doesn't appear in your applications menu:
- Run: `update-desktop-database ~/.local/share/applications`
- Log out and log back in to refresh the desktop environment
- Check that your desktop environment supports `.desktop` files

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Created by Happy STL - A simple, elegant solution for managing Firefox profiles on Linux.
