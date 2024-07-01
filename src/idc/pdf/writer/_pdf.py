import argparse
import os
from typing import List, Iterable

from wai.logging import LOGGING_WARNING

from idc.api import ImageData, BatchWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


class PdfImageWriter(BatchWriter):

    def __init__(self, output_dir: str = None, image_name_as_title: bool = None,
                 image_scale: float = None, metadata_keys: str = None,
                 offset_x: int = None, offset_y: int = None, gap: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param output_dir: the output directory to save the image/report in
        :type output_dir: str
        :param image_name_as_title: whether to use the image name as title for the image
        :type image_name_as_title: bool
        :param image_scale: the scale factor for images (1.0=100%)
        :type image_scale: float
        :param metadata_keys: the comma-separated list of meta-data keys to display below the image
        :type metadata_keys: str
        :param offset_x: the horizontal offset on the page
        :type offset_x: int
        :param offset_y: the vertical offset on the page
        :type offset_y: int
        :param gap: the vertical gap between title, image, meta-data
        :type gap: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_dir
        self.image_name_as_title = image_name_as_title
        self.image_scale = image_scale
        self.metadata_keys = metadata_keys
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.gap = gap

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-pdf"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the images in a PDF."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output_file", type=str, help="The PDF file to write the images to.", required=True)
        parser.add_argument("-t", "--image_name_as_title", action="store_true", help="Whether to use the image name as the title for the image.", required=False)
        parser.add_argument("-s", "--image_scale", type=float, help="The scale factor to apply to the image (1.0=100%%).", required=False, default=1.0)
        parser.add_argument("-m", "--metadata_keys", type=str, help="The keys of meta-data values to display below the image (comma-separated list).", required=False, default=None)
        parser.add_argument("-x", "--offset_x", type=int, help="The horizontal offset on the page.", required=False, default=50)
        parser.add_argument("-y", "--offset_y", type=int, help="The vertical offset on the page.", required=False, default=50)
        parser.add_argument("-g", "--gap", type=int, help="The vertical gap between title, image, meta-data.", required=False, default=50)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output_file
        self.image_name_as_title = ns.image_name_as_title
        self.image_scale = ns.image_scale
        self.metadata_keys = ns.metadata_keys
        self.offset_x = ns.offset_x
        self.offset_y = ns.offset_y
        self.gap = ns.gap

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        output_dir = os.path.dirname(self.output_file)
        if not os.path.exists(output_dir):
            self.logger().info("Creating output dir: %s" % output_dir)
            os.makedirs(output_dir)
        if self.image_name_as_title is None:
            self.image_name_as_title = False
        if self.image_scale is None:
            self.image_scale = 1.0
        if self.offset_x is None:
            self.offset_x = 50
        if self.offset_y is None:
            self.offset_y = 50
        if self.gap is None:
            self.gap = 50

    def write_batch(self, data: Iterable):
        """
        Saves the data in one go.

        :param data: the data to write
        :type data: Iterable
        """
        self.logger().info("Creating output file: %s" % self.output_file)
        pdf_canvas = canvas.Canvas(self.output_file, pagesize=A4)
        width, height = A4

        keys = None
        if self.metadata_keys is not None:
            keys = self.metadata_keys.split(",")

        for item in data:
            self.logger().info("Adding: %s" % item.image_name)

            y = height - self.offset_y
            x = self.offset_x

            # title
            if self.image_name_as_title:
                pdf_canvas.drawString(x, y, item.image_name)
                y -= self.gap

            # image
            img = item.image
            img_width, img_height = item.image_size
            if self.image_scale != 1.0:
                img_width = int(img_width * self.image_scale)
                img_height = int(img_height * self.image_scale)
                img = img.resize((img_width, img_height))
            y -= img_height
            pdf_canvas.drawImage(ImageReader(img), x, y, width=img_width, height=img_height, preserveAspectRatio=True)

            # metadata
            if (keys is not None) and (item.has_metadata()):
                y -= self.gap
                textobject = pdf_canvas.beginText(x, y)
                for key in keys:
                    meta = item.get_metadata()
                    if key in meta:
                        textobject.textLine("%s: %s" % (key, str(meta[key])))
                pdf_canvas.drawText(textobject)

            # page break
            pdf_canvas.showPage()

        pdf_canvas.save()
