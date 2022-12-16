import os
from io import BytesIO
from typing import Tuple

from PIL import Image as PillowImage

from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.db import models

from api.core.models import CommonModel
from api.users.models import User


class ResizableImageFieldFile(models.ImageField.attr_class):
    EXTENSIONS = {
        ".blp": "BLP",
        ".bmp": "BMP",
        ".dib": "DIB",
        ".bufr": "BUFR",
        ".cur": "CUR",
        ".pcx": "PCX",
        ".dcx": "DCX",
        ".dds": "DDS",
        ".ps": "EPS",
        ".eps": "EPS",
        ".fit": "FITS",
        ".fits": "FITS",
        ".fli": "FLI",
        ".flc": "FLI",
        ".ftc": "FTEX",
        ".ftu": "FTEX",
        ".gbr": "GBR",
        ".gif": "GIF",
        ".grib": "GRIB",
        ".h5": "HDF5",
        ".hdf": "HDF5",
        ".png": "PNG",
        ".apng": "PNG",
        ".jp2": "JPEG2000",
        ".j2k": "JPEG2000",
        ".jpc": "JPEG2000",
        ".jpf": "JPEG2000",
        ".jpx": "JPEG2000",
        ".j2c": "JPEG2000",
        ".icns": "ICNS",
        ".ico": "ICO",
        ".im": "IM",
        ".iim": "IPTC",
        ".tif": "TIFF",
        ".tiff": "TIFF",
        ".jfif": "JPEG",
        ".jpe": "JPEG",
        ".jpg": "JPEG",
        ".jpeg": "JPEG",
        ".mpg": "MPEG",
        ".mpeg": "MPEG",
        ".mpo": "MPO",
        ".msp": "MSP",
        ".palm": "PALM",
        ".pcd": "PCD",
        ".pdf": "PDF",
        ".pxr": "PIXAR",
        ".pbm": "PPM",
        ".pgm": "PPM",
        ".ppm": "PPM",
        ".pnm": "PPM",
        ".psd": "PSD",
        ".bw": "SGI",
        ".rgb": "SGI",
        ".rgba": "SGI",
        ".sgi": "SGI",
        ".ras": "SUN",
        ".tga": "TGA",
        ".icb": "TGA",
        ".vda": "TGA",
        ".vst": "TGA",
        ".webp": "WEBP",
        ".wmf": "WMF",
        ".emf": "WMF",
        ".xbm": "XBM",
        ".xpm": "XPM",
    }

    def resize(self, size: Tuple[int, int]) -> None:
        if (self.width, self.height) != size:
            self._resize(size)

    def _resize(self, size: Tuple[int, int]) -> None:
        if self.closed:
            self.open()

        image = PillowImage.open(self.file)
        filename = os.path.split(self.file.name)[-1]
        extension = os.path.splitext(filename)[1].lower()
        resized_image = image.resize(size)
        stream = BytesIO()
        resized_image.save(stream, format=self.EXTENSIONS[extension])

        self.delete(save=False)
        self.save(name=filename, content=ContentFile(stream.getvalue()), save=False)


class ResizableImageField(models.ImageField):
    attr_class = ResizableImageFieldFile

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Image(CommonModel):
    title = models.CharField(max_length=120)
    width = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    height = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    file = ResizableImageField(upload_to="images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self})>"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        self.file.resize((self.width, self.height))
        super().save(*args, **kwargs)
