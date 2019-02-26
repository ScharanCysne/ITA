#include "LAB03_LIBRARY.h"

int main(){

	char expressao[101], symbol;
	int value, result, i = 0, failed = 0;

	pilha_t stack;

	printf(" CES-11: LAB03 - Calculadora Polonesa utilizando o TAD Pilha.\n  \n");
	printf(" Por favor insira a expressao desejada (maximo de 100 caracteres): ");

	fgets(expressao, 101, stdin);
	adt_initStack(stack); 

	while(1){

		symbol = nonBlank(expressao, i);

		if(isdigit(symbol)){
		
			value = makeNumber(expressao, i, symbol);
			adt_pushStack(&stack, value);
		}
		else if(symbol == '+' || symbol == '*'){

 			failed = executeOper(&stack, symbol);

	 		if(failed == 1) 
	 			break;
	 
	 		symbol = nextCarac(expressao, i);
	 	} 	
 		else {
 		
 			failed = 1; 
 			break;
 		}

	}

	failed = 0;

	if(adt_emptyStack(stack))
		result = 0;
	else{
	
		result = adt_topStack(stack); 
		adt_popStack(&stack);

		if(!adt_emptyStack(stack)) 
			failed = 1;
	}

	if(failed) 
		 printf("\n Erro na expressao!\n");
	else printf("\n Valor da expressao = %d.\n", result);

    return 0;
}