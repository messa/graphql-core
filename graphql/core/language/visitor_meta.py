from . import ast

QUERY_DOCUMENT_KEYS = {
    ast.Name: (),

    ast.Document: ('definitions',),
    ast.OperationDefinition: ('name', 'variable_definitions', 'directives', 'selection_set'),
    ast.VariableDefinition: ('variable', 'type', 'default_value'),
    ast.Variable: ('name',),
    ast.SelectionSet: ('selections',),
    ast.Field: ('alias', 'name', 'arguments', 'directives', 'selection_set'),
    ast.Argument: ('name', 'value'),

    ast.FragmentSpread: ('name', 'directives'),
    ast.InlineFragment: ('type_condition', 'directives', 'selection_set'),
    ast.FragmentDefinition: ('name', 'type_condition', 'directives', 'selection_set'),

    ast.IntValue: (),
    ast.FloatValue: (),
    ast.StringValue: (),
    ast.BooleanValue: (),
    ast.EnumValue: (),
    ast.ListValue: ('values',),
    ast.ObjectValue: ('fields',),
    ast.ObjectField: ('name', 'value'),

    ast.Directive: ('name', 'arguments'),

    ast.NamedType: ('name',),
    ast.ListType: ('type',),
    ast.NonNullType: ('type',),

    ast.ObjectTypeDefinition: ('name', 'interfaces', 'fields'),
    ast.FieldDefinition: ('name', 'arguments', 'type'),
    ast.InputValueDefinition: ('name', 'type', 'default_value'),
    ast.InterfaceTypeDefinition: ('name', 'fields'),
    ast.UnionTypeDefinition: ('name', 'types'),
    ast.ScalarTypeDefinition: ('name',),
    ast.EnumTypeDefinition: ('name', 'values'),
    ast.EnumValueDefinition: ('name',),
    ast.InputObjectTypeDefinition: ('name', 'fields'),
    ast.TypeExtensionDefinition: ('definition',),
}

AST_KIND_TO_TYPE = {c.__name__: c for c in QUERY_DOCUMENT_KEYS.keys()}


class VisitorMeta(type):
    def __new__(cls, name, bases, attrs):
        enter_handlers = {}
        leave_handlers = {}

        for base in bases:
            if hasattr(base, '_enter_handlers'):
                enter_handlers.update(base._enter_handlers)
            if hasattr(base, '_leave_handlers'):
                leave_handlers.update(base._leave_handlers)

        for attr, val in attrs.items():
            if attr.startswith('enter_'):
                ast_kind = attr[6:]
                ast_type = AST_KIND_TO_TYPE.get(ast_kind)
                enter_handlers[ast_type] = val

            elif attr.startswith('leave_'):
                ast_kind = attr[6:]
                ast_type = AST_KIND_TO_TYPE.get(ast_kind)
                leave_handlers[ast_type] = val

        attrs['_get_enter_handler'] = enter_handlers.get
        attrs['_get_leave_handler'] = leave_handlers.get
        return super(VisitorMeta, cls).__new__(cls, name, bases, attrs)
