"""Base class for commands.  Handles parsing supplied arguments."""

import getopt
import sys
import binascii

__author__    = "Moxie Marlinspike"
__license__   = "GPLv3"
__copyright__ = "Copyright 2012, Moxie Marlinspike"

class Command:

    def __init__(self, argv, options, flags, allowArgRemainder=False):
        try:
            self.flags                     = flags
            self.options                   = ":".join(options) + ":"
            self.values, self.argRemainder = getopt.getopt(argv, self.options + self.flags)

            if not allowArgRemainder and self.argRemainder:
                self.printError("Too many arguments: %s" % self.argRemainder)
        except getopt.GetoptError as e:
            self.printError(e)

    def _getOptionValue(self, flag):
        for option, value in self.values:
            if option == flag:
                return value

        return None

    def _containsOption(self, flag):
        for option, value in self.values:
            if option == flag:
                return True

    def _getInputFile(self):
        inputFile = self._getOptionValue("-i")

        if not inputFile:
            self.printError("Missing input file (-i)")

        return inputFile

    def _checkForChalResp(self):
        if self._containsOption("-C") and self._containsOption("-R"):
                return True
        return None


    def _getCmdChal(self):
        if not self._checkForChalResp:
                self.printError("No Challenge or Response Specificed!")

        cmdline_chal = self._getOptionValue("-C")
        if len(cmdline_chal) != 23:
                self.printError("Invalid Challenge Length")
        return binascii.unhexlify(cmdline_chal.replace(":", ""))

    def _getCmdResp(self):
        if not self._checkForChalResp:
                self.printError("No Challenge or Response Specificed!")

        cmdline_resp = self._getOptionValue("-R")

        if len(cmdline_resp) != 71:
                self.printError("Invalid Response Length")
        return binascii.unhexlify(cmdline_resp.replace(":",""))


    def printError(self, error):
        sys.stderr.write("ERROR: %s\n" % error)
        sys.exit(-1)
