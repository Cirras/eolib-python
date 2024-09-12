from protocol_code_generator.type.blob_type import BlobType
from protocol_code_generator.type.bool_type import BoolType
from protocol_code_generator.type.enum_type import EnumType, EnumValue
from protocol_code_generator.type.has_underlying_type import HasUnderlyingType
from protocol_code_generator.type.integer_type import IntegerType
from protocol_code_generator.type.length import Length
from protocol_code_generator.type.string_type import StringType
from protocol_code_generator.type.struct_type import StructType
from protocol_code_generator.util.number_utils import try_parse_int
from protocol_code_generator.util.xml_utils import (
    get_instructions,
    get_required_string_attribute,
    get_string_attribute,
    get_text,
)


class TypeFactory:
    def __init__(self):
        self.unresolved_types = {}
        self.types = {}

    def get_type(self, name: str, length=None):
        if not length:
            length = Length.unspecified()
        if length.specified:
            return TypeFactory._create_type_with_specified_length(name, length)
        if name not in self.types:
            self.types[name] = self._create_type(name, length)
        return self.types[name]

    def define_custom_type(self, protocol_type, source_path):
        name = get_required_string_attribute(protocol_type, "name")
        if name in self.unresolved_types:
            return False
        self.unresolved_types[name] = UnresolvedCustomType(protocol_type, source_path)
        return True

    def clear(self):
        self.unresolved_types.clear()
        self.types.clear()

    def _create_type(self, name, length):
        underlying_type = self._read_underlying_type(name)
        if underlying_type is not None:
            name = name[: name.index(":")]

        result = None

        if name in ["byte", "char"]:
            result = IntegerType(name, 1)
        elif name == "short":
            result = IntegerType(name, 2)
        elif name == "three":
            result = IntegerType(name, 3)
        elif name == "int":
            result = IntegerType(name, 4)
        elif name == "bool":
            if underlying_type is None:
                underlying_type = self.get_type("char")
            result = BoolType(underlying_type)
        elif name in ["string", "encoded_string"]:
            result = StringType(name, length)
        elif name == "blob":
            result = BlobType()
        else:
            result = self._create_custom_type(name, underlying_type)

        if underlying_type is not None and not isinstance(result, HasUnderlyingType):
            raise RuntimeError(
                f"{result.name} has no underlying type, so {underlying_type.name} is not allowed "
                + "as an underlying type override."
            )

        return result

    def _read_underlying_type(self, name):
        parts = name.split(":")

        if len(parts) == 1:
            return None
        elif len(parts) == 2:
            type_name, underlying_type_name = parts
            if type_name == underlying_type_name:
                raise RuntimeError(f"{type_name} type cannot specify itself as an underlying type.")
            underlying_type = self.get_type(underlying_type_name)
            if not isinstance(underlying_type, IntegerType):
                raise RuntimeError(
                    f"{underlying_type.name} is not a numeric type, so it cannot be specified as "
                    + "an underlying type."
                )
            return underlying_type
        else:
            raise RuntimeError(f'"{name}" type syntax is invalid. (Only one colon is allowed)')

    def _create_custom_type(self, name, underlying_type_override):
        unresolved_type = self.unresolved_types.get(name)
        if not unresolved_type:
            raise RuntimeError(f"{name} type is not defined.")

        if unresolved_type.type_xml.tag == "enum":
            return self._create_enum_type(
                unresolved_type.type_xml, underlying_type_override, unresolved_type.relative_path
            )
        elif unresolved_type.type_xml.tag == "struct":
            return self._create_struct_type(unresolved_type.type_xml, unresolved_type.relative_path)
        else:
            raise RuntimeError(
                f'Unhandled CustomType xml element: <{unresolved_type.type_xml.tag}>'
            )

    def _create_enum_type(self, protocol_enum, underlying_type_override, relative_path):
        underlying_type = underlying_type_override
        enum_name = get_required_string_attribute(protocol_enum, "name")

        if underlying_type is None:
            underlying_type_name = get_required_string_attribute(protocol_enum, "type")
            if enum_name == underlying_type_name:
                raise RuntimeError(f"{enum_name} type cannot specify itself as an underlying type.")

            default_underlying_type = self.get_type(underlying_type_name)
            if not isinstance(default_underlying_type, IntegerType):
                raise RuntimeError(
                    f"{default_underlying_type.name} is not a numeric type, so it cannot be "
                    + "specified as an underlying type."
                )

            underlying_type = default_underlying_type

        protocol_values = protocol_enum.findall("value")

        values = []
        ordinals = set()
        names = set()

        for protocol_value in protocol_values:
            text = get_text(protocol_value)
            ordinal = try_parse_int(text)
            value_name = get_required_string_attribute(protocol_value, "name")
            python_name = value_name

            if python_name == 'None':
                python_name += '_'

            if ordinal is None:
                raise RuntimeError(f'{enum_name}.{value_name} has invalid ordinal value "{text}"')

            if ordinal not in ordinals:
                ordinals.add(ordinal)
            else:
                raise RuntimeError(
                    f'{enum_name}.{value_name} cannot redefine ordinal value {ordinal}.'
                )

            if python_name not in names:
                names.add(python_name)
            else:
                raise RuntimeError(f"{enum_name} enum cannot redefine value name {value_name}.")

            values.append(EnumValue(ordinal, value_name, python_name))

        return EnumType(enum_name, relative_path, underlying_type, values)

    def _create_struct_type(self, protocol_struct, relative_path):
        return StructType(
            get_required_string_attribute(protocol_struct, "name"),
            self._calculate_fixed_struct_size(protocol_struct),
            self._is_bounded(protocol_struct),
            relative_path,
        )

    def _calculate_fixed_struct_size(self, protocol_struct):
        size = 0

        for instruction in TypeFactory._flatten_instructions(protocol_struct):
            instruction_size = 0

            if instruction.tag == "field":
                instruction_size = self._calculate_fixed_struct_field_size(instruction)
            elif instruction.tag == "array":
                instruction_size = self._calculate_fixed_struct_array_size(instruction)
            elif instruction.tag == "dummy":
                instruction_size = self._calculate_fixed_struct_dummy_size(instruction)
            elif instruction.tag == "chunked":
                # Chunked reading is not allowed in fixed-size structs
                return None
            elif instruction.tag == "switch":
                # Switch sections are not allowed in fixed-sized structs
                return None

            if instruction_size is None:
                return None

            size += instruction_size

        return size

    def _calculate_fixed_struct_field_size(self, protocol_field):
        type_name = get_required_string_attribute(protocol_field, "type")
        type_length = TypeFactory._create_type_length_for_field(protocol_field)
        type_instance = self.get_type(type_name, type_length)
        field_size = type_instance.fixed_size

        if field_size is None:
            # All fields in a fixed-size struct must also be fixed-size
            return None

        if protocol_field.get("optional"):
            # Nothing can be optional in a fixed-size struct
            return None

        return field_size

    def _calculate_fixed_struct_array_size(self, protocol_array):
        length_string = protocol_array.get("length")
        length = try_parse_int(length_string)

        if length is None:
            # An array cannot be fixed-size unless a numeric length attribute is provided
            return None

        type_name = get_required_string_attribute(protocol_array, "type")
        type_instance = self.get_type(type_name)

        element_size = type_instance.fixed_size

        if element_size is None:
            # An array cannot be fixed-size unless its elements are also fixed-size
            # All arrays in a fixed-size struct must also be fixed-size
            return None

        if protocol_array.get("optional"):
            # Nothing can be optional in a fixed-size struct
            return None

        if protocol_array.get("delimited"):
            # It's possible to omit data or insert garbage data at the end of each chunk
            return None

        return length * element_size

    def _calculate_fixed_struct_dummy_size(self, protocol_dummy):
        type_name = get_required_string_attribute(protocol_dummy, "type")
        type_instance = self.get_type(type_name)
        dummy_size = type_instance.fixed_size

        if dummy_size is None:
            # All dummy fields in a fixed-size struct must also be fixed-size
            return None

        return dummy_size

    def _is_bounded(self, protocol_struct):
        result = True

        for instruction in TypeFactory._flatten_instructions(protocol_struct):
            if not result:
                result = instruction.tag == "break"
                continue

            if instruction.tag == "field":
                field_type = self.get_type(
                    get_required_string_attribute(instruction, "type"),
                    TypeFactory._create_type_length_for_field(instruction),
                )
                result = field_type.bounded
            elif instruction.tag == "array":
                element_type = self.get_type(get_required_string_attribute(instruction, "type"))
                length = get_string_attribute(instruction, "length")
                result = element_type.bounded and length is not None
            elif instruction.tag == "dummy":
                dummy_type = self.get_type(get_required_string_attribute(instruction, "type"))
                result = dummy_type.bounded

        return result

    @staticmethod
    def _flatten_instruction(instruction, result):
        result.append(instruction)

        if instruction.tag == "chunked":
            for chunked_instruction in get_instructions(instruction):
                TypeFactory._flatten_instruction(chunked_instruction, result)
        elif instruction.tag == "switch":
            protocol_cases = instruction.findall("case")
            for protocol_case in protocol_cases:
                for case_instruction in get_instructions(protocol_case):
                    TypeFactory._flatten_instruction(case_instruction, result)

    @staticmethod
    def _flatten_instructions(element, result=None):
        if result is None:
            result = []

        for instruction in get_instructions(element):
            TypeFactory._flatten_instruction(instruction, result)

        return result

    @staticmethod
    def _create_type_length_for_field(protocol_field):
        length_string = protocol_field.get("length")
        if length_string is not None:
            return Length.from_string(length_string)
        else:
            return Length.unspecified()

    @staticmethod
    def _create_type_with_specified_length(name, length):
        if name in ["string", "encoded_string"]:
            return StringType(name, length)
        else:
            raise RuntimeError(
                f'{name} type with length {length} is invalid. '
                + '(Only string types may specify a length)'
            )


class UnresolvedCustomType:
    def __init__(self, type_xml, relative_path):
        self._type_xml = type_xml
        self._relative_path = relative_path

    @property
    def type_xml(self):
        return self._type_xml

    @property
    def relative_path(self):
        return self._relative_path
