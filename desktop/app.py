"""
Standalone CustomTkinter desktop GUI for toDPG.

Drag & drop (or browse for) video files, adjust output resolution/FPS,
and convert them to .dpg using dpgcore.encode() — no Flask, no Docker.
"""
from __future__ import annotations

import os
import queue
import re
import shutil
import threading
from dataclasses import dataclass, field
from tkinter import filedialog, messagebox

import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

from dpgcore import EncodeSettings, EncodingError, encode, probe_duration_seconds

VIDEO_EXTENSIONS = {
    ".avi", ".mp4", ".mkv", ".mov", ".webm", ".flv", ".wmv", ".m4v", ".mpg", ".mpeg", ".ts",
}

# ffmpeg's mpeg1video encoder only accepts standard MPEG-1 frame rates.
VALID_FPS_OPTIONS = ["24", "25", "30"]

# Fraction of overall progress attributed to each encode() stage.
STAGE_WEIGHTS = {"audio": 0.15, "video": 0.80, "thumbnail": 0.03, "mux": 0.02, "done": 0.0}
STAGE_START = {"audio": 0.0, "video": 0.15, "thumbnail": 0.95, "mux": 0.98, "done": 1.0}

_TIME_RE = re.compile(r"time=(\d+):(\d+):(\d+\.?\d*)")


def _parse_ffmpeg_time(line: str) -> float | None:
    match = _TIME_RE.search(line)
    if not match:
        return None
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


