/* Estrutura encadeada para pilhas */

typedef struct noh noh;

struct noh{
	int elem;
	noh *prox;
};

typedef noh *pilha;

/* Variaveis globais */

int i;
char c, expr[200], erro;

pilha P;

/*Prototipos das funcoes processamento expressao */

/*Pega cada digito do operando e encontra seu valor numerico */

int FormarNumero(void);

/* Desempilha 2 operandos, aplica-lhes o operador conforme o caractere (+ ou *) e empilha resultado da operacao */

void ExecutarOperacao(void);

/*Prototipos das funcoes para operacoes em pilhas*/

void Empilhar(int, pilha*);
void Desempilhar(pilha*);
int Topo(pilha);
void InicPilha(pilha*);
char Vazia(pilha);

/*Prototipos das funcoes p/ percorrer a expressao*/

/* Percorre a expressao ate encontrar o primeiro caractere nao-branco, retornando-o */

char PegaNaoBranco(void);

char ProxCarac(void);
void InicExpr(void);

void main(){

	int num, val;

/*Leitura da expressao, inicializacao da pilha e preparo para comecar o percurso na expressao */

	write("Digite a expressao: ");
	read(expr); 
	InicPilha(&P); 
	erro = 0; 
	InicExpr();

/* Processo repetitivo percorrendo a expressao, empilhando os operandos e executando as operacoes aritmeticas O processo termina quando for encontrado o fim da expressao ou um erro na mesma */

	while(1){
		c = PegaNaoBranco();
		if(c == ’\0’) 
			break;

1 /* Formacao e empilhamento de um operando */
2 if(isdigit(c)){
3 /* FormarNumero deixa a variavel c
4 com o proximo caractere depois
5 do numero */
6 num = FormarNumero();
7 Empilhar(num, &P);
8 }
9 /* Execucao de uma operacao aritmetica,
10 desempilhando dois operandos e empilhando
11 o resultado; tambem sinaliza casos de
12 erros na expressao */
13 else if(c == ’+’ || c == ’*’){
14 /* ExecutarOperacao nao deixa a variavel c
15 com o proximo caractere depois operador*/
16 ExecutarOperacao();
17 if(erro == 1) break;
18 c = ProxCarac();
19 }
20 else {erro = 1; break;}
21 2
o}período de 2018 Loubach, Lourenço CES11 - Algoritmos e Estruturas de Dados ITA 65/70 /* Fim do while */
Exercícios resolvidos (cont.)
Polonesa sufixa para expressões aritméticas – solução
1 /* Final do processo repetivo com teste de erro
2 e escrita do resultado */
3
4 if(!erro){
5 /* Prevendo o caso da expressao ser vazia */
6 if(Vazia(P)) val = 0;
7 else{
8 val = Topo(P); Desempilhar(&P);
9 if(!Vazia(P)) erro = 1;
10 }
11 }
12 if(erro) write("Erro na expressao!");
13 else write("Valor da expressao = ", val);
14 }/* Final da funcao main */
2
o período de 2018 Loubach, Lourenço CES11 - Algoritmos e Estruturas de Dados ITA 66/70
Exercícios resolvidos (cont.)
Polonesa sufixa para expressões aritméticas – solução
1 /* Funcao para formar um numero a partir de
2 seus digitos */
3
4 int FormarNumero(){
5 int num;
6 num = c - ’0’; c = ProxCarac();
7 while(isdigit(c)){
8 num = 10 * num + c - ’0’;
9 c = ProxCarac();
10 }
11 return num;
12 }
2
o período de 2018 Loubach, Lourenço CES11 - Algoritmos e Estruturas de Dados ITA 67/70
Exercícios resolvidos (cont.)
Polonesa sufixa para expressões aritméticas – solução
1 /* Funcao para executar operacao aritmetica
2 detectando casos de erro na expressao */
3 void ExecutarOperacao(){
4 int val;
5 if(Vazia(P)){
6 erro = 1; return;
7 }
8 val = Topo(P);
9 Desempilhar(&P);
10 if(Vazia(P)){
11 erro = 1; return;
12 }
13 if(c == ’+’)
14 val += Topo(P);
15 else
16 val *= Topo(P);
17
18 Desempilhar(&P);
19 Empilhar(val, &P);
20 }
2
o período de 2018 Loubach, Lourenço CES11 - Algoritmos e Estruturas de Dados ITA 68/70
Exercícios resolvidos (cont.)
Polonesa sufixa para expressões aritméticas – solução
1 /* Funcoes para percorrer a expressao digitada */
2
3 char PegaNaoBranco(){
4 while( isspace(expr[i]) ||
5 ( iscntrl(expr[i]) && expr[i] != ’\0’)) i++;
6 return expr[i];
7 }
8
9 char ProxCarac(){
10 i++;
11 return expr[i];
12 }
13
14 void InicExpr(){
15 i = 0;
16 }