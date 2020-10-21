from dataclasses import dataclass
from typing import Dict
from jinja2 import Template


@dataclass
class DefaultTemplater(object):
    """ Allow to inject data in a jinja2 templated file and write the result to specified destination """

    source: str
    destination: str

    def render(self, data: Dict) -> None:
        """ Write template from source filled with data to destination
        Args:
        data: the data to inject in the template 
        """
        self.load_template()
        filled_template = self.replace(data)
        self.write_filled_template(filled_template)

    def load_template(self) -> None:
        """ Load template from source
        """
        with open(self.source, "r") as f:
            self.template = f.read()

    def replace(self, values: Dict) -> str:
        """ Replace tag in template with values
        Args: 
        values: dict with key: tag to search in template, value: value to replace the tag
        """
        template = Template(self.template)
        templated = template.render(**values)
        return templated

    def write_filled_template(self, content: str):
        """Write the result of the template and injected value to destination
        Args:
        content: what to write
        """
        with open(self.destination, "w") as f:
            f.write(content)