import segno, io
from aiogram import types


class QrGenerator:
    def __init__(self):
        self.qrcode = None
        self.buffer = None
        self.image_data = None

    async def __generate(self, payload):
        self.qrcode = segno.make_qr(content=payload, error="H")
        
    async def __write_qr_data(self, _format: str = "PNG"):
        self.buffer = io.BytesIO()

        with self.buffer as f:     
            self.buffer.truncate()
            self.qrcode.save(f, kind=_format, scale=10)
            self.buffer.seek(0)
            self.image_data = self.buffer.read()

    async def generate(self, payload: str, use_buffered_input_file: bool = True, _format: str = "PNG") -> types.BufferedInputFile | bytes:
        await self.__generate(payload)
        await self.__write_qr_data(_format)
        
        data = self.image_data
        self.image_data = None

        return types.BufferedInputFile(data, filename='image.png') if use_buffered_input_file \
            else data
        

qr_genetator = QrGenerator()