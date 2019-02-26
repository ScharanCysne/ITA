#include <stdio.h>
#include <stdlib.h>

int main(){
	
	int numero;
	char sinal;

	FILE * entrada;

	entrada = fopen ("entradda.txt", "r");

	while(!feof(entrada)){

	fscanf(entrada, " %c %d ", &sinal, &numero);

	printf("%c e %d \n", sinal, numero);

	}

	getchar;


	return 0;
}