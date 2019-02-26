/**
  *	LAB 04 - Árvore Binária para Expressão Aritmética
  *
  *	Author: Nicholas Scharan Cysne
  *
  *	CES-11 Algoritmos e Estruturas de Dados
  *
  * Prof. Denis Loubach & Lourenço Junior
  *
**/

#include "LAB04_LIBRARY.c"

int main(int argc, char *argv[]){

	// Parenthetical Form Acquisition

	printf("\n CES-11: LAB04 - Arvore Binaria para Expressao Aritmetica.\n\n");
	printf(" Por favor digite a expressao desejada: \n\n");
	printf(" (Considera-se que cada expressao possui no maximo 100 caracteres.) \n\n");

	printf(" Expressao: ");
	fgets(parentheticalForm, 100, stdin);
	make_atoms();

	printf("\n Atoms encontrados:\n");
	print_atoms(parenthetical, n_atoms);

	// Polish Form Transformation

	op_stack = new_stack();

	for(int k = 0; k < n_atoms; k++){

		static int polish_cursor = 0;

		switch(parenthetical[k].mode){

			case NUMBER:

				polishForm[polish_cursor] = parenthetical[k];
				polish_cursor++;
				break;

			case OP:

				push(op_stack, &parenthetical[k]);
				break;

			case OPAR:

				break;

			case CPAR:

				if(!is_empty(*op_stack)){
		
					atom * temp;
					temp = top(*op_stack);
					polishForm[polish_cursor] = *temp;
					pop(op_stack);

					polish_cursor++;
				}

				break;

			default:

				break;
		}
	}

	bt = create_tree(polishForm);
	printf("\n Print by Tree: ");
	print_tree(bt);
	printf("\n\n Evaluate: %g\n", eval_expr(bt));

	return 0;
}