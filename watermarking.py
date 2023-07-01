from tkinter import Label, Image, filedialog as fd
from PIL import ImageTk, Image, ImageDraw, ImageFont


class ImageBox(Label):
    def __init__(self, root, *args, **kwargs):

        super().__init__(root, *args, **kwargs)

        self.grey_image = None

        self.display_size = (640, 480)

        self.grey_image = Image.new(size=self.display_size, mode="RGBA", color="grey")
        self.grey_photo = ImageTk.PhotoImage(self.grey_image)
        self.config(image=self.grey_photo)


class Watermark:
    def __init__(self, text="", color=(255, 255, 255, 255), font_size=30, x=0.5, y=0.5, rotation=0, opacity=150, font = "arial.ttf"):
        self.text = text
        self.color = color
        self.font_size = font_size
        self.x = x
        self.y = y
        self.rotation = rotation
        self.opacity = opacity
        self.font = font

    def set_opacity(self, value):
        self.opacity = int(value)
        self.color = (self.color[0], self.color[1], self.color[2], self.opacity)

    def move_up(self):
        self.y -= 0.01
    def move_down(self):
        self.y += 0.01
    def move_left(self):
        self.x -= 0.01
    def move_right(self):
        self.x += 0.01
    def rotate_left(self):
        self.rotation += 10
    def rotate_right(self):
        self.rotation -= 10


class WatermarkImage(Label):
    def __init__(self, root, image_box_instance, orig_img, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.shown_img = None
        self.original_img = None

        self.clean_original = orig_img.convert('RGBA')

        self.clean_shown = orig_img.convert('RGBA')
        width, height = self.clean_shown.size
        window_width = 640
        window_height = 480
        if width > window_width or height > window_height:
            ratio = min(window_width / width, window_height / height)
            self.clean_shown = self.clean_shown.resize((int(width * ratio), int(height * ratio)), Image.LANCZOS)

        self.watermark_instance = Watermark()
        self.image_box_instance = image_box_instance


    def update_image(self):
        self.shown_img = self.apply_watermark(self.clean_shown, self.watermark_instance.text)

        shown_img = ImageTk.PhotoImage(self.shown_img)
        self.image_box_instance.config(image=shown_img)
        self.image_box_instance.image = shown_img  # garbage collection

        self.original_img = self.apply_watermark(self.clean_original, self.watermark_instance.text)

    def apply_watermark(self, image, text_entry):
        img = image.copy()
        width, height = img.size

        watermark_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_image)

        font_size = int(self.watermark_instance.font_size / 100 * height)
        font = ImageFont.truetype(self.watermark_instance.font, size=font_size)

        text_width, text_height = draw.textsize(text_entry, font=font)
        text_position = (int((self.watermark_instance.x - text_width / 2 / width) * width), int((self.watermark_instance.y - text_height / 2 / height) * height))

        draw.text(text_position, text_entry, font=font, fill=self.watermark_instance.color)

        # Rotate the watermark image
        watermark_image = watermark_image.rotate(self.watermark_instance.rotation, expand=1)

        rotated_watermark_image = Image.new('RGBA', img.size)
        rotated_watermark_image.paste(watermark_image, (int((width - watermark_image.width) / 2), int((height - watermark_image.height) / 2)))

        img = Image.alpha_composite(img, rotated_watermark_image)

        return img

    def save_image(self):
        print("Saving image...")
        file_path = fd.asksaveasfilename(defaultextension='.png', filetypes=[("PNG Image", '*.png'), ("JPEG Image", '*.jpg'), ("All Files", '*.*')])
        if file_path:
            if self.original_img is not None:
                if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                    self.original_img.save(file_path, quality=100)
                else:
                    self.original_img.save(file_path)
