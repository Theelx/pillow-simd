import io
import os
import os.path
import tempfile
import time

import pytest
from PIL import Image, PdfParser

from .helper import PillowTestCase, hopper


class TestFilePdf(PillowTestCase):
    def helper_save_as_pdf(self, mode, **kwargs):
        # Arrange
        im = hopper(mode)
        outfile = self.tempfile("temp_" + mode + ".pdf")

        # Act
        im.save(outfile, **kwargs)

        # Assert
        assert os.path.isfile(outfile)
        assert os.path.getsize(outfile) > 0
        with PdfParser.PdfParser(outfile) as pdf:
            if kwargs.get("append_images", False) or kwargs.get("append", False):
                assert len(pdf.pages) > 1
            else:
                assert len(pdf.pages) > 0
        with open(outfile, "rb") as fp:
            contents = fp.read()
        size = tuple(
            int(d)
            for d in contents.split(b"/MediaBox [ 0 0 ")[1].split(b"]")[0].split()
        )
        assert im.size == size

        return outfile

    def test_monochrome(self):
        # Arrange
        mode = "1"

        # Act / Assert
        self.helper_save_as_pdf(mode)

    def test_greyscale(self):
        # Arrange
        mode = "L"

        # Act / Assert
        self.helper_save_as_pdf(mode)

    def test_rgb(self):
        # Arrange
        mode = "RGB"

        # Act / Assert
        self.helper_save_as_pdf(mode)

    def test_p_mode(self):
        # Arrange
        mode = "P"

        # Act / Assert
        self.helper_save_as_pdf(mode)

    def test_cmyk_mode(self):
        # Arrange
        mode = "CMYK"

        # Act / Assert
        self.helper_save_as_pdf(mode)

    def test_unsupported_mode(self):
        im = hopper("LA")
        outfile = self.tempfile("temp_LA.pdf")

        with pytest.raises(ValueError):
            im.save(outfile)

    def test_save_all(self):
        # Single frame image
        self.helper_save_as_pdf("RGB", save_all=True)

        # Multiframe image
        with Image.open("Tests/images/dispose_bgnd.gif") as im:

            outfile = self.tempfile("temp.pdf")
            im.save(outfile, save_all=True)

            assert os.path.isfile(outfile)
            assert os.path.getsize(outfile) > 0

            # Append images
            ims = [hopper()]
            im.copy().save(outfile, save_all=True, append_images=ims)

            assert os.path.isfile(outfile)
            assert os.path.getsize(outfile) > 0

            # Test appending using a generator
            def imGenerator(ims):
                yield from ims

            im.save(outfile, save_all=True, append_images=imGenerator(ims))

        assert os.path.isfile(outfile)
        assert os.path.getsize(outfile) > 0

        # Append JPEG images
        with Image.open("Tests/images/flower.jpg") as jpeg:
            jpeg.save(outfile, save_all=True, append_images=[jpeg.copy()])

        assert os.path.isfile(outfile)
        assert os.path.getsize(outfile) > 0

    def test_multiframe_normal_save(self):
        # Test saving a multiframe image without save_all
        with Image.open("Tests/images/dispose_bgnd.gif") as im:

            outfile = self.tempfile("temp.pdf")
            im.save(outfile)

        assert os.path.isfile(outfile)
        assert os.path.getsize(outfile) > 0

    def test_pdf_open(self):
        # fail on a buffer full of null bytes
        with pytest.raises(PdfParser.PdfFormatError):
            PdfParser.PdfParser(buf=bytearray(65536))

        # make an empty PDF object
        with PdfParser.PdfParser() as empty_pdf:
            assert len(empty_pdf.pages) == 0
            assert len(empty_pdf.info) == 0
            assert not empty_pdf.should_close_buf
            assert not empty_pdf.should_close_file

        # make a PDF file
        pdf_filename = self.helper_save_as_pdf("RGB")

        # open the PDF file
        with PdfParser.PdfParser(filename=pdf_filename) as hopper_pdf:
            assert len(hopper_pdf.pages) == 1
            assert hopper_pdf.should_close_buf
            assert hopper_pdf.should_close_file

        # read a PDF file from a buffer with a non-zero offset
        with open(pdf_filename, "rb") as f:
            content = b"xyzzy" + f.read()
        with PdfParser.PdfParser(buf=content, start_offset=5) as hopper_pdf:
            assert len(hopper_pdf.pages) == 1
            assert not hopper_pdf.should_close_buf
            assert not hopper_pdf.should_close_file

        # read a PDF file from an already open file
        with open(pdf_filename, "rb") as f:
            with PdfParser.PdfParser(f=f) as hopper_pdf:
                assert len(hopper_pdf.pages) == 1
                assert hopper_pdf.should_close_buf
                assert not hopper_pdf.should_close_file

    def test_pdf_append_fails_on_nonexistent_file(self):
        im = hopper("RGB")
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(IOError):
                im.save(os.path.join(temp_dir, "nonexistent.pdf"), append=True)

    def check_pdf_pages_consistency(self, pdf):
        pages_info = pdf.read_indirect(pdf.pages_ref)
        assert b"Parent" not in pages_info
        assert b"Kids" in pages_info
        kids_not_used = pages_info[b"Kids"]
        for page_ref in pdf.pages:
            while True:
                if page_ref in kids_not_used:
                    kids_not_used.remove(page_ref)
                page_info = pdf.read_indirect(page_ref)
                assert b"Parent" in page_info
                page_ref = page_info[b"Parent"]
                if page_ref == pdf.pages_ref:
                    break
            assert pdf.pages_ref == page_info[b"Parent"]
        assert kids_not_used == []

    def test_pdf_append(self):
        # make a PDF file
        pdf_filename = self.helper_save_as_pdf("RGB", producer="PdfParser")

        # open it, check pages and info
        with PdfParser.PdfParser(pdf_filename, mode="r+b") as pdf:
            assert len(pdf.pages) == 1
            assert len(pdf.info) == 4
            assert pdf.info.Title == os.path.splitext(os.path.basename(pdf_filename))[0]
            assert pdf.info.Producer == "PdfParser"
            assert b"CreationDate" in pdf.info
            assert b"ModDate" in pdf.info
            self.check_pdf_pages_consistency(pdf)

            # append some info
            pdf.info.Title = "abc"
            pdf.info.Author = "def"
            pdf.info.Subject = "ghi\uABCD"
            pdf.info.Keywords = "qw)e\\r(ty"
            pdf.info.Creator = "hopper()"
            pdf.start_writing()
            pdf.write_xref_and_trailer()

        # open it again, check pages and info again
        with PdfParser.PdfParser(pdf_filename) as pdf:
            assert len(pdf.pages) == 1
            assert len(pdf.info) == 8
            assert pdf.info.Title == "abc"
            assert b"CreationDate" in pdf.info
            assert b"ModDate" in pdf.info
            self.check_pdf_pages_consistency(pdf)

        # append two images
        mode_CMYK = hopper("CMYK")
        mode_P = hopper("P")
        mode_CMYK.save(pdf_filename, append=True, save_all=True, append_images=[mode_P])

        # open the PDF again, check pages and info again
        with PdfParser.PdfParser(pdf_filename) as pdf:
            assert len(pdf.pages) == 3
            assert len(pdf.info) == 8
            assert PdfParser.decode_text(pdf.info[b"Title"]) == "abc"
            assert pdf.info.Title == "abc"
            assert pdf.info.Producer == "PdfParser"
            assert pdf.info.Keywords == "qw)e\\r(ty"
            assert pdf.info.Subject == "ghi\uABCD"
            assert b"CreationDate" in pdf.info
            assert b"ModDate" in pdf.info
            self.check_pdf_pages_consistency(pdf)

    def test_pdf_info(self):
        # make a PDF file
        pdf_filename = self.helper_save_as_pdf(
            "RGB",
            title="title",
            author="author",
            subject="subject",
            keywords="keywords",
            creator="creator",
            producer="producer",
            creationDate=time.strptime("2000", "%Y"),
            modDate=time.strptime("2001", "%Y"),
        )

        # open it, check pages and info
        with PdfParser.PdfParser(pdf_filename) as pdf:
            assert len(pdf.info) == 8
            assert pdf.info.Title == "title"
            assert pdf.info.Author == "author"
            assert pdf.info.Subject == "subject"
            assert pdf.info.Keywords == "keywords"
            assert pdf.info.Creator == "creator"
            assert pdf.info.Producer == "producer"
            assert pdf.info.CreationDate == time.strptime("2000", "%Y")
            assert pdf.info.ModDate == time.strptime("2001", "%Y")
            self.check_pdf_pages_consistency(pdf)

    def test_pdf_append_to_bytesio(self):
        im = hopper("RGB")
        f = io.BytesIO()
        im.save(f, format="PDF")
        initial_size = len(f.getvalue())
        assert initial_size > 0
        im = hopper("P")
        f = io.BytesIO(f.getvalue())
        im.save(f, format="PDF", append=True)
        assert len(f.getvalue()) > initial_size
