"""
Standalone CustomTkinter desktop GUI for toDPG.

Drag & drop (or browse for) video files, adjust output resolution/FPS,
and convert them to .dpg using convqueue.ConversionQueue (itself built on
dpgcore.encode()) — no Flask, no Docker. All queueing, threading, and
progress-fraction math lives in convqueue, which has no CustomTkinter (or
any GUI toolkit) dependency; this file only owns widgets and marshals
convqueue's events onto the Tk main thread.
"""
from __future__ import annotations

import os
import queue
import shutil
from tkinter import filedialog, messagebox

import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

from convqueue import ConversionQueue, EventKind, ItemStatus, QueueEvent, QueueItem
from dpgcore import EncodeSettings

VIDEO_EXTENSIONS = {
    ".avi", ".mp4", ".mkv", ".mov", ".webm", ".flv", ".wmv", ".m4v", ".mpg", ".mpeg", ".ts",
}

# ffmpeg's mpeg1video encoder only accepts standard MPEG-1 frame rates.
# dpgcore snaps any fps to the nearest of these regardless, but offering
# exactly these as choices means the GUI never shows a value that will be
# silently changed underneath the user.
FPS_OPTIONS = ["23.976", "24", "25", "29.97", "30"]

_STATUS_COLORS = {
    ItemStatus.ERROR: "#e05555",
    ItemStatus.CANCELLED: "#c9a227",
}


