# ============================================================
# PYDANTIC V2 EXERCISE + SOLUTION
# ============================================================
#
# QUESTION:
#
# Build a pure Pydantic v2 validation system for a small Tea Shop.
# Everything must be inside this single Python file.
#
# The system should contain these models:
# 1. Address
# 2. Category
# 3. MenuItem
# 4. Customer
# 5. Payment
# 6. OrderItem
# 7. Order
#
# Concepts to demonstrate:
# - BaseModel
# - Type annotations
# - Annotated
# - Field validations
# - field_validator
# - model_validator
# - computed_field / @property
# - Literal
# - Nested models
# - Self-referencing models
# - Advanced / cross-field validation
#
# Requirements:
#
# Address:
# - street and city must have length constraints
# - country can only be "IN" or "US"
# - Indian postal code must contain exactly 6 digits
# - US postal code must contain exactly 5 digits
#
# Category:
# - positive category_id
# - clean the category name
# - category can contain more Category objects recursively
#
# MenuItem:
# - positive item_id and price
# - name must be cleaned
# - category must be a nested Category
# - spice_level must use Literal
#
# Customer:
# - positive customer_id
# - clean the name
# - normalize phone number
# - lowercase and validate email
# - loyalty_points cannot be negative
# - computed loyalty_tier
#
# Payment:
# - payment method can be cash, card or upi
# - card payment requires exactly 4 card digits
# - non-card payments cannot contain card_last4
# - tip cannot be negative
#
# OrderItem:
# - positive menu_item_id and price
# - quantity between 1 and 20
# - computed line_total
#
# Order:
# - customer must be a nested Customer
# - items must be a list of OrderItem
# - at least one item is required
# - order_type is delivery or pickup
# - delivery requires delivery_address
# - pickup cannot have delivery_address
# - duplicate menu_item_id values are not allowed
# - discount must be between 0 and 50
# - computed subtotal, discount_amount, tax_amount and final_total
#
# Finally:
# - create valid test data
# - create a 4-level Category tree
# - print normalized values
# - print computed values
# - run one invalid test and display the ValidationError
#
# ============================================================

from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    Field,
    computed_field,
    field_validator,
    model_validator,
)


class Address(BaseModel):
    street: Annotated[str, Field(min_length=3, max_length=100)]
    city: Annotated[str, Field(min_length=2, max_length=50)]
    country: Literal["IN", "US"]
    postal_code: str

    @field_validator("street", "city")
    @classmethod
    def clean_text(cls, value: str) -> str:
        return " ".join(value.strip().split())

    @model_validator(mode="after")
    def validate_postal_code(self):
        if self.country == "IN":
            if not self.postal_code.isdigit() or len(self.postal_code) != 6:
                raise ValueError("Indian postal code must contain 6 digits")

        if self.country == "US":
            if not self.postal_code.isdigit() or len(self.postal_code) != 5:
                raise ValueError("US postal code must contain 5 digits")

        return self


class Category(BaseModel):
    category_id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(min_length=2, max_length=40)]
    subcategories: list["Category"] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return " ".join(value.strip().split()).title()


Category.model_rebuild()


class MenuItem(BaseModel):
    item_id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(min_length=3, max_length=60)]
    price: Annotated[float, Field(gt=0)]
    category: Category
    is_vegetarian: bool = True
    spice_level: Literal["mild", "medium", "hot"] | None = None
    available: bool = True

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return " ".join(value.strip().split()).title()

    @model_validator(mode="after")
    def validate_spice(self):
        if not self.is_vegetarian and self.spice_level == "mild":
            raise ValueError(
                "Non-vegetarian item cannot have mild spice"
            )
        return self


class Customer(BaseModel):
    customer_id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(min_length=3, max_length=50)]
    email: str
    phone: str
    address: Address
    loyalty_points: Annotated[int, Field(ge=0)] = 0

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return " ".join(value.strip().split()).title()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()

        if "@" not in value:
            raise ValueError("Invalid email")

        if value.endswith("@test.com"):
            raise ValueError("test.com emails are not allowed")

        return value

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, value: str) -> str:
        digits = "".join(c for c in value if c.isdigit())

        if digits.startswith("91") and len(digits) == 12:
            digits = digits[2:]

        if len(digits) != 10:
            raise ValueError("Phone must contain 10 digits")

        return digits

    @computed_field
    @property
    def loyalty_tier(self) -> str:
        if self.loyalty_points >= 1000:
            return "gold"
        if self.loyalty_points >= 500:
            return "silver"
        return "bronze"