@dataclass
class QueueItem:
    path: str
    status: str = "Pending"
    message: str = ""
    row_frame: ctk.CTkFrame | None = field(default=None, repr=False)
    status_label: ctk.CTkLabel | None = field(default=None, repr=False)


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

        self.queue_items: list[QueueItem] = []
        self.output_dir: str | None = None
        self.progress_events: "queue.Queue[tuple]" = queue.Queue()
        self.is_running = False
        self.current_index: int | None = None

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
        self.fps_combo = ctk.CTkComboBox(settings_frame, values=VALID_FPS_OPTIONS, width=80)
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
        button_frame.grid_columnconfigure((0, 1), weight=1)

        self.convert_button = ctk.CTkButton(button_frame, text="Convert All", command=self._start_conversion)
        self.convert_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        if not self.ffmpeg_path or not self.ffprobe_path:
            self.convert_button.configure(state="disabled")

        self.clear_button = ctk.CTkButton(
            button_frame, text="Clear Queue", fg_color="#555555", hover_color="#444444", command=self._clear_queue
        )
        self.clear_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))

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
        existing = {item.path for item in self.queue_items}
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
            self.queue_items.append(QueueItem(path=path))
            existing.add(path)
        if skipped:
            self._append_log(f"Skipped non-video file(s): {', '.join(skipped)}")
        self._refresh_queue_list()

    def _remove_item(self, item: QueueItem) -> None:
        if item.status == "Encoding":
            return
        self.queue_items.remove(item)
        self._refresh_queue_list()

    def _clear_queue(self) -> None:
        self.queue_items = [item for item in self.queue_items if item.status == "Encoding"]
        self._refresh_queue_list()

    def _refresh_queue_list(self) -> None:
        for child in self.queue_frame.winfo_children():
            child.destroy()

        if not self.queue_items:
            ctk.CTkLabel(self.queue_frame, text="No files queued.", text_color="#888888").grid(
                row=0, column=0, sticky="w", padx=8, pady=8
            )
            return

        for row, item in enumerate(self.queue_items):
            row_frame = ctk.CTkFrame(self.queue_frame, fg_color="transparent")
            row_frame.grid(row=row, column=0, sticky="ew", pady=2)
            row_frame.grid_columnconfigure(0, weight=1)
            item.row_frame = row_frame

            name_label = ctk.CTkLabel(row_frame, text=os.path.basename(item.path), anchor="w")
            name_label.grid(row=0, column=0, sticky="ew", padx=(4, 8))

            status_label = ctk.CTkLabel(row_frame, text=item.status, anchor="w", width=140)
            status_label.grid(row=0, column=1, sticky="w")
            item.status_label = status_label

            remove_btn = ctk.CTkButton(
                row_frame, text="✕", width=28, fg_color="transparent", hover_color="#553333",
                command=lambda i=item: self._remove_item(i),
            )
            remove_btn.grid(row=0, column=2, padx=(8, 4))
            if item.status == "Encoding":
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
            fps = int(self.fps_combo.get())
            if width <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid settings", "Width, height, and FPS must be positive numbers.")
            return None
        if str(fps) not in VALID_FPS_OPTIONS:
            messagebox.showerror(
                "Invalid FPS", f"FPS must be one of {', '.join(VALID_FPS_OPTIONS)} (MPEG-1 constraint)."
            )
            return None
        return EncodeSettings(
            video_fps=fps,
            video_width=width,
            video_height=height,
            ffmpeg_path=self.ffmpeg_path or "ffmpeg",
            ffprobe_path=self.ffprobe_path or "ffprobe",
        )

    def _start_conversion(self) -> None:
        if self.is_running:
            return
        pending = [item for item in self.queue_items if item.status == "Pending"]
        if not pending:
            messagebox.showinfo("Nothing to convert", "Add some video files to the queue first.")
            return
        settings = self._read_settings()
        if settings is None:
            return

        self.is_running = True
        self.convert_button.configure(state="disabled")
        self.clear_button.configure(state="disabled")

        thread = threading.Thread(target=self._process_queue, args=(settings,), daemon=True)
        thread.start()

    def _process_queue(self, settings: EncodeSettings) -> None:
        for index, item in enumerate(self.queue_items):
            if item.status != "Pending":
                continue

            self.progress_events.put(("status", index, "Encoding", ""))

            output_dir = self.output_dir or os.path.dirname(item.path)
            stem = os.path.splitext(os.path.basename(item.path))[0]
            output_path = os.path.join(output_dir, stem + ".dpg")

            try:
                duration = probe_duration_seconds(item.path, settings.ffprobe_path)
            except EncodingError:
                duration = 0.0

            def on_progress(stage: str, message: str, _index=index, _duration=duration) -> None:
                elapsed = _parse_ffmpeg_time(message)
                if elapsed is not None and _duration > 0 and stage in STAGE_WEIGHTS:
                    fraction = STAGE_START[stage] + min(elapsed / _duration, 1.0) * STAGE_WEIGHTS[stage]
                    self.progress_events.put(("progress", _index, fraction, stage))
                elif stage in STAGE_START:
                    self.progress_events.put(("progress", _index, STAGE_START[stage], stage))
                if "time=" in message or stage in ("thumbnail", "mux", "done"):
                    self.progress_events.put(("log", f"[{stage}] {message}"))

            try:
                encode(item.path, output_path, settings, on_progress=on_progress)
                self.progress_events.put(("status", index, "Done", output_path))
            except EncodingError as exc:
                self.progress_events.put(("status", index, "Error", str(exc)))
            except Exception as exc:  # noqa: BLE001 - surface unexpected errors in the UI, not a crash
                self.progress_events.put(("status", index, "Error", str(exc)))

        self.progress_events.put(("all_done",))

    # -------------------------------------------------------- main-thread

    def _poll_progress_events(self) -> None:
        try:
            while True:
                event = self.progress_events.get_nowait()
                self._handle_event(event)
        except queue.Empty:
            pass
        self.after(150, self._poll_progress_events)

    def _handle_event(self, event: tuple) -> None:
        kind = event[0]

        if kind == "status":
            _, index, status, message = event
            item = self.queue_items[index]
            item.status = status
            item.message = message
            if item.status_label is not None and item.row_frame is not None and item.row_frame.winfo_exists():
                item.status_label.configure(text=status)
            if status == "Encoding":
                self.current_index = index
                self.current_file_label.configure(text=f"Converting: {os.path.basename(item.path)}")
                self.progress_bar.set(0)
            elif status == "Done":
                self._append_log(f"Done: {message}")
            elif status == "Error":
                self._append_log(f"Error converting {os.path.basename(item.path)}: {message}")

        elif kind == "progress":
            _, index, fraction, stage = event
            if index == self.current_index:
                self.progress_bar.set(min(max(fraction, 0.0), 1.0))
                self.current_file_label.configure(
                    text=f"Converting: {os.path.basename(self.queue_items[index].path)} ({stage}, {fraction * 100:.0f}%)"
                )

        elif kind == "log":
            self._append_log(event[1])

        elif kind == "all_done":
            self.is_running = False
            self.current_index = None
            self.convert_button.configure(state="normal")
            self.clear_button.configure(state="normal")
            self.current_file_label.configure(text="All conversions complete.")
            self.progress_bar.set(1)


def main() -> None:
    app = ConverterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
