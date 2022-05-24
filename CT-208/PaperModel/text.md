Given the root of a tree of resources, where a node i of the tree represents a resource i, implement the following functions:

void grantAccess(i) - grants access of resource i to a user.
void revokeAccess(i) - revoke access of resource i to a user.
bool hasAccess(i) - returns if the user has access to the resource i

All grant/revoke actions are done recursevely, so if it is granted access to the user of a resource i, it is also granted access to all its children and children of children and so on.

Node {
    private int id; 
    private bool access;
    private Node* children; 
}

---------
- The tree may be empty. 
- Resources will always exists (but the candidate should ask what happens if a resource doesnt exist) OK, boa demais
- All resources begin with access=false

Possible approach: 
    2 BFS to grant/revoke - O(N), O(D)
    Aux dict to has access to map visited - O(1), O(n)

- Fez perguntas no inicio, ótimo (empty, inputs, etc)
- Fez um exemplo no inicio, ótimo
- Disse as complexidades antes O(n), O(n), mas falou O(n) no espaço, mas DFS seria a altura da árvore, não? achieved O(1) in time for hasAccess, great
- 10min falando, mas foi bem completo - perfeito
- N entendi bem pq vc começou a criar uma nova classe Resources sendo q eu já tinha te dado o Node, perdeu um certo tempo pq eu falei q podia só implementar as funções separadamente
- DFS or BFS, eu pessoalmente gosto mais de BFS
- Acho q com BFS seria mais simples iterar sobre a árvore e dar um break qndo achar
- Ao invés de passar uma string vc n poderia passar só um bool true/false e usar esse cara pra setar cada nó? Removeria a lógica do if e talvez melhoraria um pouco a performance dado q vc tá comparando strings
- o map eu faria parecia mas de todos os nós, inicializaria no search e update no grant/revoke
- bug em operation(n, "grant")
- vc n está comparando nada com "revoke", de novo, pode simplificar a lógica
- qndo falei pra procurar bug, n achou o bug em operation mas achou em search
- 

          1
         / \
        2   3
       /
      4

grantAccess(2)
revokeAccess(2)
hasAccess(4)
---------------------------------------------------------------------------------------------------------------------------------------
https://leetcode.com/problems/numbers-with-same-consecutive-differences/
Numbers With Same Consecutive Differences

Return all non-negative integers of length n such that the absolute difference between every two consecutive digits is k.

Note that every number in the answer must not have leading zeros. For example, 01 has one leading zero and is invalid.

You may return the answer in any order.

Input: n = 3, k = 7
Output: [181,292,707,818,929]

Input: n = 2, k = 1
Output: [10,12,21,23,32,34,43,45,54,56,65,67,76,78,87,89,98]

----------
- N >= 1
- k pode ser 0
- If we are asked to return numbers of a single digit (i.e. N=1), then regardless of K, all digits are valid, including zero. We treat this as a special case in the code, since in our implementation of DFS function, we will never return zero as the result.

Complexity:
Let N be the number of digits for a valid combination, and K be the difference between digits.

Essentially, the execution of the algorithm will unfolder itself as a binary tree, where each node in the tree represents an invocation of the DFS() function. The execution of the DFS() function itself takes a constant time. Therefore, the overall time complexity is proportional to the number of nodes in the execution binary tree.

Time: 2**N
Space: 2**N
