"""Defines the ReferenceInterpreter class."""

from pathlib import Path

from . import scripts_handler


class ReferenceInterpreter():
    """Provides an API to interact with the reference interpreter."""

    @staticmethod
    def construct_reference(ref_type: type, ref_value):
        """Builds a reference's dictionary to use on the constructor of this class."""

        return {'type': ref_type, 'value': ref_value}

    def __init__(self, default_references: dict = dict()) -> None:
        """Initializes the interpreter with every reference information it needs."""
        
        # Gets the Scripts Handler
        self._scripts_handler = scripts_handler.get()

        # Defines the default references present in all interpreters.
        self._default_references = {
            '@HOME': {  # User's home
                'type': str,
                'value': str(Path.home())
            }
        }

        # For each reference in the additional default references...
        for reference in default_references:
            self._default_references[reference] = default_references[reference]

        # Initializes the custom references dictionary.
        self._references = dict()

    def run(self, document: dict | list, only_defaults: bool = False) -> dict | list:
        """Interprets and replaces all the references in the document."""

        def type_check(obj):
            # print(f'Testing {obj}')
            if isinstance(obj, str):
                return self._replace(obj, only_defaults)
            elif isinstance(obj, list):
                self.run(obj, only_defaults)
            elif isinstance(obj, dict):
                self.run(obj, only_defaults)
            return obj

        # print(f'Running on {document}.')
        # print(f'Type of document: {type(document)}.')
        if isinstance(document, dict):
            for key in document:
                document[key] = type_check(document[key])
        else:
            for index in range(len(document)):
                document[index] = type_check(document[index])
        return document
    
    
    def _replace(self, value: str, only_defaults: bool):
        """Interprets and replaces all the references in a string, also changing the value's type if possible"""

        # print(f'Received string {value}.')
        if value in self._default_references:
            ref_type = self._default_references[value]['type']
            return ref_type(self._default_references[value]['value'])
        for reference in self._default_references:
            while reference in value:
                value = value.replace(reference, self._default_references[reference]['value'])
        
        while '@SCRIPT{' in value:
            pos1 = value.find('@SCRIPT{') + 8
            pos2 = value.find('}', pos1)
            script_name = value[pos1:pos2]
            value = value.replace('@SCRIPT{' + script_name + '}', 
                                  self._scripts_handler.run_reference(script_name))

        if only_defaults:
            return value
        
        # TODO non-default references...
        return value

