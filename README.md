# The Mirage Programming Language

>**NOTE:** Mirage is currently in the design stage. Many ideas and features are not solidified or implemented at the moment.

The Mirage programming language is designed around the following principles:

* There should be as few rational ways to solve the same problem as possible. This means no interchangeable syntax, for instance.
* One should not have to consider micro optimizations when writing code. They should be inferred.
* The compiler should enforce as many assumptions as possible.
* Pure functional needs to be supported with optimizations and syntax to be a reasonable alternative to imperative.
* Compiling for development should be extremely fast. Code should execute extremely fast in production.
* Configuration should be code.


### Contextual Types

The core idea that allows Mirage to uphold many of the principles above is contextual type annotations. Lines of code can infer things that may be relevant to subsequent lines of code. As humans we keep track of this to some degree and this (among many other things) allows us to understand code better than modern compilers. When Mirage encounters conditionals that affect execution flow (like the condition in an if statement) it modifies types in those contexts.

For example: getting a value from a dictionary without checking if the key exists in the dictionary is unsafe. In some languages like Scala you can get an optional instead and deal with the None case. In Mirage you can check if the value exists, and then inside the if statement the type of the dictionary is annotated to mark that the symbol you checked for is contained in the dictionary. `Dict[Int, Int]` becomes `Dict[Int, Int]-Contains[$x]` for example, where `x` is what you checked for. This annotated type allows you to safely and directly get the value with x. If a line modifies `x` then the contextual type is invalidated for subsequent lines.

Contextual type annotation can be user defined so that any boolean function can modify types. Type annotations allow defining additional methods for convenience, which is how the safe dictionary access is implemented. Even more importantly type annotations allow you to define substitutions. Substitutions can be used to find duplicate checks and dead code, perform micro optimizations, and more.


### Configuration Is Code

When humans are constantly modifying configuration files they are bound to make mistakes. Often times these mistakes are not discovered until runtime, which for large or slow building projects could take 15 minutes or longer. By moving configuration into flexible and powerful Mirage enums one can leverage the compiler and/or unit testing to enforce valid configuration. Another benefit is a lowered learning barrier since you only need to learn Mirage enums instead of potentially many different configuration syntaxes. Mirage enums can also be loaded/swapped at runtime like other configs, and come with a ton of useful features like serialization/deserialization support (think Thrift), values, and automatically generated collections.


## How to set up Sublime syntax for Sublime Text 3:

1. Move the file to a location that depends on your OS:
    * Windows (git bash): `$ cp mirage.sublime-syntax ${APPDATA}/Sublime\ Text\ 3/Packages/User`
    * Mac: `$ cp mirage.sublime-syntax ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/User`
    * Linux: `$ cp mirage.sublime-syntax ~/.config/sublime-text-3/Packages/User/`
2. Re-open Sublime Text 3
3. Click View -> Syntax -> Mirage
