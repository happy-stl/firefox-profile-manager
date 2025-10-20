#!/bin/bash
# Firefox Profile Manager Desktop Launcher Installer

set -eou pipefail

echo "Installing Firefox Profile Manager..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd "$SCRIPT_DIR" 2>&1 >/dev/null

# Installation directories
INSTALL_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

# Installation files
INSTALL_FILE="$INSTALL_DIR/firefox-profiles"
DESKTOP_FILE="$DESKTOP_DIR/firefox-profile-manager.desktop"

echo "Installing from: $SCRIPT_DIR"
echo "Installing to: $INSTALL_DIR"

# Create directories if they don't exist
mkdir -p "$SCRIPT_DIR"
mkdir -p "$DESKTOP_DIR"

# Copy the main Python script to current directory
if [ -f "firefox_profile_manager.py" ]; then
    cp -v "firefox_profile_manager.py" "$INSTALL_FILE"
    chmod +x "$INSTALL_FILE"
    echo "✅ Copied firefox_profile_manager.py to current directory"
else
    echo "❌ Error: firefox_profile_manager.py not found in script directory"
    exit 1
fi

# Update desktop file to point to the current directory
if [ -f "firefox-profile-manager.desktop" ]; then
    # Copy desktop file and update the Exec path
    cp -v "firefox-profile-manager.desktop" "$DESKTOP_FILE"
    chmod +x "$DESKTOP_FILE"
    # Update the Exec path to point to the current directory
    sed -i "s|Exec=python3 {{INSTALL_FILE}}|Exec=python3 $INSTALL_FILE|g" "$DESKTOP_FILE"
    # Update the Path as well
    sed -i "s|Path={{INSTALL_DIR}}|Path=$INSTALL_DIR|g" "$DESKTOP_FILE"
    echo "✅ Created desktop file for current directory"
else
    echo "❌ Error: firefox-profile-manager.desktop not found in script directory"
    exit 1
fi

# Update desktop database
update-desktop-database "$DESKTOP_DIR"

echo ""
echo "✅ Firefox Profile Manager installed successfully!"
echo "📁 Files installed in: $INSTALL_DIR"
echo "🖥️  Desktop launcher installed in applications menu"
echo ""
echo "You can now:"
echo "  • Run: firefox_profile_manager.py"
echo "  • Run: ./firefox-profiles"
echo "  • Find 'Firefox Profile Manager' in your applications menu"
echo ""
echo "To uninstall, run:"
echo "  rm '$INSTALL_FILE'"
echo "  rm '$DESKTOP_FILE'"
echo "  update-desktop-database '$DESKTOP_DIR'"
