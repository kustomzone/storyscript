# -*- coding: utf-8 -*-
from .Bundle import Bundle
from .Story import Story
from .exceptions import StoryError


class StoryscriptCompilationResult:
    """
    Result of a Storyscript compilation.
    Contains the compiled story or a list of compilation errors.
    """

    def __init__(self, result, errors):
        self._result = result
        self._errors = errors
        self._deprecations = []
        self._warnings = []

    @classmethod
    def from_result(cls, story):
        """
        Creates a CompilationResult from a result.
        """
        return cls(story, errors=[])

    @classmethod
    def from_error(cls, error):
        """
        Creates a CompilationResult from a single error.
        """
        return cls(None, errors=[error])

    def result(self):
        """
        Returns the compiled story.
        """
        return self._result

    def errors(self):
        """
        Returns a list of all errorsemitted by the Storyscript compiler.
        """
        return self._errors

    def warnings(self):
        """
        Returns a list of all warnings emitted by the Storyscript compiler.
        """
        return self._warnings

    def deprecations(self):
        """
        Returns a list of all deprecations emitted by the Storyscript compiler.
        """
        return self._deprecations

    def success(self):
        """
        Returns `True` if the compilation succeeded.
        """
        return self._result is not None

    def check_success(self):
        """
        Throws the first error encountered if the compilation did not succeed.
        """
        if len(self._errors) > 0:
            raise self._errors[0]


class Api:
    """
    Exposes functionalities for external use
    """
    @staticmethod
    def loads(string, debug=False):
        """
        Load story from a string.
        """
        try:
            s = Story(string).process()
            return StoryscriptCompilationResult.from_result(s)
        except StoryError as e:
            return StoryscriptCompilationResult.from_error(e)
        except Exception as e:
            if debug:
                raise e
            else:
                e = StoryError.internal_error(e)
                return StoryscriptCompilationResult.from_error(e)

    @staticmethod
    def load(stream, debug=False):
        """
        Load story from a file stream.
        """
        try:
            story = Story.from_stream(stream).process()
            s = {stream.name: story, 'services': story['services']}
            return StoryscriptCompilationResult.from_result(s)
        except StoryError as e:
            return StoryscriptCompilationResult.from_error(e)
        except Exception as e:
            if debug:
                raise e
            else:
                e = StoryError.internal_error(e)
                return StoryscriptCompilationResult.from_error(e)

    @staticmethod
    def load_map(files, debug=False):
        """
        Load multiple stories from a file mapping
        """
        try:
            s = Bundle(story_files=files).bundle()
            return StoryscriptCompilationResult.from_result(s)
        except StoryError as e:
            return StoryscriptCompilationResult.from_error(e)
        except Exception as e:
            if debug:
                raise e
            else:
                e = StoryError.internal_error(e)
                return StoryscriptCompilationResult.from_error(e)
