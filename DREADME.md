CordForge has a base class `Component`, which all other UI components deal with.

To create images, a base image is made first, and then each component has it's `Draw() -> PillowImage` function is overridden, and it's `super().Draw()` is called. All UI components `Draw() -> PillowImage` is overridden with this as it's base:
```python
async def Draw(_) -> PillowImage:
    super().Draw()
    # Unique Composition
    return _.Image
```
All of it's `Children:list[Component]` are first drawn themselves, before the parent components drawing happens.

A component by default with autofill it's given space, unless given specific dimensions.

The developer uses the `Cord` class to create and control the UI components, as well as the UI components built-in methods. There are utilities outside of the `Cord` class's functionality like the `Font` class for font handling, the `Data` class for handling persistent data, the `Player` class for handling user profiles easily, and more.



##### Container
A container's height and width is by default the parent container if given one, elsewise it's the Cord object that is it is created with.