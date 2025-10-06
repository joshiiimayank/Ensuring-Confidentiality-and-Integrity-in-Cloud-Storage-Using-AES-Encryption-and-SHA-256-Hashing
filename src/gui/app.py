import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import threading
import os
import json
from src.backup.backup_runner import backup_all_files
from src.restore.restore_runner import restore_files

class BackupRestoreGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure Cloud Backup")
        self.geometry("400x200")
        
        self.config_data = None
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        if not self.aws_access_key or not self.aws_secret_key:
            messagebox.showerror("AWS Credentials Missing", "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
            self.destroy()
            return
        
        self.load_config()
        self.create_widgets()

    def load_config(self):
        with open("config/config.json") as f:
            self.config_data = json.load(f)

    def create_widgets(self):
        tk.Label(self, text="Secure Backup and Restore", font=("Arial", 16)).pack(pady=10)
        tk.Button(self, text="Backup Files...", command=self.select_and_backup_files).pack(pady=5)
        tk.Button(self, text="Restore Files...", command=self.restore_files_thread).pack(pady=5)
        self.status_label = tk.Label(self, text="", fg="blue")
        self.status_label.pack(pady=10)

    def select_and_backup_files(self):
        file_paths = filedialog.askopenfilenames(title="Select files to backup")
        if not file_paths:
            return
        
        # Temporarily override source_dir in config for selected files
        self.backup_selected_files(file_paths)

    def backup_selected_files(self, file_paths):
        def run_backup():
            try:
                self.update_status("Running backup...")
                # Create a temporary directory and copy selected files or override source_dir temporarily
                # For demo, override source_dir to dummy folder containing selected files
                # Here, for simplicity, backup all files from selected paths (simulate batch)
                
                # Create a temporary backup manifest for these files
                import tempfile
                import shutil

                with tempfile.TemporaryDirectory() as temp_dir:
                    for fp in file_paths:
                        # preserve relative path handling can be added if needed
                        shutil.copy(fp, os.path.join(temp_dir, os.path.basename(fp)))
                    self.config_data['backup']['source_dir'] = temp_dir
                    backup_all_files(self.config_data, self.aws_access_key, self.aws_secret_key)
                self.update_status("Backup completed.")
                messagebox.showinfo("Success", "Backup completed successfully.")
            except Exception as e:
                self.update_status(f"Backup failed: {str(e)}")
                messagebox.showerror("Backup Error", str(e))
        
        thread = threading.Thread(target=run_backup)
        thread.start()

    def restore_files_thread(self):
        def run_restore():
            try:
                self.update_status("Running restore...")
                manifest_path = os.path.join(self.config_data['backup']['manifest_dir'], "backup_manifest.json")
                restore_dir = filedialog.askdirectory(title="Select folder to restore files")
                if not restore_dir:
                    self.update_status("Restore cancelled.")
                    return
                
                restore_files(self.config_data, self.aws_access_key, self.aws_secret_key, manifest_path, restore_dir)
                self.update_status("Restore completed.")
                messagebox.showinfo("Success", f"Restore completed successfully.\nFiles restored to: {restore_dir}")
            except Exception as e:
                self.update_status(f"Restore failed: {str(e)}")
                messagebox.showerror("Restore Error", str(e))
        
        thread = threading.Thread(target=run_restore)
        thread.start()

    def update_status(self, text):
        self.status_label.config(text=text)
        self.update_idletasks()

if __name__ == "__main__":
    app = BackupRestoreGUI()
    app.mainloop()
