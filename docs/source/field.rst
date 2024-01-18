Field Module
=============

The `field` module provides functionality for creating and managing simulation fields.

Field Class
------------

.. autoclass:: Field
   :members:

   Field class represents a simulation field with a given width and height.

   .. automethod:: __init__

   .. automethod:: field_creation

   .. note::
      The `field_creation` method prompts the user to input the width and height of the simulation field and validates the input.

Usage
-------

To use the `Field` class, instantiate an object and call the `field_creation` method:

.. code-block:: python

    from src.field import Field

    field = Field.field_creation()
    print(field.width)  # Accessing the width attribute of the field
    print(field.height)  # Accessing the height attribute of the field