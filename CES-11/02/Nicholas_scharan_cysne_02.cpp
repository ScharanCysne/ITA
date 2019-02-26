/*  	CES-11: Estrutura de Dados	 Lab 02      */
/* 		Nicholas Scharan Cysne        T22.1		   */

/**	
  * The data input is expected through console.
  * Please follow the instructions presented in the console.
  *
  * The Universe Set Us is considered os the example {1, 2, 3, ... , 20}
  *
  * Select between the two libraries below which
  * data structure are you using.
  *
  * vectorAdtSset - Vector Structure
  * nodeAdtSet - Node Structure
  *
  * Uncomment the library desired.
**/

#include "vectorAdtSet.h"			
//#include "nodeAdtSet.h"

int main (){
	
  int Universe[20] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 
                      12, 13, 14, 15, 16, 17, 18, 19, 20}; 
  set_t * C1, * C2;
  char ans = 's';

  adt_initSet(C1);
  adt_initSet(C2);
	
  initMessage();	
  while(ans == 's' || ans == 'S'){


  }
	
	
	
	return 0;
}