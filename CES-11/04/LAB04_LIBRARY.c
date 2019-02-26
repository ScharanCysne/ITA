/*

Global Variables

char parentheticalForm[100];		// Expression readed form terminal
char polishForm[100];				// Converted form of expression

ATOM parenthetical[100];		    // ATOMs of parenthetic form
int n_atoms, i;						// Number of ATOMs and cursor for parentheticalForm[100]
char c;								// Stores a character from parentheticalForm

#define NUMBER 1
#define OP     2
#define OPAR   3	// Open parenthesis
#define CPAR   4	// Close parenthesis
#define INVAL  5

*/

#include "LAB04_LIBRARY.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

void make_atoms (){

	float value_aux = 0;
	n_atoms = 0;
	
	init_expr();
	c = get_non_blank();

	while(c != '\0'){

		static int ATOM_cursor = 0;

		if(isdigit(c)){

			value_aux = c - '0';
			c = get_next();

			while(isdigit(c)){

				value_aux = 10*value_aux + c - '0';
				c = get_next();
			}

			if(c == '.'){

				c = get_next();
				int decimal = 0;

				while(isdigit(c)){

					decimal++;
					value_aux = value_aux + ((double)(c - '0'))/(pow(10, decimal));
					c = get_next();
				}				
			}

			parenthetical[ATOM_cursor].mode = NUMBER;
			parenthetical[ATOM_cursor].atrib.value = value_aux;
		}
		else if (c == '+' || c == '*' || c == '~' || c == '@' || c == 'L' 
				|| c == 'R' || c == 'S' || c == 'C' || c == '-' || c == '/'){

			parenthetical[ATOM_cursor].mode = OP;
			parenthetical[ATOM_cursor].atrib.op = c;
		
			c = get_next();
		}
		else if (c == '(' || c == ')'){

			if(c == '(')
				parenthetical[ATOM_cursor].mode = OPAR;
			if(c == ')')
				parenthetical[ATOM_cursor].mode = CPAR;

			c = get_next();
		}
		else{

			parenthetical[ATOM_cursor].mode = INVAL;
			parenthetical[ATOM_cursor].atrib.carac = c;
			
			c = get_next();
		}

		n_atoms++;
		ATOM_cursor++;

		c = get_non_blank();
	}
}

void print_atoms (atom *list, int n){

	printf(" Type    |   Attribute\n");
	printf(" -----------------------\n");

	for(int k = 0; k < n; k++){

		switch(list[k].mode){

			case NUMBER:

				printf(" NUMBER  |   %g\n", list[k].atrib.value);	 
				break;

			case OP:

				printf(" OP      |   %c\n", list[k].atrib.op);	 
				break;

			case OPAR:

				printf(" OPAR    |\n");	 
				break;

			case CPAR:

				printf(" CPAR    |\n");	 
				break;

			default:

				printf(" INVAL   |   %c\n", list[k].atrib.carac);	 
		}
	}
}

char get_non_blank (){

	while(isspace(parentheticalForm[i]) || (iscntrl(parentheticalForm[i]) && parentheticalForm[i] != '\0'))
		i++;
	return parentheticalForm[i];
}

char get_next (){

	i++;
	return parentheticalForm[i];
}

void init_expr (){

	i = 0;
}

void push(stack_t * p, atom * x){

	node_t * temp = (*p);

	(*p) = (node_t *) malloc (sizeof(node_t));
	(*p)->elem = x;
	(*p)->next = temp; 
}

void pop(stack_t * p){
	
	if(!is_empty(*p)){

		node_t * temp = *p;
		*p = (*p)->next;
		free(temp);
	}
}

atom * top(stack_t p){

	return is_empty(p) ? NULL : p->elem;
}

stack_t * new_stack(){

	stack_t * p = (stack_t *) malloc (sizeof(stack_t));
	(*p) = NULL;

	return p;
}

bool is_empty(stack_t p){

	return p == NULL;
}

bintree_t create_tree(atom * polish){

	bintree_node node_tree;
	node_tree = init_tree();

	while(i > 0){
		
		i--;
		if(polish[i].mode == OP){

			*node_tree->elem = polish[i];
			node_tree->rchild = create_tree(polish);
			node_tree->lchild = create_tree(polish);
			return node_tree;
		}

		else if(polish[i].mode == NUMBER){
			*node_tree->elem = polish[i];
			return node_tree;
		}
	}		
}

bintree_t init_tree(){

	bintree_t tree = (bintree_t) malloc (sizeof(cell_t));
	tree->elem = (atom *) malloc (sizeof(atom));
	tree->lchild = NULL;
	tree->rchild = NULL;

	return tree;
}

void print_tree(bintree_node tree){

		if(tree->lchild != NULL){
			printf("(");
			print_tree(tree->lchild);
		}

		if(tree->elem->mode == NUMBER)
			printf("%g", tree->elem->atrib.value);
		if(tree->elem->mode == OP)
			printf(" %c ", tree->elem->atrib.op);

		if(tree->rchild != NULL){
			print_tree(tree->rchild);
			printf(")");
		}
}

float eval_expr (bintree_t tree){

	if(tree->elem->mode == NUMBER)	
		return tree->elem->atrib.value;
	else{

		if(tree->elem->atrib.op == '+')
			return eval_expr(tree->lchild) + eval_expr(tree->rchild);
		if(tree->elem->atrib.op == '*')
			return eval_expr(tree->lchild) * eval_expr(tree->rchild);
		if(tree->elem->atrib.op == '-')
			return eval_expr(bt->lchild) - eval_expr(bt->rchild);
		if(tree->elem->atrib.op == '/')
			return eval_expr(bt->lchild) / eval_expr(bt->rchild);
		if(tree->elem->atrib.op == '~')
			return (-eval_expr(bt->rchild));
		if(tree->elem->atrib.op == '@')
			return pow(eval_expr(bt->lchild), eval_expr(bt->rchild));
		if(tree->elem->atrib.op == 'L')
			return log(eval_expr(bt->lchild)) / log(eval_expr(bt->rchild));
		if(tree->elem->atrib.op == 'R')
			return sqrt(eval_expr(bt->rchild));
		if(tree->elem->atrib.op == 's')
			return sin(eval_expr(bt->rchild));
		if(tree->elem->atrib.op == 'C')
			return cos(eval_expr(bt->rchild));
	}
}