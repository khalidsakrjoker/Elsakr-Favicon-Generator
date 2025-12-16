"""
Elsakr Favicon Generator - Premium Edition
Generate all favicon sizes from a single image.
Modern Dark Theme with Premium UI
"""

import os
import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import threading


class Colors:
    """Premium dark theme colors."""
    BG_DARK = "#0a0a0f"
    BG_CARD = "#12121a"
    BG_CARD_HOVER = "#1a1a25"
    BG_INPUT = "#1e1e2e"
    
    PRIMARY = "#6366f1"  # Indigo
    PRIMARY_HOVER = "#818cf8"
    PRIMARY_DARK = "#4f46e5"
    
    SECONDARY = "#22d3ee"  # Cyan accent
    SUCCESS = "#10b981"
    WARNING = "#f59e0b"
    ERROR = "#ef4444"
    
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#a1a1aa"
    TEXT_MUTED = "#71717a"
    
    BORDER = "#27272a"
    BORDER_FOCUS = "#6366f1"
    
    GRADIENT_START = "#6366f1"
    GRADIENT_END = "#8b5cf6"


class PremiumButton(tk.Canvas):
    """Custom premium button with gradient and hover effects."""
    
    def __init__(self, parent, text, command=None, width=200, height=45, 
                 primary=True, icon=None, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg=Colors.BG_CARD, highlightthickness=0, **kwargs)
        
        self.command = command
        self.text = text
        self.width = width
        self.height = height
        self.primary = primary
        self.icon = icon
        self.hovered = False
        
        self.draw_button()
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
    def draw_button(self):
        """Draw the button."""
        self.delete("all")
        
        # Colors based on state and type
        if self.primary:
            if self.hovered:
                bg_color = Colors.PRIMARY_HOVER
            else:
                bg_color = Colors.PRIMARY
            text_color = Colors.TEXT_PRIMARY
        else:
            if self.hovered:
                bg_color = Colors.BG_CARD_HOVER
            else:
                bg_color = Colors.BG_INPUT
            text_color = Colors.TEXT_SECONDARY
        
        # Draw rounded rectangle
        radius = 10
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, 
                                  radius, fill=bg_color, outline="")
        
        # Draw text
        self.create_text(self.width//2, self.height//2, 
                        text=self.text, fill=text_color,
                        font=("Segoe UI Semibold", 11))
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle."""
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def on_enter(self, event):
        self.hovered = True
        self.draw_button()
        self.config(cursor="hand2")
        
    def on_leave(self, event):
        self.hovered = False
        self.draw_button()
        
    def on_click(self, event):
        if self.command:
            self.command()


class PremiumCard(tk.Frame):
    """Premium card container with subtle border."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=Colors.BG_CARD, **kwargs)
        self.config(highlightbackground=Colors.BORDER, 
                   highlightthickness=1)


class DropZone(tk.Canvas):
    """Drag and drop zone for images."""
    
    def __init__(self, parent, on_file_drop=None, width=300, height=250, **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=Colors.BG_INPUT, highlightthickness=2,
                        highlightbackground=Colors.BORDER, **kwargs)
        
        self.on_file_drop = on_file_drop
        self.width = width
        self.height = height
        self.has_image = False
        self.photo = None
        
        self.draw_empty_state()
        
        self.bind("<Button-1>", self.on_click)
        
    def draw_empty_state(self):
        """Draw the empty drop zone state."""
        self.delete("all")
        
        # Dashed border effect
        dash_length = 10
        
        # Draw icon
        self.create_text(self.width//2, self.height//2 - 40,
                        text="🖼️", font=("Segoe UI", 48))
        
        # Draw text
        self.create_text(self.width//2, self.height//2 + 30,
                        text="Click to select image",
                        fill=Colors.TEXT_SECONDARY,
                        font=("Segoe UI", 12))
        
        self.create_text(self.width//2, self.height//2 + 55,
                        text="PNG, JPG, WebP, BMP",
                        fill=Colors.TEXT_MUTED,
                        font=("Segoe UI", 10))
        
    def set_image(self, image, filename=""):
        """Display the selected image."""
        self.delete("all")
        self.has_image = True
        
        # Resize for preview
        preview = image.copy()
        preview.thumbnail((self.width - 40, self.height - 60), Image.Resampling.LANCZOS)
        
        # Center the image
        self.photo = ImageTk.PhotoImage(preview)
        x = self.width // 2
        y = (self.height - 30) // 2
        
        self.create_image(x, y, image=self.photo)
        
        # Filename at bottom
        if filename:
            self.create_text(self.width//2, self.height - 20,
                            text=filename[:30] + "..." if len(filename) > 30 else filename,
                            fill=Colors.TEXT_MUTED,
                            font=("Segoe UI", 9))
        
    def on_click(self, event):
        """Handle click to select file."""
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.webp *.bmp"),
            ("All files", "*.*")
        ]
        
        path = filedialog.askopenfilename(
            title="Select Source Image",
            filetypes=filetypes
        )
        
        if path and self.on_file_drop:
            self.on_file_drop(path)


