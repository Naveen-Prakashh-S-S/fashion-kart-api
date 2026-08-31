from marshmallow import Schema, fields


# =========================================================
# PRODUCT SCHEMAS
# =========================================================

class PlainProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Int(required=True)


class ProductSizeSchema(Schema):
    size = fields.Nested(
        "PlainSizeSchema",
        required=True
    )
    stock = fields.Int(required=True)


class ProductSchema(PlainProductSchema):
    tags = fields.List(
        fields.Nested("PlainTagSchema"),
        required=True
    )

    sizes = fields.List(
        fields.Nested("ProductSizeSchema"),
        required=True
    )


class ProductSizeCreateSchema(Schema):
    size_id = fields.Int(required=True)
    stock = fields.Int(required=True)


class ProductCreateSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Int(required=True)

    tags = fields.List(
        fields.Int(),
        required=True
    )

    sizes = fields.List(
        fields.Nested("ProductSizeCreateSchema"),
        required=True
    )


# =========================================================
# TAG SCHEMAS
# =========================================================

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class TagSchema(PlainTagSchema):
    products = fields.List(
        fields.Nested("PlainProductSchema"),
        required=True
    )


class TagCreateSchema(Schema):
    name = fields.Str(required=True)


# =========================================================
# SIZE SCHEMAS
# =========================================================

class PlainSizeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class SizeCreateSchema(Schema):
    name = fields.Str(required=True)
