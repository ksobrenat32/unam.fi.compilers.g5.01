# Compilers Subject

This is the repository for the Compilers subject. The objective is to develop a compiler from scratch, using concepts learned on the subject.

We are group 5, team 01.

- Enrique Calderón
- Luis Salazar
- Luis Ugartechea
- Hansel Tepal

## Tasks

Here are the links for each project README.md

- [Lexer](./lexer/README.md)
- [Parser](./parser/README.md)

#### How to run

Once you have installed the required libraries and cloned the repository, you can run the application using the following command:

```bash
$ python compiler.py <source_file> <output_file>
```

Where `<source_file>` is the path to the source file you want to compile and `<output_file>` is the path where you want to save the compiled output.

## Tests

You can run tests for all the elements running:

```bash
$ python -m unittest discover -s tests
```