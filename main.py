#!/usr/bin/env python3
"""
SiteTester GUI - Playwright Script Manager
Professional GUI application for managing and executing Playwright scripts.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import sys
import os
import venv
import threading
import datetime
from pathlib import Path
import json


class SiteTesterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SiteTester - Playwright Script Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Set minimum window size
        self.root.minsize(600, 800)
        
        # Initialize paths
        self.project_root = Path(__file__).parent
        self.scripts_dir = self.project_root / "scripts"
        self.logs_dir = self.project_root / "logs"
        self.venv_dir = self.project_root / "venv"
        
        # Create logs directory if it doesn't exist
        self.logs_dir.mkdir(exist_ok=True)
        
        # Initialize variables
        self.available_scripts = []
        self.selected_script = tk.StringVar()
        self.is_running = False
        
        # Setup UI
        self.setup_ui()
        
        # Check environment and load scripts
        self.check_environment()
        self.load_scripts()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Playwright Script Manager", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Script selection frame
        selection_frame = ttk.LabelFrame(main_frame, text="Script Selection", padding="15")
        selection_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Script dropdown
        script_label = ttk.Label(selection_frame, text="Select Script:", 
                                font=("SF Pro Display", 12, "normal") if sys.platform == "darwin" else ("Segoe UI", 12, "normal"))
        script_label.pack(anchor=tk.W)
        
        self.script_combo = ttk.Combobox(selection_frame, textvariable=self.selected_script,
                                        state="readonly", width=50,
                                        font=("SF Pro Display", 11) if sys.platform == "darwin" else ("Segoe UI", 11))
        self.script_combo.pack(fill=tk.X, pady=(5, 10))
        
        # Control buttons frame
        button_frame = ttk.Frame(selection_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Create button container for better alignment
        button_container = ttk.Frame(button_frame)
        button_container.pack(anchor=tk.W)
        
        self.start_button = ttk.Button(button_container, text="Start Script", 
                                      command=self.start_script, style="Action.TButton")
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.refresh_button = ttk.Button(button_container, text="Refresh Scripts", 
                                        command=self.load_scripts, style="Action.TButton")
        self.refresh_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_container, text="Stop Script", 
                                     command=self.stop_script, state=tk.DISABLED, style="Stop.TButton")
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.record_button = ttk.Button(button_container, text="🔴 Neem nieuw script op", 
                                       command=self.record_new_script, style="Record.TButton")
        self.record_button.pack(side=tk.LEFT)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="15")
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_label = ttk.Label(status_frame, text="Ready", 
                                     foreground="#34C759", 
                                     font=("SF Pro Display", 12, "bold") if sys.platform == "darwin" else ("Segoe UI", 12, "bold"))
        self.status_label.pack(anchor=tk.W)
        
        # Log output frame
        log_frame = ttk.LabelFrame(main_frame, text="Script Output", padding="15")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log text area with scrollbar
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, 
                                                 font=("Monaco", 11), 
                                                 bg="#1e1e1e", fg="#ffffff",
                                                 insertbackground="white")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Clear log button
        clear_button_frame = ttk.Frame(log_frame)
        clear_button_frame.pack(fill=tk.X, pady=(15, 0))
        
        clear_button = ttk.Button(clear_button_frame, text="Clear Log", 
                                 command=self.clear_log, style="Action.TButton")
        clear_button.pack(anchor=tk.W)
        
        # Configure professional styles
        style = ttk.Style()
        
        # Configure fonts for better readability
        button_font = ("SF Pro Display", 11, "normal") if sys.platform == "darwin" else ("Segoe UI", 11, "normal")
        title_font = ("SF Pro Display", 16, "bold") if sys.platform == "darwin" else ("Segoe UI", 16, "bold")
        
        # Action buttons (primary actions)
        style.configure("Action.TButton", 
                       font=button_font,
                       padding=(16, 10),
                       background="#007AFF" if sys.platform == "darwin" else "#0078D4",
                       foreground="white")
        
        # Record button (special action with red indicator)
        style.configure("Record.TButton", 
                       font=button_font,
                       padding=(16, 10),
                       background="#FF3B30" if sys.platform == "darwin" else "#D83B01",
                       foreground="white")
        
        # Stop button (warning action)
        style.configure("Stop.TButton", 
                       font=button_font,
                       padding=(16, 10),
                       background="#FF9500" if sys.platform == "darwin" else "#FF8C00",
                       foreground="white")
        
        # Dialog buttons
        style.configure("DialogCancel.TButton", 
                       font=button_font,
                       padding=(14, 8),
                       background="#F2F2F7" if sys.platform == "darwin" else "#F3F2F1",
                       foreground="#1D1D1F" if sys.platform == "darwin" else "#323130")
        
        style.configure("DialogRecord.TButton", 
                       font=button_font,
                       padding=(14, 8),
                       background="#FF3B30" if sys.platform == "darwin" else "#D83B01",
                       foreground="white")
        
        # Update title font
        title_label.configure(font=title_font)
    
    def check_environment(self):
        """Check and setup virtual environment"""
        self.update_status("Checking environment...", "orange")
        
        if not self.venv_dir.exists():
            self.log_message("Virtual environment not found. Creating...")
            threading.Thread(target=self.setup_environment, daemon=True).start()
        else:
            self.log_message("Virtual environment found.")
            self.update_status("Environment ready", "green")
    
    def setup_environment(self):
        """Setup virtual environment and install dependencies"""
        try:
            # Create virtual environment
            self.log_message("Creating virtual environment...")
            venv.create(self.venv_dir, with_pip=True)
            
            # Install dependencies
            self.log_message("Installing dependencies...")
            
            # Get pip path
            if sys.platform == "win32":
                pip_path = self.venv_dir / "Scripts" / "pip"
                python_path = self.venv_dir / "Scripts" / "python"
            else:
                pip_path = self.venv_dir / "bin" / "pip"
                python_path = self.venv_dir / "bin" / "python"
            
            # Install packages
            packages = ["playwright", "rich"]
            for package in packages:
                self.log_message(f"Installing {package}...")
                result = subprocess.run([str(pip_path), "install", package], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    self.log_message(f"Error installing {package}: {result.stderr}")
                    return
            
            # Install Playwright browsers
            self.log_message("Installing Playwright browsers...")
            result = subprocess.run([str(python_path), "-m", "playwright", "install"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_message("Environment setup completed successfully!")
                self.update_status("Environment ready", "green")
            else:
                self.log_message(f"Error installing Playwright browsers: {result.stderr}")
                self.update_status("Environment setup failed", "red")
                
        except Exception as e:
            self.log_message(f"Error setting up environment: {str(e)}")
            self.update_status("Environment setup failed", "red")
    
    def load_scripts(self):
        """Load available scripts from scripts directory"""
        self.available_scripts = []
        
        if not self.scripts_dir.exists():
            self.log_message("Scripts directory not found!")
            return
        
        # Find all Python files in scripts directory
        for script_file in self.scripts_dir.glob("*.py"):
            script_name = script_file.stem  # Filename without extension
            self.available_scripts.append(script_name)
        
        # Update combobox
        self.script_combo['values'] = self.available_scripts
        
        if self.available_scripts:
            self.script_combo.current(0)  # Select first script
            self.log_message(f"Found {len(self.available_scripts)} scripts")
        else:
            self.log_message("No Python scripts found in scripts directory")
    
    def start_script(self):
        """Start the selected script"""
        if not self.selected_script.get():
            messagebox.showwarning("Warning", "Please select a script first")
            return
        
        if self.is_running:
            messagebox.showwarning("Warning", "A script is already running")
            return
        
        if not self.venv_dir.exists():
            messagebox.showerror("Error", "Virtual environment not found. Please wait for setup to complete.")
            return
        
        # Start script in separate thread
        script_name = self.selected_script.get()
        threading.Thread(target=self.execute_script, args=(script_name,), daemon=True).start()
    
    def execute_script(self, script_name):
        """Execute the selected script"""
        self.is_running = True
        self.update_ui_running_state(True)
        
        script_path = self.scripts_dir / f"{script_name}.py"
        
        # Create log file
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        log_file = self.logs_dir / f"{script_name}_{timestamp}.txt"
        
        try:
            self.update_status(f"Starting {script_name}...", "orange")
            self.log_message(f"Starting script: {script_name}")
            self.log_message(f"Log file: {log_file}")
            
            # Get Python path from venv
            if sys.platform == "win32":
                python_path = self.venv_dir / "Scripts" / "python"
            else:
                python_path = self.venv_dir / "bin" / "python"
            
            # Execute script
            with open(log_file, 'w') as f:
                self.process = subprocess.Popen(
                    [str(python_path), str(script_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Read output in real-time
                for line in iter(self.process.stdout.readline, ''):
                    if line:
                        line = line.strip()
                        self.log_message(line)
                        f.write(f"{datetime.datetime.now()}: {line}\n")
                        f.flush()
                
                # Wait for process to complete
                self.process.wait()
                
                if self.process.returncode == 0:
                    self.log_message(f"Script {script_name} completed successfully!")
                    self.update_status("Script completed", "green")
                else:
                    self.log_message(f"Script {script_name} failed with return code {self.process.returncode}")
                    self.update_status("Script failed", "red")
                    
        except Exception as e:
            self.log_message(f"Error executing script: {str(e)}")
            self.update_status("Execution error", "red")
            
        finally:
            self.is_running = False
            self.update_ui_running_state(False)
    
    def stop_script(self):
        """Stop the currently running script or recording"""
        stopped = False
        
        # Stop regular script execution
        if hasattr(self, 'process') and self.process:
            try:
                self.process.terminate()
                self.log_message("Script stopped by user")
                self.update_status("Script stopped", "orange")
                stopped = True
            except Exception as e:
                self.log_message(f"Error stopping script: {str(e)}")
        
        # Stop codegen recording
        if hasattr(self, 'codegen_process') and self.codegen_process:
            try:
                self.codegen_process.terminate()
                self.log_message("Recording stopped by user")
                self.update_status("Recording stopped", "orange")
                stopped = True
            except Exception as e:
                self.log_message(f"Error stopping recording: {str(e)}")
        
        if not stopped:
            self.log_message("No active process to stop")
    
    def update_ui_running_state(self, running):
        """Update UI elements based on running state"""
        if running:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.script_combo.config(state=tk.DISABLED)
            self.record_button.config(state=tk.DISABLED)
            self.refresh_button.config(state=tk.DISABLED)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.script_combo.config(state="readonly")
            self.record_button.config(state=tk.NORMAL)
            self.refresh_button.config(state=tk.NORMAL)
    
    def update_status(self, message, color="black"):
        """Update status label"""
        # Modern color scheme
        color_map = {
            "green": "#34C759",
            "orange": "#FF9500", 
            "red": "#FF3B30",
            "black": "#1D1D1F" if sys.platform == "darwin" else "#323130"
        }
        actual_color = color_map.get(color, color)
        self.status_label.config(text=message, foreground=actual_color)
    
    def log_message(self, message):
        """Add message to log output"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Thread-safe GUI update
        self.root.after(0, lambda: self._append_to_log(formatted_message))
    
    def _append_to_log(self, message):
        """Append message to log text widget (thread-safe)"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """Clear the log output"""
        self.log_text.delete(1.0, tk.END)
    
    def record_new_script(self):
        """Start recording a new Playwright script"""
        if self.is_running:
            messagebox.showwarning("Warning", "A script is already running. Please wait for it to complete.")
            return
        
        if not self.venv_dir.exists():
            messagebox.showerror("Error", "Virtual environment not found. Please wait for setup to complete.")
            return
        
        # Create dialog for script details
        dialog = ScriptRecordDialog(self.root, self.record_script_callback)
    
    def record_script_callback(self, script_name, start_url):
        """Callback function to start script recording"""
        if not script_name:
            return
        
        # Start recording in separate thread
        threading.Thread(target=self.execute_playwright_codegen, 
                        args=(script_name, start_url), daemon=True).start()
    
    def execute_playwright_codegen(self, script_name, start_url):
        """Execute playwright codegen to record a new script"""
        self.is_running = True
        self.update_ui_running_state(True)
        
        try:
            self.update_status(f"Recording script: {script_name}...", "orange")
            self.log_message(f"Starting Playwright codegen for: {script_name}")
            self.log_message(f"Starting URL: {start_url}")
            
            # Get Python path from venv
            if sys.platform == "win32":
                python_path = self.venv_dir / "Scripts" / "python"
            else:
                python_path = self.venv_dir / "bin" / "python"
            
            # Create temporary file for the generated script
            temp_script_file = self.project_root / f"{script_name}_temp.py"
            
            # Execute playwright codegen
            cmd = [
                str(python_path), "-m", "playwright", "codegen",
                "--output", str(temp_script_file),
                start_url
            ]
            
            self.log_message("Playwright codegen started. Close the browser when finished recording.")
            
            # Run codegen and wait for completion
            self.codegen_process = subprocess.Popen(cmd, 
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   text=True)
            
            # Wait for process to complete
            stdout, stderr = self.codegen_process.communicate()
            
            if self.codegen_process.returncode == 0:
                self.log_message("Recording completed successfully!")
                
                # Check if temp file was created and has content
                if temp_script_file.exists() and temp_script_file.stat().st_size > 0:
                    # Ask user if they want to save the script
                    self.root.after(0, lambda: self.save_recorded_script(script_name, temp_script_file))
                else:
                    self.log_message("No script was generated. Recording may have been cancelled.")
                    self.update_status("Recording cancelled", "orange")
            else:
                self.log_message(f"Recording failed: {stderr}")
                self.update_status("Recording failed", "red")
                
        except Exception as e:
            self.log_message(f"Error during recording: {str(e)}")
            self.update_status("Recording error", "red")
            
        finally:
            self.is_running = False
            self.update_ui_running_state(False)
    
    def save_recorded_script(self, script_name, temp_file):
        """Ask user to save the recorded script and handle the saving"""
        try:
            # Show dialog asking if user wants to save
            result = messagebox.askyesno(
                "Save Recorded Script", 
                f"Recording completed!\n\nDo you want to save the script as '{script_name}.py'?",
                icon="question"
            )
            
            if result:
                # Move temp file to scripts directory
                final_script_path = self.scripts_dir / f"{script_name}.py"
                
                # Read content from temp file and write to final location
                with open(temp_file, 'r', encoding='utf-8') as temp_f:
                    script_content = temp_f.read()
                
                with open(final_script_path, 'w', encoding='utf-8') as final_f:
                    final_f.write(script_content)
                
                self.log_message(f"Script saved as: {final_script_path}")
                self.update_status("Script saved successfully", "green")
                
                # Refresh script list
                self.load_scripts()
                
                # Select the new script
                if script_name in self.available_scripts:
                    self.selected_script.set(script_name)
                    self.log_message(f"New script '{script_name}' is now selected")
            else:
                self.log_message("Script recording discarded by user")
                self.update_status("Recording discarded", "orange")
                
        except Exception as e:
            self.log_message(f"Error saving script: {str(e)}")
            self.update_status("Save error", "red")
        
        finally:
            # Clean up temp file
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception as e:
                    self.log_message(f"Warning: Could not delete temp file: {e}")


class ScriptRecordDialog:
    """Dialog for entering new script recording details"""
    
    def __init__(self, parent, callback):
        self.result = None
        self.callback = callback
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Neem nieuw script op")
        self.dialog.geometry("420x360")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog on parent window
        parent.update_idletasks()  # Make sure parent geometry is updated
        
        # Calculate center position
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        dialog_width = 420
        dialog_height = 360
        
        center_x = parent_x + (parent_width - dialog_width) // 2
        center_y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{center_x}+{center_y}")
        
        self.setup_dialog()
        
        # Focus on script name entry
        self.script_name_entry.focus_set()
    
    def setup_dialog(self):
        """Setup the dialog interface"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Fonts for dialog
        dialog_title_font = ("SF Pro Display", 14, "bold") if sys.platform == "darwin" else ("Segoe UI", 14, "bold")
        dialog_label_font = ("SF Pro Display", 11, "normal") if sys.platform == "darwin" else ("Segoe UI", 11, "normal")
        dialog_entry_font = ("SF Pro Display", 11) if sys.platform == "darwin" else ("Segoe UI", 11)
        dialog_instruction_font = ("SF Pro Display", 10) if sys.platform == "darwin" else ("Segoe UI", 10)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔴 Nieuw Playwright Script Opnemen", 
                               font=dialog_title_font)
        title_label.pack(pady=(0, 20))
        
        # Script name
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(name_frame, text="Script naam:", font=dialog_label_font).pack(anchor=tk.W)
        self.script_name_entry = ttk.Entry(name_frame, width=40, font=dialog_entry_font)
        self.script_name_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Starting URL
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(url_frame, text="Start URL:", font=dialog_label_font).pack(anchor=tk.W)
        self.start_url_entry = ttk.Entry(url_frame, width=40, font=dialog_entry_font)
        self.start_url_entry.pack(fill=tk.X, pady=(5, 0))
        self.start_url_entry.insert(0, "https://example.com")
        
        # Instructions
        instructions = ttk.Label(main_frame, 
                               text="De Playwright browser zal openen. Voer je acties uit en sluit\nde browser wanneer je klaar bent met opnemen.",
                               justify=tk.CENTER, foreground="#8E8E93",
                               font=dialog_instruction_font)
        instructions.pack(pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Dialog button styling
        dialog_button_font = ("SF Pro Display", 11, "normal") if sys.platform == "darwin" else ("Segoe UI", 11, "normal")
        
        # Center the buttons with better spacing
        button_container = ttk.Frame(button_frame)
        button_container.pack(anchor=tk.CENTER)
        
        ttk.Button(button_container, text="🔴 Start Opname", 
                  command=self.start_recording, 
                  style="DialogRecord.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_container, text="Annuleren", 
                  command=self.cancel,
                  style="DialogCancel.TButton").pack(side=tk.LEFT)
        
        # Bind Enter key to start recording
        self.dialog.bind('<Return>', lambda e: self.start_recording())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    
    def start_recording(self):
        """Start the recording process"""
        script_name = self.script_name_entry.get().strip()
        start_url = self.start_url_entry.get().strip()
        
        if not script_name:
            messagebox.showwarning("Warning", "Voer een script naam in")
            self.script_name_entry.focus_set()
            return
        
        if not start_url:
            start_url = "https://example.com"
        
        # Validate script name (no spaces, special characters)
        if not script_name.replace('_', '').replace('-', '').isalnum():
            messagebox.showwarning("Warning", 
                                 "Script naam mag alleen letters, cijfers, '_' en '-' bevatten")
            self.script_name_entry.focus_set()
            return
        
        # Close dialog and start recording
        self.dialog.destroy()
        self.callback(script_name, start_url)
    
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = SiteTesterApp(root)
    
    # Handle window close
    def on_closing():
        if app.is_running:
            if messagebox.askokcancel("Quit", "A script is running. Do you want to quit anyway?"):
                if hasattr(app, 'process') and app.process:
                    app.process.terminate()
                if hasattr(app, 'codegen_process') and app.codegen_process:
                    app.codegen_process.terminate()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main() 