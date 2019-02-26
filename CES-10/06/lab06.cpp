/*  Lab 06: Operações com Polinômios  */
/*  Nicholas Scharan Cysne     T22.1  */
/*  CES-10		       Prof. Armando  */
/*  Compilado com CodeBlocks 17.04    */

#include <stdio.h>
#include <stdlib.h>

#define GRAU_MAX 11

int main(){

	char oper, sinal = '+', x, chap;							// operação a ser realizada e verifica o fim do polinomio
	float coef1[GRAU_MAX], coef2[GRAU_MAX], temp_coef;			// coeficientes
	int exp, i, j, k = 1, flag, grau1, grau2, grau3, reg;		// expoentes, contadores de fprintf e flag

	float result_coef[2 * GRAU_MAX];							// coeficientes do polinomio resultante

	FILE * entrada, * saida;									// inicialização de arquivos externos

	entrada = fopen("entrada.txt", "r");					
	saida = fopen("saida.txt", "w");

	fscanf(entrada, "%c", &oper);								// armazena a 1a operação a ser realizada

	while (oper != 'F'){										// verifica o fim de arquivo

		for(i = 0; i < GRAU_MAX; i++)							// Zera o polinomio
			coef1[i] = 0;
		for(i = 0; i < GRAU_MAX; i++)
			coef2[i] = 0;
		for(i = 0; i < 2 * GRAU_MAX; i++)
			result_coef[i] = 0;
		reg = 1;												// Retorna o registro em P1
		flag = 0;												// Retorna o flag em 0
		grau1 = 0;												// Retorna os graus de P1 e P2 em 0
		grau2 = 0;
		grau3 = 0;

		while (reg == 1 || reg == 2){
			do{													// Lê os monomios e armazena em cada local de memória do vetor correspondente ao expoente 
				fscanf(entrada, " %c ", &sinal);				// Lê o sinal do monômio

				if(sinal != ';')
					fscanf(entrada, " %f %c %c %d ", &temp_coef, &x, &chap, &exp);

				if(sinal == '-')
					temp_coef *= (-1); 							// Torna o coeficiente negativo se o sinal é negativo
																// Por algum motivo coef1[exp] = (-1)*coef1[exp] não funciona nesta parte
				if(reg == 1)
					 coef1[exp] = temp_coef;					// Registra em P1 se reg = 1
				else coef2[exp] = temp_coef;					// Registra em P2 se reg = 2

			}	while(sinal != ';');							// Fim do polinõmio
			reg++;
		}

		switch(oper){
			case 'S':											// Algoritmo da Soma
			case 's':	for(i = 0; i < GRAU_MAX; i++)
							result_coef[i] = coef1[i] + coef2[i];
						break;
			case 'P':											// Algoritmo da Multiplicação
			case 'p':	for(i = 0; i < GRAU_MAX; i++)
							for(j = 0; j < GRAU_MAX; j++)
								result_coef[j + i] = result_coef[j + i] + (coef1[i] * coef2[j]);
						break;
			case 'Q':											// Algortimo da Divisão (Método da Chave)
			case 'q':	for(i = 0; i < GRAU_MAX; i++){			// Análise dos graus de p1 e p2
							if(coef1[i] != 0)
								grau1 = i;
							if(coef2[i] != 0)
								grau2 = i;
						}

						while(grau1 >= grau2){								
							result_coef[grau1 - grau2] = coef1[grau1]/coef2[grau2];
							for(i = (grau1 - grau2); i <= grau1; i++)
								coef1[i] = coef1[i] - (coef1[grau1]/coef2[grau2])*coef2[i - grau1 + grau2];
							grau1--;
						}
						break;
			default: break;
		}

		for(i = 0; i < 2*GRAU_MAX; i++){			// Análise do grau de P_result
			if(result_coef[i] != 0)
				grau3 = i;
		}
	
		fprintf(saida, "%2d:", k);								// Print qual numero da operação

		for(i = 0; i < 2 * GRAU_MAX; i++){						// File Print dos resultados
			if(result_coef[2*GRAU_MAX -1 - i] != 0){			// Print só nos coeficientes diferentes de 0
				if(result_coef[2*GRAU_MAX -1 - i] < 0){
					 sinal = '-';
					 result_coef[2*GRAU_MAX -1 - i] = (-1)*result_coef[2*GRAU_MAX -1 - i];
				}
				else sinal = '+';

				if (2*GRAU_MAX -1 - i != grau3 || sinal == '-')
					fprintf(saida, " %c", sinal);
				
				fprintf(saida, " %g", result_coef[2*GRAU_MAX -1 - i]);
				if(2*GRAU_MAX -1 - i != 0){
					fprintf(saida, "x");
					if(2*GRAU_MAX -1 - i != 1)
						fprintf(saida, "^%d", 2*GRAU_MAX -1 - i);
				}
			}
			if(result_coef[i] != 0)								// Flag para caso do polinomio nulo
				flag = 1;
		}
		if(flag == 0)
			fprintf(saida, " 0");								// Print 0 se polinomio nulo

		if(oper == 'Q' || oper == 'q'){							// Se for divisão, há o resto
			flag = 0;
			fprintf(saida, " com resto");
			for(i = 0; i < GRAU_MAX; i++){
				if(coef1[GRAU_MAX -1 - i] != 0){
					
					if(coef1[GRAU_MAX -1 - i] < 0){
					 sinal = '-';
					 coef1[GRAU_MAX -1 - i] = (-1)*coef1[GRAU_MAX -1 - i];
					}
					else sinal = '+';

					if (GRAU_MAX -1 - i != grau1 || sinal == '-')
						fprintf(saida, " %c", sinal);

					fprintf(saida, " %g", coef1[GRAU_MAX -1 - i]);
					if(GRAU_MAX -1 - i != 0){
						fprintf(saida, "x");
						if(GRAU_MAX -1 - i != 1)
							fprintf(saida, "^%d", GRAU_MAX -1 - i);
					}
				}
				if(coef1[i] != 0)
					flag = 1;
			}	
			if(flag == 0)
				fprintf(saida, " 0");
		}
		fscanf(entrada, "%c", &oper);							// Armazena qual a próxima operação a ser realizada
		fprintf(saida, "\n");
		k++;
	} 
	return 0;
}