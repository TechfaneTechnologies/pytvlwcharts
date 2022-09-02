# -*- coding: utf-8 -*-
"""
    generateTypes.py
    An Experimental Python Wrapper For Tradingview's Lightweight-Charts
    A tool to generate type definitions for all the charting options.
    :url: https://tradingview.github.io/lightweight-charts/
    :copyright: (c) 2021 by Techfane Technologies Pvt. Ltd.
    :license: see LICENSE for details.
    :author: Dr June Moone
    :created: On Friday September 02, 2022 19:47:13 GMT+05:30
"""
__author__ = "Dr June Moone"
__webpage__ = "https://github.com/MooneDrJune"
__github__ = "https://github.com/TechfaneTechnologies/PyTvLwCharts"
__license__ = "MIT"

from absl import app
from absl import flags
import dataclasses
import jinja2
import json
import keyword
import textwrap
from typing import Dict, List, Set, Tuple

_FLAG_OUTPUT = flags.DEFINE_string('output',
                                   None,
                                   help='Path to write the generated types.',
                                   required=True)

_FLAG_SCHEMA = flags.DEFINE_string('schema',
                                   None,
                                   help='JSON schema file.',
                                   required=True)

_CONTENT_TEMPLATE = jinja2.Template(
    '''"""
    generated_models.py
    An Experimental Python Wrapper For Tradingview's Lightweight-Charts
    Generated With generateTypes.py. DO NOT MODIFY
    :url: https://tradingview.github.io/lightweight-charts/
    :copyright: (c) 2021 by Techfane Technologies Pvt. Ltd.
    :license: see LICENSE for details.
    :author: Dr June Moone
    :created: On Friday September 02, 2022 19:47:13 GMT+05:30
"""

from apischema import alias
from apischema import serialize
from dataclasses import field
from dataclasses import dataclass
import enum
import json
from typing import Any, Optional, Union


class JsonOptions:
  def to_json(self):
    return json.dumps(serialize(self, exclude_none=True), indent=2)


{{ types }}
''')

# Template for a data type definition.
_TYPE_TEMPLATE = jinja2.Template('''
@dataclass
class {{ name }}(JsonOptions):
  """{{ description }}

  Attributes:
{{ attribute_desc_list }}
  """
{{ attribute_list }}

''')

# Template for a type union definition (AnyOf).
_UNION_TEMPLATE = jinja2.Template('''
# {{ description }}
{{ name }} = Union[{{ any_of }}]

''')

# Template for an enum.
_ENUM_TEMPLATE = jinja2.Template('''
class {{ name }}(enum.{{ enum_class }}):
  """{{ description }}"""

  {{ member_list }}

''')

# Template for an alias.
_ALIAS_TEMPLATE = jinja2.Template('''
# {{ description }}
{{ name }} = {{ alias }}

''')


def format_description(description: str, indentation: int = 0) -> str:
  return textwrap.indent(' '.join(
      line.strip() for line in description.split('\n') if line.strip()),
                         prefix=' ' * indentation)


def as_identifier_name(value: str) -> str:
  """Produce a valid snake cased identifier name."""
  identifier = ''.join(
      '_' + c.lower() if c.isupper() else c for c in value).lstrip('_')
  if keyword.iskeyword(identifier):
    return f'{identifier}_'
  return identifier


@dataclasses.dataclass
class TypeDefinition:
  """A Python type definition."""
  name: str
  dependencies: List[str]
  code: str


@dataclasses.dataclass
class FieldDefinition:
  name: str
  description: str
  type: str
  value: str


@dataclasses.dataclass
class PartialEnumDefinition:
  """"""
  name: str
  members: List[FieldDefinition]


def type_name(definition) -> Tuple[str, str]:
  if 'type' in definition:
    return {
        'string': 'str',
        'boolean': 'bool',
        'number': 'int'
    }[definition['type']], []
  if '$ref' in definition:
    name = definition['$ref'].rsplit('/', maxsplit=1)[-1]
    return name, [name]
  if 'anyOf' in definition:
    dependencies = []
    type_names = []
    for alternative_type_name in definition['anyOf']:
      alternative_name, alternative_dependencies = type_name(
          alternative_type_name)
      type_names.append(alternative_name)
      dependencies.extend(alternative_dependencies)
    return f"Union[{', '.join(type_names)}]", dependencies


def generate_type(name: str, definition) -> TypeDefinition:
  """Generate a type definition."""
  type_dependencies = []
  attribute_desc_list = []
  attribute_list = []
  for property_name, property_definition in definition['properties'].items():
    property_python_name = as_identifier_name(property_name)
    property_type_name, property_dependencies = type_name(property_definition)

    # Check whether this is a "constant".
    if property_type_name and '.' in property_type_name:
      property_type_name, value = property_type_name.split('.', maxsplit=1)
      value = f'{property_type_name}.{as_identifier_name(value)}'
      property_type_definition = property_type_name
      type_dependencies.append(property_type_name)
    else:
      value = 'None'
      property_type_definition = f'Optional[{property_type_name}]'
      type_dependencies.extend(property_dependencies)

    attribute_desc_list.append(
        format_description(
            f'{property_python_name}: {property_definition.get("description", "")}',
            indentation=4))

    if property_python_name != property_name:
      value = f"field(default={value}, metadata=alias('{property_name}'))"
    attribute_list.append(
        f'  {property_python_name}: {property_type_definition} = {value}')

  # Render the code definition snippet.
  code = _TYPE_TEMPLATE.render(
      name=name,
      description=definition.get('description', name),
      attribute_desc_list='\n'.join(attribute_desc_list),
      attribute_list='\n'.join(attribute_list))

  return TypeDefinition(name=name, dependencies=type_dependencies, code=code)


