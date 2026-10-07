import customtkinter as ctk
import cv2
from PIL import Image
import math
import os
import threading
from tkinter import filedialog, messagebox

# Theme configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SpritesheetApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Video to Spritesheet Converter")
        self.geometry("600x550")
        self.resizable(False, False)

        self.video_path = None

        # Title
        self.title_label = ctk.CTkLabel(self, text="Video to Spritesheet Converter", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)

        # File Button
        self.btn_file = ctk.CTkButton(self, text="Choose video file", command=self.select_file, width=300)
        self.btn_file.pack(pady=10)

        self.lbl_file_name = ctk.CTkLabel(self, text="No file chosen", text_color="gray")
        self.lbl_file_name.pack(pady=(0, 20))

        # Inputs Container
        self.frame_inputs = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_inputs.pack(pady=10)

        # Width Input
        self.lbl_width = ctk.CTkLabel(self.frame_inputs, text="Width (PX)")
        self.lbl_width.grid(row=0, column=0, padx=10, sticky="w")
        self.entry_width = ctk.CTkEntry(self.frame_inputs, placeholder_text="Ex: 3840")
        self.entry_width.grid(row=1, column=0, padx=10)
        
        # Event listener to auto-fill Height
        self.entry_width.bind("<KeyRelease>", self.auto_fill_height)

        # Height Input
        self.lbl_height = ctk.CTkLabel(self.frame_inputs, text="Height (PX)")
        self.lbl_height.grid(row=0, column=1, padx=10, sticky="w")
        self.entry_height = ctk.CTkEntry(self.frame_inputs, placeholder_text="Ex: 2160")
        self.entry_height.grid(row=1, column=1, padx=10)

        # FPS Input
        self.lbl_fps = ctk.CTkLabel(self.frame_inputs, text="Frames per Second")
        self.lbl_fps.grid(row=0, column=2, padx=10, sticky="w")
        
        self.fps_var = ctk.StringVar(value="30")
        self.combo_fps = ctk.CTkComboBox(self.frame_inputs, values=["5", "10", "15", "24", "30", "60"], variable=self.fps_var)
        self.combo_fps.grid(row=1, column=2, padx=10)

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.pack(pady=30)
        self.progress_bar.set(0)

        self.lbl_status = ctk.CTkLabel(self, text="")
        self.lbl_status.pack()

        # Convert Button
        self.btn_convert = ctk.CTkButton(self, text="Convert to Spritesheet", command=self.start_conversion, width=200, height=40)
        self.btn_convert.pack(pady=20)

    # Auto-fills height based on common 16:9 resolutions
    def auto_fill_height(self, event=None):
        known_resolutions = {
            3840: 2160,  # 4K
            2560: 1440,  # 1440p (2K)
            1920: 1080,  # 1080p (Full HD)
            1280: 720,   # 720p (HD)
            854: 480,    # 480p
            640: 360,    # 360p
            426: 240,    # 240p
            320: 180     # 180p
        }
        
        current_width_str = self.entry_width.get()
        
        if current_width_str.isdigit():
            width = int(current_width_str)
            if width in known_resolutions:
                self.entry_height.delete(0, "end")
                self.entry_height.insert(0, str(known_resolutions[width]))

    def select_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if filepath:
            self.video_path = filepath
            filename = os.path.basename(filepath)
            self.lbl_file_name.configure(text=filename)

    def start_conversion(self):
        if not self.video_path:
            messagebox.showwarning("Warning", "Please select a video file first.")
            return

        self.btn_convert.configure(state="disabled")
        self.btn_file.configure(state="disabled")
        self.progress_bar.set(0)
        
        # Start in a separate thread to prevent UI freezing
        threading.Thread(target=self.process_video, daemon=True).start()

    def process_video(self):
        try:
            self.lbl_status.configure(text="Reading video...")
            
            cap = cv2.VideoCapture(self.video_path)
            original_fps = cap.get(cv2.CAP_PROP_FPS)
            total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_video_frames / original_fps

            target_fps = int(self.fps_var.get())
            total_frames_to_extract = math.floor(duration * target_fps)

            w_str = self.entry_width.get()
            h_str = self.entry_height.get()
            
            frame_width = int(w_str) if w_str else int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(h_str) if h_str else int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # JPG/PNG maximum dimension limit
            MAX_IMG_DIM = 65500 
            max_cols = math.floor(MAX_IMG_DIM / frame_width)
            max_rows = math.floor(MAX_IMG_DIM / frame_height)
            max_frames_allowed = max_cols * max_rows

            if max_cols == 0 or max_rows == 0:
                self.reset_ui("Error: Entered resolution is too high.")
                messagebox.showerror("Error", "The resolution of a single frame cannot exceed 65,500 pixels.")
                return

            # Verification for a single file limit
            if total_frames_to_extract > max_frames_allowed:
                max_seconds = max_frames_allowed / target_fps
                self.reset_ui("Process canceled.")
                messagebox.showerror(
                    "Limit Exceeded", 
                    f"To generate a single file at {frame_width}x{frame_height} at {target_fps} FPS, "
                    f"the video can be at most {max_seconds:.1f} seconds long.\n\n"
                    f"Your current video is {duration:.1f} seconds long. Please lower the FPS, reduce the resolution, or trim the video."
                )
                return

            columns = math.ceil(math.sqrt(total_frames_to_extract))
            if columns > max_cols:
                columns = max_cols
            rows = math.ceil(total_frames_to_extract / columns)

            final_width = columns * frame_width
            final_height = rows * frame_height

            self.lbl_status.configure(text=f"Allocating memory ({final_width}x{final_height})...")
            
            spritesheet = Image.new("RGB", (final_width, final_height))
            frame_interval = original_fps / target_fps
            current_frame_idx = 0
            extracted_count = 0

            self.lbl_status.configure(text="Extracting frames...")

            while True:
                ret, frame = cap.read()
                if not ret or extracted_count >= total_frames_to_extract:
                    break

                if current_frame_idx >= extracted_count * frame_interval:
                    if (frame.shape[1] != frame_width) or (frame.shape[0] != frame_height):
                        frame = cv2.resize(frame, (frame_width, frame_height))
                    
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img_pil = Image.fromarray(frame_rgb)

                    col = extracted_count % columns
                    row = extracted_count // columns

                    x = col * frame_width
                    y = row * frame_height

                    spritesheet.paste(img_pil, (x, y))

                    extracted_count += 1
                    
                    progress_val = extracted_count / total_frames_to_extract
                    self.progress_bar.set(progress_val)
                    self.lbl_status.configure(text=f"Processing: {extracted_count}/{total_frames_to_extract} frames")

                current_frame_idx += 1

            cap.release()

            self.lbl_status.configure(text="Saving image (This may take a few seconds)...")
            
            output_filename = os.path.splitext(self.video_path)[0] + "_spritesheet.jpg"
            spritesheet.save(output_filename, "JPEG", quality=90)

            self.reset_ui(f"Done! Saved as: {os.path.basename(output_filename)}")
            messagebox.showinfo("Success", f"Spritesheet generated successfully!\nSaved in the same folder as the original video.")

        except Exception as e:
            self.reset_ui("Error during processing.")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def reset_ui(self, msg=""):
        self.btn_convert.configure(state="normal")
        self.btn_file.configure(state="normal")
        self.lbl_status.configure(text=msg)

if __name__ == "__main__":
    app = SpritesheetApp()
    app.mainloop()