#!/usr/bin/env python3
"""
Firefox Profile Manager GUI
A beautiful and responsive GUI for managing Firefox profiles.
No external dependencies required - uses only Python's built-in tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import configparser
import subprocess
import shutil
from pathlib import Path
import json
import uuid
import time

class FirefoxProfileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Firefox Profile Manager")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Set modern styling
        self.setup_styles()
        
        # Firefox profile paths
        self.firefox_dir = Path.home() / ".mozilla" / "firefox"
        self.profiles_ini = self.firefox_dir / "profiles.ini"
        
        # Create main interface
        self.create_widgets()
        self.load_profiles()
        
        # Center window on screen
        self.center_window()
    
    def setup_styles(self):
        """Configure modern styling for the application"""
        style = ttk.Style()
        
        # Configure colors
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'danger': '#C73E1D',
            'light': '#F8F9FA',
            'dark': '#212529',
            'muted': '#6C757D'
        }
        
        # Configure styles
        style.theme_use('clam')
        
        # Main frame style
        style.configure('Main.TFrame', background=self.colors['light'])
        
        # Title style
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       foreground=self.colors['primary'],
                       background=self.colors['light'])
        
        # Button styles
        style.configure('Primary.TButton',
                       font=('Arial', 10, 'bold'),
                       foreground='white',
                       background=self.colors['primary'])
        
        style.configure('Success.TButton',
                       font=('Arial', 10, 'bold'),
                       foreground='white',
                       background=self.colors['success'])
        
        style.configure('Danger.TButton',
                       font=('Arial', 10, 'bold'),
                       foreground='white',
                       background=self.colors['danger'])
        
        # Treeview style
        style.configure('Treeview',
                       font=('Arial', 10),
                       rowheight=30,
                       background='white',
                       fieldbackground='white')
        
        style.configure('Treeview.Heading',
                       font=('Arial', 11, 'bold'),
                       background=self.colors['primary'],
                       foreground='white')
        
        # Configure hover effects
        style.map('Primary.TButton',
                 background=[('active', '#1e5f7a')])
        style.map('Success.TButton',
                 background=[('active', '#d67a00')])
        style.map('Danger.TButton',
                 background=[('active', '#a02d16')])
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Firefox Profile Manager", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Buttons
        self.refresh_btn = ttk.Button(control_frame, text="🔄 Refresh", 
                                    command=self.load_profiles, style='Primary.TButton')
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_btn = ttk.Button(control_frame, text="➕ Create Profile", 
                                   command=self.create_profile, style='Success.TButton')
        self.create_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.launch_btn = ttk.Button(control_frame, text="🚀 Launch Profile", 
                                   command=self.launch_profile, style='Primary.TButton')
        self.launch_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.rename_btn = ttk.Button(control_frame, text="✏️ Rename", 
                                   command=self.rename_profile, style='Primary.TButton')
        self.rename_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.delete_btn = ttk.Button(control_frame, text="🗑️ Delete", 
                                   command=self.delete_profile, style='Danger.TButton')
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Profiles list frame
        list_frame = ttk.LabelFrame(main_frame, text="Firefox Profiles", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for profiles
        columns = ('Name', 'Path', 'Default', 'Created')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configure columns
        self.tree.heading('Name', text='Profile Name')
        self.tree.heading('Path', text='Profile Path')
        self.tree.heading('Default', text='Default')
        self.tree.heading('Created', text='Created')
        
        self.tree.column('Name', width=200, minwidth=150)
        self.tree.column('Path', width=300, minwidth=200)
        self.tree.column('Default', width=80, minwidth=60)
        self.tree.column('Created', width=120, minwidth=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_profile_select)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              font=('Arial', 9), foreground=self.colors['muted'])
        status_bar.pack(pady=(10, 0))
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_profiles(self):
        """Load Firefox profiles from profiles.ini"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if not self.profiles_ini.exists():
                self.status_var.set("No Firefox profiles found")
                return
            
            # Parse profiles.ini
            config = configparser.ConfigParser()
            config.read(self.profiles_ini)
            
            profiles = []
            for section in config.sections():
                if section.startswith('Profile'):
                    profile_data = dict(config[section])
                    profile_data['section'] = section
                    profiles.append(profile_data)
            
            # Sort profiles by name
            profiles.sort(key=lambda x: x.get('Name', ''))
            
            # Add profiles to treeview
            for profile in profiles:
                name = profile.get('name', 'Unknown')
                path = profile.get('path', 'Unknown')
                is_relative = profile.get('isrelative', '1') == '1'
                is_default = profile.get('default', '0') == '1'
                default_text = '✓' if is_default else ''
                
                # Handle relative vs absolute paths
                if is_relative:
                    profile_path = self.firefox_dir / path
                else:
                    profile_path = Path(path)
                
                # Get creation date
                created = self.get_profile_creation_date(profile_path)
                
                # Display the actual profile directory name
                display_path = str(profile_path.name) if profile_path.exists() else path
                
                self.tree.insert('', 'end', values=(name, display_path, default_text, created))
            
            self.status_var.set(f"Loaded {len(profiles)} profile(s)")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load profiles: {str(e)}")
            self.status_var.set("Error loading profiles")
    
    def get_profile_creation_date(self, profile_path):
        """Get the creation date of a profile directory"""
        try:
            if profile_path.exists() and profile_path.is_dir():
                stat = profile_path.stat()
                return time.strftime('%Y-%m-%d', time.localtime(stat.st_ctime))
            return 'Unknown'
        except Exception as e:
            print(f"Error getting creation date for {profile_path}: {e}")
            return 'Unknown'
    
    def on_profile_select(self, event):
        """Handle profile selection"""
        selection = self.tree.selection()
        if selection:
            self.status_var.set("Profile selected")
        else:
            self.status_var.set("Ready")
    
    def get_selected_profile(self):
        """Get the currently selected profile"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a profile first.")
            return None
        
        item = self.tree.item(selection[0])
        return item['values']
    
    def create_profile(self):
        """Create a new Firefox profile"""
        # Get profile name
        name = simpledialog.askstring("Create Profile", "Enter profile name:")
        if not name:
            return
        
        # Validate name
        if not name.replace(' ', '').replace('-', '').replace('_', '').isalnum():
            messagebox.showerror("Invalid Name", "Profile name can only contain letters, numbers, spaces, hyphens, and underscores.")
            return
        
        try:
            # Generate unique profile ID
            profile_id = ''.join([str(uuid.uuid4()).replace('-', '')[:8] for _ in range(2)])
            profile_path = f"{profile_id}.{name.lower().replace(' ', '-')}"
            
            # Create profile directory
            full_path = self.firefox_dir / profile_path
            full_path.mkdir(exist_ok=True)
            
            # Create basic profile files
            self.create_profile_files(full_path, name)
            
            # Update profiles.ini
            self.add_profile_to_ini(name, profile_path)
            
            # Refresh the list
            self.load_profiles()
            
            messagebox.showinfo("Success", f"Profile '{name}' created successfully!")
            self.status_var.set(f"Created profile: {name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create profile: {str(e)}")
    
    def create_profile_files(self, profile_path, name):
        """Create basic files for a new profile"""
        # Create prefs.js
        prefs_js = profile_path / "prefs.js"
        with open(prefs_js, 'w') as f:
            f.write(f'// Firefox Profile: {name}\n')
            f.write('user_pref("browser.startup.page", 1);\n')
            f.write('user_pref("browser.startup.homepage", "about:blank");\n')
        
        # Create user.js (empty)
        user_js = profile_path / "user.js"
        user_js.touch()
        
        # Create times.json
        times_json = profile_path / "times.json"
        with open(times_json, 'w') as f:
            json.dump({
                "created": int(time.time() * 1000000),
                "reset": int(time.time() * 1000000)
            }, f)
    
    def add_profile_to_ini(self, name, path):
        """Add a new profile to profiles.ini"""
        config = configparser.ConfigParser()
        config.read(self.profiles_ini)
        
        # Find next profile number
        profile_numbers = []
        for section in config.sections():
            if section.startswith('Profile'):
                try:
                    num = int(section.replace('Profile', ''))
                    profile_numbers.append(num)
                except ValueError:
                    pass
        
        next_num = max(profile_numbers) + 1 if profile_numbers else 0
        
        # Add new profile
        section_name = f"Profile{next_num}"
        config[section_name] = {
            'Name': name,
            'IsRelative': '1',
            'Path': path
        }
        
        # Write back to file
        with open(self.profiles_ini, 'w') as f:
            config.write(f)
    
    def launch_profile(self):
        """Launch Firefox with the selected profile"""
        profile_data = self.get_selected_profile()
        if not profile_data:
            return
        
        name, path, _, _ = profile_data
        
        try:
            # Launch Firefox with the profile
            cmd = ['firefox', '-P', name, '--new-instance']
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            self.status_var.set(f"Launched profile: {name}")
            messagebox.showinfo("Success", f"Launching Firefox with profile '{name}'")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "Firefox not found. Please make sure Firefox is installed and in your PATH.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Firefox: {str(e)}")
    
    def rename_profile(self):
        """Rename the selected profile"""
        profile_data = self.get_selected_profile()
        if not profile_data:
            return
        
        old_name, path, is_default, _ = profile_data
        
        if is_default:
            messagebox.showwarning("Cannot Rename", "Cannot rename the default profile.")
            return
        
        # Get new name
        new_name = simpledialog.askstring("Rename Profile", f"Enter new name for '{old_name}':", initialvalue=old_name)
        if not new_name or new_name == old_name:
            return
        
        # Validate name
        if not new_name.replace(' ', '').replace('-', '').replace('_', '').isalnum():
            messagebox.showerror("Invalid Name", "Profile name can only contain letters, numbers, spaces, hyphens, and underscores.")
            return
        
        try:
            # Update profiles.ini
            config = configparser.ConfigParser()
            config.read(self.profiles_ini)
            
            # Find and update the profile
            for section in config.sections():
                if section.startswith('Profile'):
                    if config[section].get('Name') == old_name:
                        config[section]['Name'] = new_name
                        break
            
            # Write back to file
            with open(self.profiles_ini, 'w') as f:
                config.write(f)
            
            # Refresh the list
            self.load_profiles()
            
            messagebox.showinfo("Success", f"Profile renamed from '{old_name}' to '{new_name}'")
            self.status_var.set(f"Renamed profile: {old_name} → {new_name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename profile: {str(e)}")
    
    def delete_profile(self):
        """Delete the selected profile"""
        profile_data = self.get_selected_profile()
        if not profile_data:
            return
        
        name, path, is_default, _ = profile_data
        
        if is_default:
            messagebox.showwarning("Cannot Delete", "Cannot delete the default profile.")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete profile '{name}'?\n\n"
                                   f"This will permanently remove the profile and all its data.",
                                   icon='warning')
        if not result:
            return
        
        try:
            # Remove from profiles.ini
            config = configparser.ConfigParser()
            config.read(self.profiles_ini)
            
            # Find and remove the profile section
            section_to_remove = None
            for section in config.sections():
                if section.startswith('Profile'):
                    if config[section].get('Name') == name:
                        section_to_remove = section
                        break
            
            if section_to_remove:
                config.remove_section(section_to_remove)
            
            # Write back to file
            with open(self.profiles_ini, 'w') as f:
                config.write(f)
            
            # Remove profile directory
            profile_path = self.firefox_dir / path
            if profile_path.exists():
                shutil.rmtree(profile_path)
            
            # Refresh the list
            self.load_profiles()
            
            messagebox.showinfo("Success", f"Profile '{name}' deleted successfully")
            self.status_var.set(f"Deleted profile: {name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete profile: {str(e)}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = FirefoxProfileManager(root)
    
    # Handle window closing
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()