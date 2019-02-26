/**

	Lab 01 - CES-11 - Armazenamento e manipulação de números
	inteiros muito grandes em encadeamentos de estruturas

	Nicholas Scharan Cysne - T22.1				16/08/18

**/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef struct cell cell;
typedef int boolean;

const int TRUE = 1;
const int FALSE = 0;

struct cell {														// Estrutura de matriz de células para cada 4 números

	int data;														// Número a ser guardado
	cell * nextCell;												// Ponteiro para a próxima célula
	cell * prevCell;												// Ponteiro para a célular anterior
	cell * nextNumber;												// Ponteiro para próximo número em mesma posição de célula
};

/** Mensagem inicial **/

void initialMessage(){												// Mensagem de Inicio de Programa

	printf("\nEstrutura de Armazenamento de Dados - Lab 01");
	printf("\nEscolha a opção que deseja realizar:\n");
	printf("\n01 - Armazenamento de números e impressão.");
	printf("\n02 - Soma de N números.\n\n - ");	
}

/** Verificação de dados **/

int isValid(char * number){											// Verificação se é um número válido
	
	int sizeReceived = strlen(number);								// Salva o tamanho da string 		
	boolean valid = TRUE;

	for(int i = 0; (i < sizeReceived) && (valid != FALSE); i++)		// Checagem de cada caractere para ver se o número é válido
		valid = isdigit(number[i]);									// Retorna 0 ou diferente para cada caractere

	return valid;													
}

/** Criação de próxima célula na Lista **/

void createCell(cell * p){											// Cria próxima célula depois de p

	p->nextCell = (cell *) malloc (sizeof(cell));					// Aloca espaço de memória na próxima célula
	p->nextCell->prevCell = p;
	p->nextCell->nextCell = NULL;									// Coloca os ponteiros próximos em NULL
	p->nextCell->nextNumber = NULL;
	p->nextCell->data = 0;
}

/** Criação da própria célula **/

cell * create(){													// Cria uma célula para o ponteiro especificado

	cell * source = (cell *) malloc (sizeof(cell));					// Alocação de memória
	source->nextCell = NULL;										// Coloca todos os ponteiros vindos deste em NULL
	source->prevCell = NULL;
	source->nextNumber = NULL;
	source->data = 0;												// Zera os dados da célula

	return source;													// Retorna o endereço do espaço de memória criado
}

/** Encontra a última célula da lista **/

cell * last(cell * p){												// Leva o ponteiro à última célula da lista

	cell * q;														// Ponteiro auxiliar
	for(q = p; q->nextCell != NULL; q = q->nextCell);				// Leva q à última posição
	return q;														// Retorna o esdereço da última posição
}

/** Impressão de todos os valores contidos na estrutura **/

void print(cell * source){											// Partindo da origem, imprime todos os números listados

	cell * p, * q;													// Ponteiros auxiliares na impressão
	if(source->nextNumber != NULL)
		 p = source->nextNumber;									// Aloca o primeiro ponteiro no início da estrutura
	else p = source;

	while(p != NULL){												// Caso contrário, imprime os números enquanto p não chega ao fim
		for(q = last(p); q != NULL; q = q->prevCell)				// Aloca q onde p está e imprime os dados presentes nas células daquele local
			if(q->prevCell != NULL)
				 printf("%04d ", q->data);
			else printf("%d ", q->data);
		
		p = p->nextNumber;											// Para para o próximo número
		printf("\n");
	}
}

/** Atualização da estrutura de dados lendo e armazenando novo número **/

