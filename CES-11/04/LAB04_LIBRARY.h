#ifndef LIBRARY_H_
#define LIBRARY_H_

#include <stdbool.h>

#define NUMBER 1
#define OP     2
#define OPAR   3	// Open parenthesis
#define CPAR   4	// Close parenthesis
#define INVAL  5

typedef union {						// Union
	float value;
	char op, carac;
} atribatom;

typedef struct{						// Atom

	int mode;	
	atribatom atrib;	
} atom;

typedef struct node{				// Stack - node_t

	atom * elem;
	struct node * next;
} node_t;

typedef struct cell{				// Tree
atom * elem;
struct cell * lchild, * rchild;
} cell_t;

typedef cell_t * bintree_node;
typedef cell_t * bintree_t;
typedef node_t * stack_t;

// Global Variables

char parentheticalForm[100];		// Expression readed form terminal
atom polishForm[100];				// Converted form of expression

atom parenthetical[100];		    // ATOMs of parenthetic form
int n_atoms, i;						// Number of ATOMs and cursor for parentheticalForm[100]
char c;								// Stores a character from parentheticalForm
stack_t * op_stack;					// Stack of operators
bintree_t bt;						// Binary Tree of Operations

// Functions prototypes

/* Parenthetical Lifesaver */

void make_atoms();					// Stores in Parenthetical the atoms of expression ParentheticalForm
void print_atoms(atom *, int);		// Print the parenthetical list
char get_non_blank();				// Pretty intuitive, correct?
char get_next();					// This one too...
void init_expr();					// Do I have to say something?

/* Polish Lifesaver */

void push(stack_t *, atom *);		// Let me guess, it "pushes"?
void pop(stack_t *);				// and this one pops
atom * top(stack_t);				// Return the top atom
stack_t * new_stack();				// I will not explain this
bool is_empty(stack_t);				// How original...

/* Tree Lifesaver */

float eval_expr (bintree_t bt);									// Evaluate Expression stored in binary tree
bintree_node create_tree(atom * polish);		// Create the goddamn tree
void print_tree(bintree_t bt);									// PRINT the tree
bintree_t init_tree();											// Allocates memory and sets shildren NULL

#endif  /* LIBRARY_H_ */