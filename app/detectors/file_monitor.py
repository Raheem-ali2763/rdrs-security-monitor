from collections.abc import Callable
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from app.detectors.base import FileEvent


EventCallback = Callable[[FileEvent], None]


class RDRSEventHandler(FileSystemEventHandler):
    """Convert watchdog events into normalized RDRS FileEvent objects."""

    def __init__(self, callback: EventCallback) -> None:
        super().__init__()
        self.callback = callback

    def _emit(self, event_type: str, path: str) -> None:
        event = FileEvent.create(
            event_type=event_type,
            path=path,
        )
        self.callback(event)

    def on_created(self, event) -> None:
        if not event.is_directory:
            self._emit("create", event.src_path)

    def on_modified(self, event) -> None:
        if not event.is_directory:
            self._emit("modify", event.src_path)

    def on_deleted(self, event) -> None:
        if not event.is_directory:
            self._emit("delete", event.src_path)

    def on_moved(self, event) -> None:
        if not event.is_directory:
            self._emit("rename", event.dest_path)


class FileMonitor:
    """Monitor configured directories for file-system activity."""

    def __init__(
        self,
        paths: list[str | Path],
        callback: EventCallback,
    ) -> None:
        self.paths = [Path(path) for path in paths]
        self.callback = callback
        self.observer = Observer()

    def start(self) -> None:
        """Start monitoring configured directories."""
        handler = RDRSEventHandler(self.callback)

        for path in self.paths:
            path.mkdir(parents=True, exist_ok=True)
            self.observer.schedule(
                handler,
                str(path),
                recursive=True,
            )

        self.observer.start()

    def stop(self) -> None:
        """Stop monitoring and wait for the observer thread."""
        self.observer.stop()
        self.observer.join()
