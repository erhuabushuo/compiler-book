[TOC]

# Programming Languages and Implementation
As programmers writing complex systems to solve a problem, such as
searching the web or a classic such as Doom its easy to forget what
your programming language is doing under the hood. Without programming
languages, you would have to write raw assembler for your target
system which isn't really what we all want to do since working with
such raw primitives such as cpu instructions is very tedious and
difficult job to do well.

A programming language's design often has a strong influence on what,
way it should be implemented; for example a language such as
Python has such dynamic behaviour to implement that writing it as an
interpreter is very natural as you can resolve anything at
runtime. But if you look at C or Fortran a traditional Ahead of Time
compiler such as GCC targets this more naturally, since C has strong
ties to how computers see data via raw pointers thusly we can compile
this to native target code.

Lets dive in and implement a pseudo python language (Not full) since
it would take too long for the purposes of this book.

## Audiance
This book is aimed at students or entusiasts or even a full time
programmer, anyone who has experince in C or Python or Java should be
familar with the concepts used and discussed. Mostly a knowledge in
Data-Stuctures is required Linked-Lists, Stacks, Tree's and Hash
Tables.

The code in this book is going to be written mostly in C and Python
as these are my favorites i will have a section on targeting the JVM
so i will use Java here.

This book isn't going to show more advanced techniques but designed to
show all the simple techniques require to write Interpreters, Virtual
Machines and Compilers. For example Parsing i use a simple Recursive
Decent Parser and dont go into the details of LL LR or LALR parsing. I
aim to keep this as simple and non-computer science as i can.

### Dynamic Languages - Tiny Python
Lets get stuck in right away an interpreter usually accepts a source
file argument to execute or an interactive shell using ReadLine. We
can implement an interpreter loop in python by doing:

```python
def interactive_shell (prompt='>>> '):
    while True:
        try:
            line = raw_input (prompt)
            parse_execute (line)
        except EOFError:
            break
```

Now we have a shell to work with, lets look at sample input strings
and from first principles figure out what we need to do.

If i enter

```python
>>> x = 1 + 1
```

We would expect there to be a name x which stores the value 2. If i
input some syntax error such as:

```python
>>> x , = 2
```

We would expect a syntax error, if we try to address an unknown such
as:

```python
>>> x = doesnt_exist
```

It should bring an error. So for something so simple as assigning data
to a variable there is at first glance quite a few things to keep in
mind. In compiler development divide and conquer algorithms are very
important split things down into simpler and more defined chunks.

The starting point in any compiler is the Abstract Syntax Tree, which
means we split every declaration (each expression or function etc)
into a tree which represents the syntax in memory. So for example

```
# x = 1 + 2 - 3
    =
  /  \
x     +
     /  \
	1    -
	    /  \
		2   3
```

For me once i understood this concept everything can fall into place
for compilers. You may see this referenced as the Directed Acyclic
Graph (DAG) is a formal name of what this is the dragon book has a
great section on this but its simple concept.

So if you imagine in the compiler this is a Tree data Stucture such
as:

```c
typedef enum {
	EQUALS,
	PLUS,
	MINUX,
	INTEGER,
	NAME
} NODE_TYPE;

struct node {
	NODE_TYPE T;
	union {
		int integer;
		char * name;
	} data;
}

struct syntax_node {
	struct node value;
	struct syntax_node * lhs;
	struct syntax_node * rhs;
}
```

This set of structs can represent anything in the syntax now in memory
for any kind of semantic analysis we will need to do. Imagine the
expression:

```python
>>> x = 1 + 2
```

This will create:

```c
struct syntax_node * integer_1 = calloc (1, sizeof (struct syntax_node));
struct syntax_node * integer_2 = calloc (1, sizeof (struct syntax_node));
struct syntax_node * name = calloc (1, sizeof (struct syntax_node))
struct syntax_node * addition = calloc (1, sizeof (struct syntax_node));
struct syntax_node * assignment = calloc (1, sizeof (struct syntax_node));

integer_1->value.T = INTEGER;
integer_1->value.data.integer = 1;

integer_2->value.T = INTEGER;
integer_2->value.data.integer = 2;

name->value.T = NAME;
name->value.data.name = 'x';

assignment->value.T = EQUALS;
assignment->lhs = name;
assignment->rhs = addition;
```

This will create that exact tree, i shown this in C just because in
Python it is less obvious the concept being used to do this as we dont
have explicit unions or antyhing in python as it is dynamicly typed
antyhing can be anything.

So now we know how to represent pure source code in memory in a useful
way we need to parse the input and generate these tree's in a useful
way. As i mentioned before divide and conquer this is why we create a
Lexer and a Parser 2 sperate pieces of code.

#### Parsing
A Lexer is responsible for reading the raw input and a Parser
understands the grammar of the language to then generate these
tree's. To understand what way these work in practice is to look at
each individually for a Lexer this example shows what it should do:

```python
x = 1 + 2
```

The lexer would return:

1. IDENTIFIER (x)
2. EQUALS
3. INTEGER (1)
4. PLUS
5. INTEGER (2)
6: EOF

First we define a token type:

```c
typedef enum {
	IDENTIFIER,
	EQUALS,
	INTEGER,
	PLUS,
	EOF
} TOKEN_TYPE;

struct token {
	TOKEN_TYPE T;
	union {
		int integer;
		char * name;
	} value;
}
```

The Lexer works via regular expressions so you can define what a token
would look like the taditional way this function is defined is:

```c
struct lexer_state {
	char * buffer;
	size_t offset, size;
};

struct token current_token;
struct lexer_state lexer;

void yylex (void) {
  while (lexer.offset < lexer.size)
  {
	char c = lexer.buffer [lexer.offset];
	
	if (c == '=') {
		current_token.T = EQUALS;
		break;
	}
	else if (c == integer) {
		read_integer (&lexer, &current_token);
		break;
	}
	else if (c == character) {
		read_name (..)
		break;
	}
	
	lexer.offset++;
  }
  current_token.T = EOF;
}
```

So this means you can keep calling the yylex function and read the
current token afer it returns. If you setup the buffer with an input
string of source code this function will return each token and ignore
white space since this is not a lexical token that matters.