class DnDCTk(ctk.CTk, TkinterDnD.DnDWrapper):
    """A CustomTkinter root window with drag-and-drop support."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


class ConverterApp(DnDCTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.title("toDPG Converter")
        self.geometry("720x680")
        self.minsize(640, 600)

        self.queue = ConversionQueue()
        self._widgets: dict[int, tuple[ctk.CTkFrame, ctk.CTkLabel]] = {}
        self.output_dir: str | None = None
        self.progress_events: "queue.Queue[QueueEvent]" = queue.Queue()
        self.current_item: QueueItem | None = None

        self.ffmpeg_path = shutil.which("ffmpeg")
        self.ffprobe_path = shutil.which("ffprobe")

        self._build_widgets()
        self._poll_progress_events()

    # ------------------------------------------------------------------ UI

    def _build_widgets(self) -> None:
        self.grid_columnconfigure(0, weight=1)

        if not self.ffmpeg_path or not self.ffprobe_path:
            warning = ctk.CTkLabel(
                self,
                text="FFmpeg/ffprobe not found on PATH — install FFmpeg to enable conversion.",
                text_color="#e05555",
            )
            warning.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 0))

        self.drop_zone = ctk.CTkFrame(self, height=110, border_width=2, border_color="#5a5a5a")
        self.drop_zone.grid(row=1, column=0, sticky="ew", padx=12, pady=12)
        self.drop_zone.grid_propagate(False)
        drop_label = ctk.CTkLabel(
            self.drop_zone,
            text="Drag & drop video files here\nor click to browse",
            font=ctk.CTkFont(size=15),
        )
        drop_label.place(relx=0.5, rely=0.5, anchor="center")

        for widget in (self.drop_zone, drop_label):
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind("<<Drop>>", self._on_drop)
            widget.bind("<Button-1>", lambda _e: self._browse_files())

        self.queue_frame = ctk.CTkScrollableFrame(self, label_text="Queue", height=160)
        self.queue_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.queue_frame.grid_columnconfigure(0, weight=1)

        settings_frame = ctk.CTkFrame(self)
        settings_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 12))
        for col in range(6):
            settings_frame.grid_columnconfigure(col, weight=1)

        ctk.CTkLabel(settings_frame, text="Width").grid(row=0, column=0, padx=(12, 4), pady=10, sticky="w")
        self.width_entry = ctk.CTkEntry(settings_frame, width=70)
        self.width_entry.insert(0, "256")
        self.width_entry.grid(row=0, column=1, padx=(0, 12), pady=10, sticky="w")

        ctk.CTkLabel(settings_frame, text="Height").grid(row=0, column=2, padx=(12, 4), pady=10, sticky="w")
        self.height_entry = ctk.CTkEntry(settings_frame, width=70)
        self.height_entry.insert(0, "192")
        self.height_entry.grid(row=0, column=3, padx=(0, 12), pady=10, sticky="w")

        ctk.CTkLabel(settings_frame, text="FPS").grid(row=0, column=4, padx=(12, 4), pady=10, sticky="w")
        self.fps_combo = ctk.CTkComboBox(settings_frame, values=FPS_OPTIONS, width=90)
        self.fps_combo.set("24")
        self.fps_combo.grid(row=0, column=5, padx=(0, 12), pady=10, sticky="w")

        ctk.CTkLabel(settings_frame, text="Output folder").grid(row=1, column=0, padx=(12, 4), pady=(0, 10), sticky="w")
        self.output_label = ctk.CTkLabel(settings_frame, text="Same as source file", anchor="w")
        self.output_label.grid(row=1, column=1, columnspan=3, padx=(0, 4), pady=(0, 10), sticky="ew")
        ctk.CTkButton(settings_frame, text="Choose...", width=90, command=self._choose_output_folder).grid(
            row=1, column=4, columnspan=2, padx=(0, 12), pady=(0, 10), sticky="e"
        )

        progress_frame = ctk.CTkFrame(self)
        progress_frame.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 12))
        progress_frame.grid_columnconfigure(0, weight=1)

        self.current_file_label = ctk.CTkLabel(progress_frame, text="No conversion in progress", anchor="w")
        self.current_file_label.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 2))

        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))

        self.log_box = ctk.CTkTextbox(self, height=140, state="disabled")
        self.log_box.grid(row=5, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.grid_rowconfigure(5, weight=1)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=6, column=0, sticky="ew", padx=12, pady=(0, 12))
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.convert_button = ctk.CTkButton(button_frame, text="Convert All", command=self._start_conversion)
        self.convert_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        if not self.ffmpeg_path or not self.ffprobe_path:
            self.convert_button.configure(state="disabled")

        self.cancel_button = ctk.CTkButton(
            button_frame, text="Cancel", fg_color="#8a3b3b", hover_color="#732f2f",
            command=self._cancel_conversion, state="disabled",
        )
        self.cancel_button.grid(row=0, column=1, sticky="ew", padx=6)

        self.clear_button = ctk.CTkButton(
            button_frame, text="Clear Queue", fg_color="#555555", hover_color="#444444", command=self._clear_queue
        )
        self.clear_button.grid(row=0, column=2, sticky="ew", padx=(6, 0))

    # --------------------------------------------------------------- queue

    def _on_drop(self, event) -> None:
        paths = self.tk.splitlist(event.data)
        self._add_files(paths)

    def _browse_files(self) -> None:
        paths = filedialog.askopenfilenames(
            title="Select video files",
            filetypes=[("Video files", " ".join(f"*{ext}" for ext in VIDEO_EXTENSIONS)), ("All files", "*.*")],
        )
        if paths:
            self._add_files(paths)

    def _add_files(self, paths) -> None:
        existing = {item.path for item in self.queue.items}
        skipped = []
        for path in paths:
            path = os.path.abspath(path)
            if not os.path.isfile(path):
                continue
            ext = os.path.splitext(path)[1].lower()
            if ext not in VIDEO_EXTENSIONS:
                skipped.append(os.path.basename(path))
                continue
            if path in existing:
                continue
            self.queue.add(path)
            existing.add(path)
        if skipped:
            self._append_log(f"Skipped non-video file(s): {', '.join(skipped)}")
        self._refresh_queue_list()

    def _remove_item(self, item: QueueItem) -> None:
        if self.queue.remove(item):
            self._refresh_queue_list()

    def _clear_queue(self) -> None:
        self.queue.clear_pending()
        self._refresh_queue_list()

    def _refresh_queue_list(self) -> None:
        for child in self.queue_frame.winfo_children():
            child.destroy()
        self._widgets.clear()

        if not self.queue.items:
            ctk.CTkLabel(self.queue_frame, text="No files queued.", text_color="#888888").grid(
                row=0, column=0, sticky="w", padx=8, pady=8
            )
            return

        for row, item in enumerate(self.queue.items):
            row_frame = ctk.CTkFrame(self.queue_frame, fg_color="transparent")
            row_frame.grid(row=row, column=0, sticky="ew", pady=2)
            row_frame.grid_columnconfigure(0, weight=1)

            name_label = ctk.CTkLabel(row_frame, text=os.path.basename(item.path), anchor="w")
            name_label.grid(row=0, column=0, sticky="ew", padx=(4, 8))

            status_label = ctk.CTkLabel(
                row_frame, text=item.status.value, anchor="w", width=140,
                text_color=_STATUS_COLORS.get(item.status),
            )
            status_label.grid(row=0, column=1, sticky="w")
            self._widgets[id(item)] = (row_frame, status_label)

            remove_btn = ctk.CTkButton(
                row_frame, text="✕", width=28, fg_color="transparent", hover_color="#553333",
                command=lambda i=item: self._remove_item(i),
            )
            remove_btn.grid(row=0, column=2, padx=(8, 4))
            if item.status == ItemStatus.ENCODING:
                remove_btn.configure(state="disabled")

    def _choose_output_folder(self) -> None:
        folder = filedialog.askdirectory(title="Choose output folder")
        if folder:
            self.output_dir = folder
            self.output_label.configure(text=folder)

    # ------------------------------------------------------------ logging

    def _append_log(self, text: str) -> None:
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    # --------------------------------------------------------- conversion

    def _read_settings(self) -> EncodeSettings | None:
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            fps = float(self.fps_combo.get())
            if width <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid settings", "Width, height, and FPS must be positive numbers.")
            return None
        # dpgcore snaps video_fps/audio_frequency/audio_channels to
        # MPEG-1/DPG-safe values itself, so no manual validation is needed
        # beyond basic type/positivity checks above.
        return EncodeSettings(
            video_fps=fps,
            video_width=width,
            video_height=height,
            ffmpeg_path=self.ffmpeg_path or "ffmpeg",
            ffprobe_path=self.ffprobe_path or "ffprobe",
        )

    def _start_conversion(self) -> None:
        if self.queue.is_running():
            return
        pending = [item for item in self.queue.items if item.status == ItemStatus.PENDING]
        if not pending:
            messagebox.showinfo("Nothing to convert", "Add some video files to the queue first.")
            return
        settings = self._read_settings()
        if settings is None:
            return

        if self.output_dir:
            for item in pending:
                stem = os.path.splitext(os.path.basename(item.path))[0]
                item.output_path = os.path.join(self.output_dir, stem + ".dpg")

        self.convert_button.configure(state="disabled")
        self.clear_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")

        self.queue.start(settings, on_event=self.progress_events.put)

    def _cancel_conversion(self) -> None:
        self.cancel_button.configure(state="disabled")
        self.queue.cancel()

    # -------------------------------------------------------- main-thread

    def _poll_progress_events(self) -> None:
        try:
            while True:
                event = self.progress_events.get_nowait()
                self._handle_event(event)
        except queue.Empty:
            pass
        self.after(150, self._poll_progress_events)

    def _handle_event(self, event: QueueEvent) -> None:
        if event.kind == EventKind.STATUS:
            item = event.item
            widgets = self._widgets.get(id(item))
            if widgets is not None:
                _, status_label = widgets
                if status_label.winfo_exists():
                    status_label.configure(
                        text=item.status.value, text_color=_STATUS_COLORS.get(item.status)
                    )
            if item.status == ItemStatus.ENCODING:
                self.current_item = item
                self.current_file_label.configure(text=f"Converting: {os.path.basename(item.path)}")
                self.progress_bar.set(0)
            elif item.status == ItemStatus.DONE:
                self._append_log(f"Done: {item.message}")
            elif item.status == ItemStatus.ERROR:
                self._append_log(f"Error converting {os.path.basename(item.path)}: {item.message}")
            elif item.status == ItemStatus.CANCELLED:
                self._append_log(f"Cancelled: {os.path.basename(item.path)}")

        elif event.kind == EventKind.PROGRESS:
            if event.item is self.current_item:
                fraction = min(max(event.fraction or 0.0, 0.0), 1.0)
                self.progress_bar.set(fraction)
                self.current_file_label.configure(
                    text=f"Converting: {os.path.basename(event.item.path)} ({event.stage}, {fraction * 100:.0f}%)"
                )

        elif event.kind == EventKind.LOG:
            self._append_log(event.message)

        elif event.kind == EventKind.ALL_DONE:
            self.current_item = None
            self.convert_button.configure(state="normal")
            self.clear_button.configure(state="normal")
            self.cancel_button.configure(state="disabled")
            self.current_file_label.configure(text="All conversions complete.")
            self.progress_bar.set(1)


def main() -> None:
    app = ConverterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
