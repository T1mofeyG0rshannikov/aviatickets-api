import random
import string
from typing import List

import fitz

from src.usecases.tickets.pdf.adapter import AdapterPdfField


def generate_random_string(length=5) -> str:
    letters = string.ascii_uppercase
    return "".join(random.choice(letters) for _ in range(length))


class PdfService:
    def set_file(self, file_path: str) -> None:
        self._file = fitz.open(file_path)

    def update_form(self, adapter_fields: list[AdapterPdfField]) -> None:
        adapter_fields_dict = {field.name: field.value for field in adapter_fields}

        for page in self._file:
            for field in page.widgets():
                if field.field_name in adapter_fields_dict:
                    field.field_value = adapter_fields_dict[field.field_name]
                    field.update()

    def flatten_pdf_to_bytes(self) -> bytes:
        doc = self._file

        for page in doc:
            widgets = page.widgets()
            for widget in widgets:
                rect = widget.rect
                rect.x1 += 150
                rect.y1 += 150
                page.insert_textbox(
                    rect,
                    widget.field_value,
                    fontsize=widget.text_fontsize,
                    color=widget.text_color,
                    fontname=widget.text_font,
                    align=fitz.TEXT_ALIGN_LEFT,
                )
                page.delete_widget(widget)

        pdf_bytes = doc.write(garbage=4)
        doc.close()
        return pdf_bytes

    def save_file(self) -> bytes:
        return self.flatten_pdf_to_bytes()
