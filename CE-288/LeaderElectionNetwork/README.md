## CE-288 

### Projeto de Exame
### Leader Election for UAV Swarm with Limited Range Communication

Implementação de Leader Election em uma rede de drones decentralizada, com limitações de comunicação e conhecimento local. A rede também dispõe de métricas de conectividade e robustez para a tomada de decisões.





BEGIN
WHILE DISCONNECTED
    REGROUP
IF NO LEADER
    START ELECTION
    FINISH ELECTION
ELSE
    LISTEN COMM
    FIND NEIGHBORS, LEADER, GUIDELINE
    EXECUTE ACTION