void read(cell * source){											// Leitura via Console e Armazenamento de Dados na Estrutura

	char answer;													// Verifica se deseja adicionar mais números
	char dataReceived [101], dataCopied[5];							// Número a ser armazenado: Máximo de 100 algarismos e bloco de 4 algarismos a ser registrado
	int sizeReceived, numberOfCells = 0, sizeNumber;				// Qunatidade de algarismos e Número de células a serem criadas
	cell * p, *q;													// Ponteiro auxiliar na construção da estrutura

	scanf("%s", dataReceived);										// Leitura do número
	sizeReceived = strlen(dataReceived);							// Determinação do tamanho da string

	while(!isValid(dataReceived)){									// Repete a inserção até encontrar um número válido

		printf("Inválido! Digite outro número:\n\n - ");
		scanf("%s", dataReceived);									// Nova tentativa
		sizeReceived = strlen(dataReceived);
	}

	for(sizeNumber = 0; dataReceived[sizeNumber] == '0'; sizeNumber++);
	sizeNumber = sizeReceived - sizeNumber;							// Checa quantas casas de 0 à esquerda existem

	if(sizeNumber%4 != 0)
		 numberOfCells = sizeNumber/4 + 1;							// Quantas células são necessaŕias para o armazenamento
	else numberOfCells = sizeNumber/4;

	for(p = source; p->nextNumber != NULL; p = p->nextNumber);					
	p->nextNumber = create();
	q = p->nextNumber;

	for(int i = 0; i < numberOfCells; i++){							// Cria e armazena em cada célula um pacote de 4 algarismos

		strcpy(dataCopied, "0000");									// Zera a área de transferência para a próxima cópia
																	// Copia os 4 últimos algarismos do número para a área de transferência
		for(int j = 0; j < 4 && (sizeReceived - 1 - 4*i - j) >= 0; j++)
			dataCopied[3 - j] = dataReceived[sizeReceived - 1 - 4*i - j];

		q->data = atoi(dataCopied);									// Transforma a string copiada em tipo int		

		if(i != numberOfCells - 1){									// Checa se é necessário outra célula
			createCell(q);											// Cria próxima célula
			q = q->nextCell;										// Já deixa pronto na próxima
		}
	}

	printf("\nDeseja mais valores? (s/n) ");						// Verificação de mais armazenamento
	scanf(" %c", &answer);											// Resposta do usuário

	if(answer == 's' || answer == 'S'){	
		printf("\n - ");
		read(source);												// Atualiza o origin novamente
	}
}

/** Libera a memória alocada **/

void freeAll(cell * source){										// Libera a memória dinâmica alocada

	cell * p, * q;
	
	for(p = source; p->nextNumber != NULL; p = p->nextNumber);
	for(q = last(p)->prevCell; q != NULL; q = q->prevCell)
		free(q->nextCell);
}

/** Soma de valores introduzidos pelo usuário **/

void sumAll(cell * source){											// Armazenamento de dados e soma de valores

	char * result, * dataCopied;									// String do resultado ao final
	cell * sum, * p, * q, * t;
	int numberOfCells, sizeFirstCell, storage, i;

	printf("\n*************************************\n");
	printf("\nDigite os números que deseja somar:\n\n - ");
	
	read(source);

	sum = create();

	for(p = source->nextNumber; p != NULL; p = p->nextNumber){
	
		q = p;
		t = sum;

		t->data += q->data;

		if(t->data > 9999){
			t->data -= 10000;
			if(t->nextCell == NULL)
				createCell(t);		
			t->nextCell->data++;		
		}

		while(q->nextCell != NULL){

			if(t->nextCell == NULL)
				createCell(t);
			t = t->nextCell;
			q = q->nextCell;

			t->data += q->data;

			if(t->data > 9999){
				t->data -= 10000;
				if(t->nextCell == NULL)
					createCell(t);		
				t->nextCell->data++;		
			}
		}
	}

	printf("\nSoma Total: ");
	print(sum);
	freeAll(sum);
}

int main(){

	/** Declaração de Variáveis e Origem da Estrutura de Dados **/

	cell * origin = create();										// Origem da estrutura de dados
	int answer;														// Verifica se deseja adicionar mais números

	/** Mensagem Inicial do Programa **/

	initialMessage();												// Mensagem inicial do programa
	scanf("%d", &answer);											// Qual programa executar

	/** Escolah entre os programas 01 - Armazenamento ou 02 - Soma **/

	switch(answer){													// Escolha entre simples armazenamento e impressão ou soma de N valores

		case 1: printf("\n*************************************\n");
				printf("\nDigite o número que deseja armazenar:\n - ");
				read(origin);
				printf("\nValores digitados:\n\n");					// Armazenamento
				print(origin);										// Impressão da estrutura
				break;
		case 2: sumAll(origin);										// Imprime a soma dos números
				break;
		default: return 1;
	}

	/** Liberação da Memória Dinâmica e dos Ponteiros Utilizados **/

	freeAll(origin);

	return 0;
}