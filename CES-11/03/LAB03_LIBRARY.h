#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

typedef struct node_st * pilha_t; 

struct node_st { 
    
    int data; 
    struct node_st * next;
};

// inicializa uma pilha vazia 

void adt_initStack(pilha_t node){

    node = NULL;
}

// adiciona um elemento no topo da pilha 

void adt_pushStack(pilha_t * node, int newData){

	node_st * temp;

	temp = *node;
	(*node) = (node_st *) malloc (sizeof(node_st));
	(*node)->data = newData;
	(*node)->next = temp;
}

// remove um elemento do topo da pilha 

void adt_popStack(pilha_t * node){

	node_st * temp;
	
	if(*node != NULL){
		
		temp = (*node);
		(*node) = (*node)->next;
		free(temp);
	} 
	else 
		printf("Delecao em pilha vazia!\n");
}

// retorna <true> quando a pilha encontra−se vazia 

bool adt_emptyStack(pilha_t node){

	return (node == NULL);
}

// retorna o elemento do topo da pilha sem remove−lo 

int adt_topStack(pilha_t node){

	if(!adt_emptyStack(node))
		 return node->data;
	else printf("Pilha Vazia!\n");
}

// Esvazia a pilha
void adt_freeStack(pilha_t * node){

	while(1){
		if(*node != NULL)
			adt_popStack(node);
		else break;
	}
}

/* Função para achar o próximo caractere da expressão */

char nextCarac(char * data, int &i){
	
	i++;
	return data[i];
}

/* Funcao para formar um numero a partir de seus digitos */

int makeNumber(char * data, int &i, char &symbol){

	int num = 0;
	symbol = data[i];

	while(isdigit(symbol)){
		num = 10 * num + symbol - '0';
		symbol = nextCarac(data, i);
	}

	return num;
}

/* Funcao para executar operacao aritmetica detectando casos de erro na expressao */

int executeOper(pilha_t * node, char symbol){

	int val;

	if(*node == NULL)
		return 1;

	val = adt_topStack(*node);
	adt_popStack(node);
	
	if(adt_emptyStack(*node)) 
		return 1;

	if(symbol == '+')
		val += adt_topStack(*node);
	else
		val *= adt_topStack(*node);
	
	adt_popStack(node);
	adt_pushStack(node, val);

	return 0;
}

/* Funcoes para percorrer a expressao digitada */

char nonBlank(char * data, int &i){

	while(isspace(data[i]) || (iscntrl(data[i]) && data[i] != '\0')) 
		i++;

	return data[i];
}