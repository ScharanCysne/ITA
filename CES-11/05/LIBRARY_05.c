#include "LIBRARY_05.h"

graph_t * read_graph(){

	int digraph, origin, destination, weight, last_origin;
	edge_t * neighbors_aux = NULL;
	vertex_t vertexes_aux = NULL;

	G = (graph_t *) malloc (sizeof(graph_t));

	fscanf(fin, " %d", &G->order);
	fscanf(fin, " %d", &digraph);
	fscanf(fin, " %d %d %d", &origin, &destination, &weight);
		
	G->vertexes = (vertex_t *) malloc (G->order * sizeof(vertex_t));

	for(int i = 0; i < G->order; i++)
		

	last_origin = origin;

	if(digraph)
		 G->is_digraph = true;
	else G->is_digraph = false;

	while(origin != 0){

		if(0 < origin && origin <= G->order && 0 < destination && destination <= G->order){

			vertexes_aux = G->vertexes[origin - 1];
			neighbors_aux = G->vertexes[origin - 1].neighbors;

			while(neighbors_aux->next != NULL)
				neighbors_aux = neighbors_aux->next;

			neighbors_aux->next = (edge_t *) malloc (sizeof(edge_t));
			neighbors_aux = neighbors_aux->next;
			neighbors_aux->v = destination;
			neighbors_aux->weight = weight;
			neighbors_aux->next = NULL;
		}
		
		fscanf(fin, " %d %d %d", &origin, &destination, &weight);	
	}

	return G;
}

void print_graph(graph_t * root){

	edge_t * neighbors_aux;

	for(int i = 0; i < root->order; i++){

		printf(" Origin: %d \n\n\t Neighbors: ", i + 1);

		if(neighbors_aux == NULL)
			printf("0 neighbors.\n");
		else while(neighbors_aux != NULL){

			printf("%d Weight: %d \n", neighbors_aux->v, neighbors_aux->weight);
			neighbors_aux = neighbors_aux->next;
		}
	}
}

void free_graph(graph_t * root){


}