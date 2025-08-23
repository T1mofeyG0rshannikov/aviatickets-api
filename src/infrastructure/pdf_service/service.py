import fitz

from src.application.dto.user_ticket import AdapterPdfField
from src.application.usecases.tickets.pdf.strategies.base import PdfServiceInterface
from src.infrastructure.pdf_service.exceptions import FileNotSetYetError


class PdfService(PdfServiceInterface):
    def set_file(self, file_path: str) -> None:
        self._file = fitz.open(file_path)

    def _get_file(self) -> fitz.Document:
        file = self._file
        if file is None:
            raise FileNotSetYetError("no file set in PdfService")

        return file

    def update_form(self, adapter_fields: list[AdapterPdfField]) -> None:
        adapter_fields_dict = {field.name: field.value for field in adapter_fields}

        for page in self._file:
            for field in page.widgets():
                if field.field_name in adapter_fields_dict:
                    field.field_value = adapter_fields_dict[field.field_name]
                    field.update()

    def merge_byte_files(self, files: list[bytes]) -> bytes:
        docs = [fitz.open(f"file{ind}", pdf) for ind, pdf in enumerate(files)]

        rects = [doc[0].rect for doc in docs]

        new_height = sum(rect.height for rect in rects)
        new_width = max(rect.width for rect in rects)

        merged = fitz.open()
        new_page = merged.new_page(width=new_width, height=new_height)

        height = 0
        for i in range(len(rects)):
            rect = rects[i]

            new_page.show_pdf_page(fitz.Rect(0, height, rect.width, rect.height + height), docs[i], 0)

            height += rect.height

        pdf_bytes = merged.write(garbage=4)
        merged.close()

        return pdf_bytes

    def flatten_pdf_to_bytes(self) -> bytes:
        doc = self._get_file()

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
