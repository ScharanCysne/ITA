#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef int vertex_index;

typedef struct edge{

	int weight;
	vertex_index v;
	struct edge * next;
} edge_t;

typedef struct vertex{

	// Three state:
	//		white: Neither entry nor exit time were set
	//		Grey, and Black
	int entry_time;		// Grey
	int exit_time;		// Black
	edge_t * neighbors;
} vertex_t;

typedef struct graph{
	
	int order;
	vertex_t * vertexes;
	bool is_connected;
	bool is_digraph;
} graph_t;

graph_t * G;
FILE * fin;

graph_t * read_graph();
void print_graph(graph_t * root);
void free_graph(graph_t * root);