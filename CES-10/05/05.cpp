#include <stdio.h>
#include <stdlib.h>

int main(){

	//Declaração de Variaveies
	FILE * entrada, * saida;
	int bolo, gelatina, fruta, sorvete;
	
	//Abertura de arquivos
	entrada = fopen("C:\\Lab4\\entrada5.txt", "r");
	saida = fopen("C:\\Lab4\\Nicholas_Scharan_Cysne_04.txt", "w");
	
	//Mensagem Inicial
	fprintf(saida, "Programa cardapio De Sobremesas\n");
	fprintf(saida, "Opcoes: Bolo, Gelatina, Fruta, Sorvete\n");
	fprintf(saida, "Os pedidos de hoje sao:\n");
	fprintf(saida, "-----\n");
	
	//Leitura de valores
	while(fscanf(entrada, "%d ", &bolo) > 0){

		fscanf(entrada, "%d %d %d", &gelatina, &fruta, &sorvete);

		if(bolo != 0){
			fprintf(saida, " %d Bolo", bolo);
			if(bolo > 1)
				fprintf(saida, "s");
		}
		if(gelatina != 0){
			if(bolo != 0 && (fruta != 0 || sorvete != 0))
				fprintf(saida, ",");	
			if(bolo != 0 && fruta == 0 && sorvete == 0)
				fprintf(saida, " e");
			fprintf(saida, " %d Gelatina", gelatina);
			if(gelatina > 1)
				fprintf(saida, "s");
		}
		if(fruta != 0){
			if((bolo != 0 || gelatina != 0) && sorvete != 0)
				fprintf(saida, ",");
			if((bolo != 0 || gelatina != 0) && sorvete == 0)
				fprintf(saida, " e");
			fprintf(saida, " %d Fruta", fruta);
			if(fruta > 1)
				fprintf(saida, "s");
		}
		if(sorvete != 0){
			if(bolo != 0 || gelatina != 0 || sorvete != 0)
				fprintf(saida, " e");
			fprintf(saida, " %d Sorvete", sorvete);
			if(sorvete > 1)
				fprintf(saida, "s");
		}
		fprintf(saida, ".\n");
	}	
	return 0;
}