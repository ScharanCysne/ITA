#include "LIBRARY_05.c"

int main(int argc, char * arg[]){

	if(!(fin = fopen("graph.dat", "r"))){

		fprintf(stderr, "Error while opening 'graph.dat'\n");
		return 1;
	}

	G = read_graph();		// Produces a new graph from graph.dat
	print_graph(G);
	free_graph(G);
	return 0;
}