import argparse
import os.path
from typing import List, Iterable, Union

from seppl.io import locate_files
from wai.logging import LOGGING_WARNING

from idc.api import DATATYPES, data_type_to_class, ImageData
from idc.api import Reader
from pypdf import PdfReader


class PdfImageReader(Reader):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 data_type: str = None, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param data_type: the type of output to generate from the images
        :type data_type: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.data_type = data_type
        self._inputs = None
        self._current_input = None
        self._output_cls = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-pdf"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Extracts the images from the PDF file(s) and forwards them as the specified data type."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the PDF file(s) to extract the images from; glob syntax is supported", required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the PDF files to use", required=False, nargs="*")
        parser.add_argument("-t", "--data_type", choices=DATATYPES, type=str, default=None, help="The type of data to forward", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.source = ns.input
        self.source_list = ns.input_list
        self.data_type = ns.data_type

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        if self.data_type is None:
            return [ImageData]
        else:
            return [data_type_to_class(self.data_type)]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.data_type is None:
            raise Exception("No data type defined!")
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.pdf")
        self._output_cls = data_type_to_class(self.data_type)

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))
        reader = PdfReader(self.session.current_input)
        count = 0
        for page in reader.pages:
            for image_file_object in page.images:
                count += 1
                meta = {
                    "file": self.session.current_input,
                    "page": page.page_number,
                }
                yield self._output_cls(image_name=image_file_object.name, data=image_file_object.data, metadata=meta)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
