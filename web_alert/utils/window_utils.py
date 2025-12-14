"""Window utility functions."""


def center_window(window, width: int, height: int):
    """Center a tkinter window on screen.

    Args:
        window: The tkinter window to center
        width: Window width in pixels
        height: Window height in pixels
    """
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