def generate_anyof_type(name: str, definition) -> TypeDefinition:
  """Generate a type alias for an anyof definition."""
  dependencies = []
  alternatives = []
  for type_option in definition['anyOf']:
    option_type_name, option_dependencies = type_name(type_option)
    dependencies.extend(option_dependencies)
    alternatives.append(option_type_name)
  return TypeDefinition(name=name,
                        dependencies=dependencies,
                        code=_UNION_TEMPLATE.render(
                            name=name,
                            description=format_description(
                                definition.get('description', name)),
                            any_of=', '.join(alternatives)))


def generate_enum_type(name: str, definition) -> TypeDefinition:
  """Generate an enum definition."""
  is_int_enum = definition['type'] == 'number'
  # TODO: we don't get the member names, touch this up manually.
  member_list = [
      f'{name.upper()}_{value} = {value}'
      if is_int_enum else f"{as_identifier_name(value)} = '{value}'"
      for value in definition['enum']
  ]
  return TypeDefinition(name=name,
                        dependencies=[],
                        code=_ENUM_TEMPLATE.render(
                            name=name,
                            description=definition.get('description', name),
                            enum_class='IntEnum' if is_int_enum else 'Enum',
                            member_list='\n  '.join(member_list)))


def generate_enum_type_from_partial(
    definition: PartialEnumDefinition) -> TypeDefinition:
  member_list = [
      f'# {member.description}\n  {as_identifier_name(member.name)} = {member.value}'
      for member in definition.members
  ]
  return TypeDefinition(name=definition.name,
                        dependencies=[],
                        code=_ENUM_TEMPLATE.render(
                            name=definition.name,
                            description=definition.name,
                            enum_class='Enum',
                            member_list='\n\n  '.join(member_list)))


def extend_enum_partial_type(
    name: str, definition,
    partial_enum_definitions: Dict[str, PartialEnumDefinition]):
  name, member = name.split('.')
  partial_enum_definition = partial_enum_definitions.get(
      name, PartialEnumDefinition(name=name, members=[]))

  # Add member definition.
  assert len(definition['enum']) == 1
  assert definition['type'] == 'string'
  partial_enum_definition.members.append(
      FieldDefinition(name=member,
                      description=definition.get('description', name),
                      type='str',
                      value=f"'{definition['enum'][0]}'"))
  partial_enum_definitions[name] = partial_enum_definition


def generate_type_alias(name: str, definition) -> TypeDefinition:
  """Generate a type alias."""
  alias_name, dependencies = type_name(definition)
  return TypeDefinition(name=name,
                        dependencies=dependencies,
                        code=_ALIAS_TEMPLATE.render(
                            name=name,
                            description=format_description(
                                definition.get('description', name)),
                            alias=alias_name))


def generate_type_definitions(root_type_name: str,
                              schema) -> List[TypeDefinition]:
  """Generate all type definitions."""
  definitions: List[TypeDefinition] = []
  partial_definitions: Dict[str, PartialEnumDefinition] = {}
  for name, definition in schema['definitions'].items():
    if 'properties' in definition:
      definitions.append(generate_type(name, definition))
    elif 'anyOf' in definition:
      definitions.append(generate_anyof_type(name, definition))
    elif 'enum' in definition:
      if '.' in name:
        # This is a split out enum definition.
        extend_enum_partial_type(name, definition, partial_definitions)
      else:
        definitions.append(generate_enum_type(name, definition))
    elif '$ref' in definition:
      # An alias.
      definitions.append(generate_type_alias(name, definition))
    else:
      print(f'Skip {name}')
      definitions.append(
          TypeDefinition(name=name,
                         dependencies=[],
                         code=_ALIAS_TEMPLATE.render(
                             name=name,
                             description=format_description(
                                 definition.get('description', name)),
                             alias='Any')))

  # Finalize partial types.
  definitions.extend(
      map(generate_enum_type_from_partial, partial_definitions.values()))

  # Add root type.
  definitions.append(generate_type(root_type_name, schema))

  return definitions


def toposort(type_definitions: List[TypeDefinition]) -> List[TypeDefinition]:
  """Topologically sort a list of type definitions."""

  def visit(type_definition: TypeDefinition, visited: Set[str],
            dependencies: Dict[str,
                               TypeDefinition], result: List[TypeDefinition]):
    visited.add(type_definition.name)
    for dependency_name in type_definition.dependencies:
      if dependency_name not in visited:
        visited.add(dependency_name)
        if dependency_name in dependencies:
          visit(type_definition=dependencies[dependency_name],
                visited=visited,
                dependencies=dependencies,
                result=result)
    result.append(type_definition)

  graph = {definition.name: definition for definition in type_definitions}
  ordered_types = []
  visited = set()
  for type_definition in type_definitions:
    if type_definition.name not in visited:
      visit(type_definition, visited, graph, ordered_types)
  return ordered_types


def assemble(type_definitions: List[TypeDefinition]) -> str:
  """Assemble the Python file."""
  type_definitions = {
      type_definition.name: type_definition
      for type_definition in type_definitions
  }.values()
  return _CONTENT_TEMPLATE.render(types='\n'.join(
      definition.code for definition in toposort(type_definitions)))


def main(_):
  type_name, schema_file = _FLAG_SCHEMA.value.split(':', maxsplit=1)
  schema = json.load(open(schema_file, encoding='utf8'))
  type_definitions = generate_type_definitions(root_type_name=type_name,
                                               schema=schema)
  with open(_FLAG_OUTPUT.value, 'w') as f:
    f.write(assemble(type_definitions))


if __name__ == '__main__':
  app.run(main)
