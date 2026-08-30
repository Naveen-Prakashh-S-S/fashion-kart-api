from marshmallow import Schema, fields

# Product
class PlainProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Int(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainSizeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ProductSizeSchema(Schema):
    size = fields.Nested(
        PlainSizeSchema,
        required=True
    )

    stock = fields.Int( required=True )


class ProductSchema(PlainProductSchema):
    tags = fields.List(fields.Nested(PlainTagSchema), required=True)
    sizes = fields.List(fields.Nested(ProductSizeSchema),required=True)


# Tag with Products

class TagSchema(PlainTagSchema):

    products = fields.List( fields.Nested(PlainProductSchema), required=True)