class FaviconGenerator:
    """Main application class for Premium Favicon Generator."""
    
    FAVICON_SIZES = {
        'favicon-16x16.png': (16, 16),
        'favicon-32x32.png': (32, 32),
        'apple-touch-icon.png': (180, 180),
        'android-chrome-192x192.png': (192, 192),
        'android-chrome-512x512.png': (512, 512),
        'mstile-150x150.png': (150, 150),
    }
    
    ICO_SIZES = [(16, 16), (32, 32), (48, 48)]
    
    def __init__(self, root):
        self.root = root
        self.root.title("Elsakr Favicon Generator")
        self.root.geometry("1250x850")
        self.root.minsize(1000, 700)
        self.root.configure(bg=Colors.BG_DARK)
        
        # Set window icon
        self.set_window_icon()
        
        # Variables
        self.source_image = None
        self.source_path = None
        self.bg_color = "#FFFFFF"
        self.output_folder = None
        self.preview_images = {}
        
        # Load logo
        self.load_logo()
        
        # Build UI
        self.create_ui()
        
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def set_window_icon(self):
        """Set the window icon."""
        try:
            icon_path = self.resource_path(os.path.join("assets", "fav.ico"))
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
            
    def load_logo(self):
        """Load the Elsakr logo."""
        self.logo_photo = None
        try:
            logo_path = self.resource_path(os.path.join("assets", "Sakr-logo.png"))
            if os.path.exists(logo_path):
                logo = Image.open(logo_path)
                logo.thumbnail((45, 45), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo)
        except:
            pass
        
    def create_ui(self):
        """Create the premium UI."""
        # Main container
        main = tk.Frame(self.root, bg=Colors.BG_DARK)
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)
        
        # Header
        self.create_header(main)
        
        # Content
        content = tk.Frame(main, bg=Colors.BG_DARK)
        content.pack(fill=tk.BOTH, expand=True, pady=(25, 0))
        
        # Left panel
        self.create_left_panel(content)
        
        # Right panel
        self.create_right_panel(content)
        
    def create_header(self, parent):
        """Create the header section."""
        header = tk.Frame(parent, bg=Colors.BG_DARK)
        header.pack(fill=tk.X)
        
        # Logo and title
        title_frame = tk.Frame(header, bg=Colors.BG_DARK)
        title_frame.pack(side=tk.LEFT)
        
        if self.logo_photo:
            logo_label = tk.Label(title_frame, image=self.logo_photo, bg=Colors.BG_DARK)
            logo_label.pack(side=tk.LEFT, padx=(0, 15))
        
        title_text = tk.Frame(title_frame, bg=Colors.BG_DARK)
        title_text.pack(side=tk.LEFT)
        
        tk.Label(title_text, text="Favicon Generator", 
                font=("Segoe UI Bold", 24), fg=Colors.TEXT_PRIMARY,
                bg=Colors.BG_DARK).pack(anchor=tk.W)
        
        tk.Label(title_text, text="Generate all favicon sizes from a single image",
                font=("Segoe UI", 11), fg=Colors.TEXT_MUTED,
                bg=Colors.BG_DARK).pack(anchor=tk.W)
        
        # Version badge
        version_frame = tk.Frame(header, bg=Colors.BG_DARK)
        version_frame.pack(side=tk.RIGHT)
        
        badge = tk.Label(version_frame, text=" v1.0 ", 
                        font=("Segoe UI", 9), fg=Colors.PRIMARY,
                        bg=Colors.BG_INPUT)
        badge.pack()
        
    def create_left_panel(self, parent):
        """Create the left panel with input controls."""
        left = tk.Frame(parent, bg=Colors.BG_DARK, width=380)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left.pack_propagate(False)
        
        # Source Image Card
        source_card = PremiumCard(left, padx=20, pady=20)
        source_card.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(source_card, text="📁 Source Image",
                font=("Segoe UI Semibold", 13), fg=Colors.TEXT_PRIMARY,
                bg=Colors.BG_CARD).pack(anchor=tk.W, pady=(0, 15))
        
        # Drop zone
        self.drop_zone = DropZone(source_card, on_file_drop=self.load_image,
                                  width=340, height=220)
        self.drop_zone.pack()
        
        # Image info
        self.image_info = tk.Label(source_card, text="No image selected",
                                   font=("Segoe UI", 10), fg=Colors.TEXT_MUTED,
                                   bg=Colors.BG_CARD)
        self.image_info.pack(pady=(10, 0))
        
        # Settings Card
        settings_card = PremiumCard(left, padx=20, pady=20)
        settings_card.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(settings_card, text="⚙️ Settings",
                font=("Segoe UI Semibold", 13), fg=Colors.TEXT_PRIMARY,
                bg=Colors.BG_CARD).pack(anchor=tk.W, pady=(0, 15))
        
        # Background color
        color_frame = tk.Frame(settings_card, bg=Colors.BG_CARD)
        color_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(color_frame, text="Background Color (for transparent images)",
                font=("Segoe UI", 10), fg=Colors.TEXT_SECONDARY,
                bg=Colors.BG_CARD).pack(side=tk.LEFT)
        
        color_btn_frame = tk.Frame(color_frame, bg=Colors.BG_CARD)
        color_btn_frame.pack(side=tk.RIGHT)
        
        self.color_preview = tk.Label(color_btn_frame, width=4, height=1,
                                      bg=self.bg_color, relief='flat')
        self.color_preview.pack(side=tk.LEFT, padx=(0, 8))
        
        color_btn = tk.Label(color_btn_frame, text="Choose", cursor="hand2",
                            font=("Segoe UI", 9), fg=Colors.PRIMARY,
                            bg=Colors.BG_CARD)
        color_btn.pack(side=tk.LEFT)
        color_btn.bind("<Button-1>", lambda e: self.choose_color())
        
        # Output folder
        tk.Label(settings_card, text="Output Folder",
                font=("Segoe UI", 10), fg=Colors.TEXT_SECONDARY,
                bg=Colors.BG_CARD).pack(anchor=tk.W)
        
        folder_frame = tk.Frame(settings_card, bg=Colors.BG_CARD)
        folder_frame.pack(fill=tk.X, pady=(8, 0))
        
        self.folder_entry = tk.Entry(folder_frame, font=("Segoe UI", 10),
                                     bg=Colors.BG_INPUT, fg=Colors.TEXT_PRIMARY,
                                     insertbackground=Colors.TEXT_PRIMARY,
                                     relief='flat', highlightthickness=1,
                                     highlightbackground=Colors.BORDER)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        
        browse_btn = tk.Label(folder_frame, text="📂", cursor="hand2",
                             font=("Segoe UI", 16), fg=Colors.TEXT_SECONDARY,
                             bg=Colors.BG_CARD)
        browse_btn.pack(side=tk.RIGHT)
        browse_btn.bind("<Button-1>", lambda e: self.select_output_folder())
        
        # Generate button
        self.generate_btn = PremiumButton(left, text="🚀  Generate Favicons",
                                          command=self.generate_favicons,
                                          width=340, height=50)
        self.generate_btn.pack(pady=(15, 0))
        
        # Progress section
        progress_frame = tk.Frame(left, bg=Colors.BG_DARK)
        progress_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Custom progress bar
        self.progress_canvas = tk.Canvas(progress_frame, height=6, 
                                          bg=Colors.BG_INPUT, highlightthickness=0)
        self.progress_canvas.pack(fill=tk.X)
        
        self.status_label = tk.Label(progress_frame, text="Ready",
                                     font=("Segoe UI", 10), fg=Colors.TEXT_MUTED,
                                     bg=Colors.BG_DARK)
        self.status_label.pack(pady=(8, 0))
        
    def create_right_panel(self, parent):
        """Create the right panel with previews."""
        right = tk.Frame(parent, bg=Colors.BG_DARK)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Preview Card
        preview_card = PremiumCard(right, padx=25, pady=20)
        preview_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(preview_card, text="👁️ Preview - All Sizes",
                font=("Segoe UI Semibold", 13), fg=Colors.TEXT_PRIMARY,
                bg=Colors.BG_CARD).pack(anchor=tk.W, pady=(0, 20))
        
        # Preview grid
        grid_frame = tk.Frame(preview_card, bg=Colors.BG_CARD)
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        self.preview_slots = {}
        sizes_info = [
            ('favicon.ico', '16/32/48', 48),
            ('favicon-16x16.png', '16×16', 16),
            ('favicon-32x32.png', '32×32', 32),
            ('apple-touch-icon.png', '180×180', 60),
            ('android-chrome-192x192.png', '192×192', 70),
            ('mstile-150x150.png', '150×150', 55),
        ]
        
        for i, (name, size_text, display_size) in enumerate(sizes_info):
            row = i // 3
            col = i % 3
            
            slot = tk.Frame(grid_frame, bg=Colors.BG_INPUT, padx=15, pady=15)
            slot.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
            
            # Preview image placeholder
            img_frame = tk.Frame(slot, bg=Colors.BG_DARK, width=80, height=80)
            img_frame.pack(pady=(0, 10))
            img_frame.pack_propagate(False)
            
            img_label = tk.Label(img_frame, text="—", font=("Segoe UI", 20),
                                fg=Colors.TEXT_MUTED, bg=Colors.BG_DARK)
            img_label.pack(expand=True)
            
            # Size name
            tk.Label(slot, text=name.replace('.png', '').replace('.ico', ''),
                    font=("Segoe UI", 9), fg=Colors.TEXT_PRIMARY,
                    bg=Colors.BG_INPUT).pack()
            
            tk.Label(slot, text=size_text,
                    font=("Segoe UI", 8), fg=Colors.TEXT_MUTED,
                    bg=Colors.BG_INPUT).pack()
            
            self.preview_slots[name] = (img_label, display_size)
        
        # Configure grid
        for i in range(3):
            grid_frame.columnconfigure(i, weight=1)
        for i in range(2):
            grid_frame.rowconfigure(i, weight=1)
        
        # HTML Code Card
        html_card = PremiumCard(right, padx=25, pady=20)
        html_card.pack(fill=tk.X, pady=(15, 0))
        
        header_row = tk.Frame(html_card, bg=Colors.BG_CARD)
        header_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header_row, text="📋 HTML Code Snippet",
                font=("Segoe UI Semibold", 13), fg=Colors.TEXT_PRIMARY,
                bg=Colors.BG_CARD).pack(side=tk.LEFT)
        
        copy_btn = tk.Label(header_row, text="Copy", cursor="hand2",
                           font=("Segoe UI", 10), fg=Colors.PRIMARY,
                           bg=Colors.BG_CARD)
        copy_btn.pack(side=tk.RIGHT)
        copy_btn.bind("<Button-1>", lambda e: self.copy_html())
        
        # HTML text area
        self.html_text = tk.Text(html_card, height=5, font=("Consolas", 10),
                                 bg=Colors.BG_INPUT, fg=Colors.TEXT_SECONDARY,
                                 insertbackground=Colors.TEXT_PRIMARY,
                                 relief='flat', wrap=tk.NONE,
                                 highlightthickness=1,
                                 highlightbackground=Colors.BORDER)
        self.html_text.pack(fill=tk.X)
        self.html_text.insert('1.0', '<!-- Generate favicons to see the HTML code -->')
        self.html_text.config(state=tk.DISABLED)
        
    def load_image(self, path):
        """Load and display the selected image."""
        try:
            self.source_image = Image.open(path)
            self.source_path = path
            
            # Update drop zone
            filename = os.path.basename(path)
            self.drop_zone.set_image(self.source_image, filename)
            
            # Update info
            w, h = self.source_image.size
            mode = self.source_image.mode
            self.image_info.config(text=f"{w}×{h} px • {mode}")
            
            # Update previews
            self.update_previews()
            
            # Set default output folder
            if not self.folder_entry.get():
                self.folder_entry.insert(0, os.path.dirname(path))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
            
    def update_previews(self):
        """Update preview images."""
        if not self.source_image:
            return
            
        for name, (label, display_size) in self.preview_slots.items():
            if name == 'favicon.ico':
                size = (48, 48)
            else:
                size = self.FAVICON_SIZES.get(name, (32, 32))
            
            # Create preview
            preview = self.prepare_image(self.source_image, size)
            preview = preview.resize((display_size, display_size), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(preview)
            self.preview_images[name] = photo
            label.config(image=photo, text="")
            
    def prepare_image(self, img, size):
        """Prepare image for a specific size."""
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        max_dim = max(img.size)
        square = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
        offset = ((max_dim - img.size[0]) // 2, (max_dim - img.size[1]) // 2)
        square.paste(img, offset)
        
        return square.resize(size, Image.Resampling.LANCZOS)
        
    def choose_color(self):
        """Open color chooser."""
        color = colorchooser.askcolor(color=self.bg_color, title="Choose Background Color")
        if color[1]:
            self.bg_color = color[1]
            self.color_preview.config(bg=self.bg_color)
            
    def select_output_folder(self):
        """Select output folder."""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
            
    def update_progress(self, value):
        """Update progress bar."""
        self.progress_canvas.delete("progress")
        width = self.progress_canvas.winfo_width()
        fill_width = width * (value / 100)
        
        if fill_width > 0:
            self.progress_canvas.create_rectangle(
                0, 0, fill_width, 6,
                fill=Colors.PRIMARY, outline="", tags="progress"
            )
            
    def generate_favicons(self):
        """Generate all favicon sizes."""
        if not self.source_image:
            messagebox.showwarning("No Image", "Please select a source image first.")
            return
            
        output_folder = self.folder_entry.get()
        if not output_folder:
            messagebox.showwarning("No Folder", "Please select an output folder.")
            return
            
        output_path = os.path.join(output_folder, "favicons")
        os.makedirs(output_path, exist_ok=True)
        
        thread = threading.Thread(target=self._generate_thread, args=(output_path,))
        thread.start()
        
    def _generate_thread(self, output_path):
        """Thread for generating favicons."""
        try:
            total = len(self.FAVICON_SIZES) + 3
            current = 0
            
            def update(step, status):
                self.root.after(0, lambda: self.update_progress((step/total)*100))
                self.root.after(0, lambda: self.status_label.config(text=status))
            
            # Generate PNGs
            for filename, size in self.FAVICON_SIZES.items():
                current += 1
                update(current, f"Generating {filename}...")
                
                img = self.prepare_image(self.source_image, size)
                
                if img.mode == 'RGBA':
                    bg = Image.new('RGB', size, self.bg_color)
                    bg.paste(img, mask=img.split()[3])
                    img = bg
                
                img.save(os.path.join(output_path, filename), quality=95)
            
            # Generate ICO
            current += 1
            update(current, "Generating favicon.ico...")
            
            ico_images = []
            for size in self.ICO_SIZES:
                img = self.prepare_image(self.source_image, size)
                if img.mode == 'RGBA':
                    bg = Image.new('RGB', size, self.bg_color)
                    bg.paste(img, mask=img.split()[3])
                    img = bg
                ico_images.append(img)
            
            ico_images[0].save(
                os.path.join(output_path, 'favicon.ico'),
                format='ICO',
                sizes=[(img.size[0], img.size[1]) for img in ico_images]
            )
            
            # Generate manifest
            current += 1
            update(current, "Generating site.webmanifest...")
            
            manifest = {
                "name": "",
                "short_name": "",
                "icons": [
                    {"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
                    {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}
                ],
                "theme_color": "#ffffff",
                "background_color": "#ffffff",
                "display": "standalone"
            }
            
            with open(os.path.join(output_path, 'site.webmanifest'), 'w') as f:
                json.dump(manifest, f, indent=2)
            
            # Update HTML
            current += 1
            update(current, "✓ Done!")
            
            html = '''<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="msapplication-TileColor" content="#da532c">
<meta name="theme-color" content="#ffffff">'''
            
            self.root.after(0, lambda: self._update_html(html))
            self.root.after(0, lambda: self.update_progress(100))
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", f"All favicons generated!\n\n{output_path}"
            ))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.status_label.config(text="Error"))
            
    def _update_html(self, html):
        """Update HTML snippet."""
        self.html_text.config(state=tk.NORMAL)
        self.html_text.delete('1.0', tk.END)
        self.html_text.insert('1.0', html)
        self.html_text.config(state=tk.DISABLED)
        
    def copy_html(self):
        """Copy HTML to clipboard."""
        self.html_text.config(state=tk.NORMAL)
        html = self.html_text.get('1.0', tk.END).strip()
        self.html_text.config(state=tk.DISABLED)
        
        self.root.clipboard_clear()
        self.root.clipboard_append(html)
        
        self.status_label.config(text="✓ Copied to clipboard!")
        self.root.after(2000, lambda: self.status_label.config(text="Ready"))


def main():
    root = tk.Tk()
    app = FaviconGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
