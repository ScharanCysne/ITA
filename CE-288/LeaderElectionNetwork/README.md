## CE-288 

### Projeto de Exame
### Leader Election for UAV Swarm with Limited Range Communication

Implementação de Leader Election em uma rede de drones decentralizada, com limitações de comunicação e conhecimento local. A rede também dispõe de métricas de conectividade e robustez para a tomada de decisões.

-- Instruções:

- Executar o arquivo main.py.
- Dependendo do poder de processamento do seu computador a execução pode ficar lenta dado que são criados 21 processos de python, todos comunicando entre si.
- Ao final de cada episódio (15 segundos ou todos os drones destruídos) todos os processos são fechados.
- Congestionadmentos de mensagens podem causar uma demora a mais no fechamento dos processos, CTRL+C no terminal nesses casos fecha todas as instâncias abertas.

-- Simplificações 

A fim de focar no algoritmo de Leader Election, algumas métricas como Algebraic COnnectivity e Betweenness Centrality foram calculadas por um controlador externo (Env), evitando cálculos de estimativa desnecessários para a simulação que deixaria o processo ainda mais lento, aqui queremos mostrar apenas que o algoritmo de leader election focando nessas métricas funciona melhor que o Raft simples.