class Payment(BaseModel):
    payment_id: Annotated[int, Field(gt=0)]
    method: Literal["cash", "card", "upi"]
    card_last4: str | None = None
    tip: Annotated[float, Field(ge=0)] = 0.0

    @model_validator(mode="after")
    def validate_card(self):
        if self.method == "card":
            if self.card_last4 is None:
                raise ValueError(
                    "Card payment requires card_last4"
                )

            if (
                not self.card_last4.isdigit()
                or len(self.card_last4) != 4
            ):
                raise ValueError(
                    "card_last4 must contain exactly 4 digits"
                )

        elif self.card_last4 is not None:
            raise ValueError(
                "card_last4 is only allowed for card payment"
            )

        return self


class OrderItem(BaseModel):
    menu_item_id: Annotated[int, Field(gt=0)]
    item_name: Annotated[str, Field(min_length=3, max_length=60)]
    unit_price: Annotated[float, Field(gt=0)]
    quantity: Annotated[int, Field(ge=1, le=20)]

    @computed_field
    @property
    def line_total(self) -> float:
        return self.unit_price * self.quantity


class Order(BaseModel):
    order_id: Annotated[int, Field(gt=0)]
    customer: Customer
    items: list[OrderItem] = Field(min_length=1)
    payment: Payment
    order_type: Literal["delivery", "pickup"]
    delivery_address: Address | None = None
    discount_percent: Annotated[float, Field(ge=0, le=50)] = 0.0

    @model_validator(mode="after")
    def validate_order(self):
        if (
            self.order_type == "delivery"
            and self.delivery_address is None
        ):
            raise ValueError(
                "Delivery order requires delivery_address"
            )

        if (
            self.order_type == "pickup"
            and self.delivery_address is not None
        ):
            raise ValueError(
                "Pickup order cannot have delivery_address"
            )

        ids = [item.menu_item_id for item in self.items]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "Duplicate menu_item_id is not allowed"
            )

        return self

    @computed_field
    @property
    def subtotal(self) -> float:
        return sum(item.line_total for item in self.items)

    @computed_field
    @property
    def discount_amount(self) -> float:
        return self.subtotal * self.discount_percent / 100

    @computed_field
    @property
    def tax_amount(self) -> float:
        return (self.subtotal - self.discount_amount) * 0.05

    @computed_field
    @property
    def final_total(self) -> float:
        delivery_fee = 40 if self.order_type == "delivery" else 0

        return (
            self.subtotal
            - self.discount_amount
            + self.tax_amount
            + self.payment.tip
            + delivery_fee
        )


if __name__ == "__main__":

    # --------------------------------------------------------
    # SELF-REFERENCING CATEGORY
    # --------------------------------------------------------

    category = Category(
        category_id=1,
        name="  beverages ",
        subcategories=[
            {
                "category_id": 2,
                "name": "hot beverages",
                "subcategories": [
                    {
                        "category_id": 3,
                        "name": "tea",
                        "subcategories": [
                            {
                                "category_id": 4,
                                "name": "milk tea"
                            }
                        ]
                    }
                ]
            }
        ]
    )

    # --------------------------------------------------------
    # VALID ORDER
    # --------------------------------------------------------

    order = Order(
        order_id=1001,

        customer={
            "customer_id": 1,
            "name": "  vismay thakkar ",
            "email": "VISMAY@GMAIL.COM",
            "phone": "+91 98765-43210",

            "address": {
                "street": " SG Highway ",
                "city": " Ahmedabad ",
                "country": "IN",
                "postal_code": "380054"
            },

            "loyalty_points": 650
        },

        items=[
            {
                "menu_item_id": 101,
                "item_name": "Masala Chai",
                "unit_price": 40,
                "quantity": 2
            },
            {
                "menu_item_id": 102,
                "item_name": "Adrak Chai",
                "unit_price": 35,
                "quantity": 1
            }
        ],

        payment={
            "payment_id": 5001,
            "method": "card",
            "card_last4": "4242",
            "tip": 20
        },

        order_type="delivery",

        delivery_address={
            "street": "12 MG Road",
            "city": "Ahmedabad",
            "country": "IN",
            "postal_code": "380001"
        },

        discount_percent=10
    )

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    print("\n========== CUSTOMER ==========")
    print("Name:", order.customer.name)
    print("Email:", order.customer.email)
    print("Phone:", order.customer.phone)
    print("Loyalty Tier:", order.customer.loyalty_tier)

    print("\n========== ORDER ==========")
    print("Subtotal:", order.subtotal)
    print("Discount:", order.discount_amount)
    print("Tax:", order.tax_amount)
    print("Final Total:", order.final_total)

    print("\n========== CATEGORY TREE ==========")
    print(category.name)
    print(category.subcategories[0].name)
    print(category.subcategories[0].subcategories[0].name)
    print(
        category
        .subcategories[0]
        .subcategories[0]
        .subcategories[0]
        .name
    )

    # --------------------------------------------------------
    # INVALID TEST
    # --------------------------------------------------------

    print("\n========== INVALID TEST ==========")

    try:
        Payment(
            payment_id=99,
            method="cash",
            card_last4="1234"
        )
    except Exception as error:
        print(type(error).__name__)
        print(error)