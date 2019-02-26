#include <stdio.h>
#include <stdlib.h>

int main(){
	
	FILE * entrada, * saida;
	int dec, octal, hexa, temp;
	char type;
	int flag_h = 0, flag_d = 0, flag_o = 0;

	entrada = fopen("entrada.txt", "r");
	saida  = fopen("saida.txt", "w");

	while(!feof(entrada)){

		fscanf(entrada, " %c ", &type);

		switch(type){

			case 'H':	fscanf(entrada, "%x", &temp);
						hexa = temp;
						flag_h = 1;
						break;
			case 'O': 	fscanf(entrada, "%o", &temp);
						octal = temp;
						flag_o = 1;
						break;
			case 'D': 	fscanf(entrada, "%d", &temp);
						dec = temp;
						flag_d = 1;
						break;
			default: 	break;

		}

		if (flag_h == 1){
			
		}
		if (flag_o == 1){

		}
		if (flag_d == 1){

		}



	}

	return 0;
}