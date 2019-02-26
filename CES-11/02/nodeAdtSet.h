#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct position_t position_t;
typedef struct set_t set_t;

struct position_t{

	int data;
	position_t * next;
	position_t * prev;

};

struct set_t{

	position_t * setUniverse;

};


/** Funções indepentes das estruturas de dados **/

/*
Inicializa uma lista-conjunto vazia pronta para novas inserções.
*/
void adt_initSet(set_t *){


}

/*
Retorna o elemento da lista-conjunto da posição indicada no parâmetro da função.
*/
int adt_element(set_t, position_t){


}

/*
Insere o elemento indicado no parâmetro da função no final da lista-conjunto.
Fora do escopo do TAD, deverão ser elaboradas funções auxiliares tais como:
*/
void adt_insertLast(set_t *, int){


}

/*
Exibe os elementos do conjunto.
*/
void printSet(set_t){


}

/*
Exibe uma mensagem conforme o parâmetro da função.
*/
void errorMessage(char * message){


}

/*
Copia os elementos do set C2 para o set C1
*/
void adt_copySet(set_t * C1, set_t C2){


}

void initMessage(){

	system("clear");
	printf(" *********  CES-11:  Estrutura de Dados - Lab 02  *********\n");
	printf(" Armazenamento de Numeros Inteiros - Versão Lista Encadeada\n\n");
	printf(" Por favor insira os conjuntos a operar:\n");
}


/** Operadores da TAD position_t **/


/*
Retorna a posição do primeiro elemento da lista-conjunto.
*/
position_t adt_first(set_t){


}

/*
Retorna a posição do elemento da lista-conjunto seguinte a posição do elemento indicada no
parâmetro da função.
*/
position_t adt_after(position_t){


}

/*
Retorna a posição do último elemento da lista-conjunto.
*/
position_t adt_last(set_t){


}

/*
Retorna a posição na lista-conjunto do elemento indicado no parâmetro da função.
*/
position_t adt_position(set_t, int){


}


/** Operadores da TAD set_t **/


/*
Recuperação (pode ser de um arquivo pré-definido ou digitação) e armazenamento dos elementos
de um conjunto, eliminando os elementos que não pertencerem ao conjunto US bem como os
elementos repetidos. Por final, retorna o conjunto armazenado.
*/
set_t getFilteredSet(void){


}

/*
Realiza a união dos sets C1 e C2.
*/
set_t unionSet(set_t, set_t){


}
