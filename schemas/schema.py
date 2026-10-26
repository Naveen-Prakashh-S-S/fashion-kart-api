from marshmallow import Schema, fields, validate


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

class ProductTagCreateSchema(Schema):
    id = fields.Int(required=True)

class ProductAddSize(Schema):
    id = fields.Int(required = True)
    stock = fields.Int(required = True)

class ProductStockUpdateSchema(Schema):
    stock = fields.Int(required=True)
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


# =========================================================
# USER SCHEMAS
# =========================================================

class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class UserProfileSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()

# =========================================================
# CART SCHEMAS
# =========================================================

class CartSchema(Schema):
    product_id = fields.Int(required = True)
    size_id = fields.Int(required = True)
    quantity = fields.Int(required = True, validate=validate.Range(min=1))

class CartUpdateQuantity(Schema):
    quantity = fields.Int(required = True, validate=validate.Range(min=1))


# =========================================================
# ORDER SCHEMAS
# =========================================================

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    price = fields.Float(dump_only=True)


class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    status = fields.Str(dump_only=True)
    total_price = fields.Float(dump_only=True)
    items = fields.List(
        fields.Nested(OrderItemSchema),
        dump_only=True
    )