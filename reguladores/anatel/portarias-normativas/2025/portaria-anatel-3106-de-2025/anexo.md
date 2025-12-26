ANEXO
DIRETRIZES E PROCEDIMENTOS PARA CONTROLE DE ACESSO AO REPOSITÓRIO GIT DA ANATEL
CAPÍTULO I
DO OBJETO
Art. 1º Esta portaria estabelece as diretrizes, responsabilidades, limitações e requisitos normativos aplicáveis ao acesso ao repositório Git da Anatel, com base nos Termos de Ciência e Responsabilidade (TCR) vigentes, referentes aos seguintes tipos de acesso:
I - Soluções departamentais (baixo impacto organizacional); e
II - Soluções institucionais/legados (alto impacto organizacional).
Art. 2º A presente portaria formaliza, para fins de governança e segurança da informação, todos os requisitos de uso, obrigações, vedações, responsabilidades, riscos, mecanismos de controle e regras aplicáveis para concessão e manutenção desses acessos.
CAPÍTULO II
DA ABRANGÊNCIA
Art. 3º As disposições desta portaria se aplicam:
I - Aos administradores do repositório Git (GIDS/SGI);
II - Aos Product Owners (PO) das soluções de TIC;
III - Aos desenvolvedores e equipes técnicas vinculadas a contratos de TIC;
IV - Às chefias das áreas gestoras das soluções de TIC; e
V - Aos servidores autorizados a acessar repositórios departamentais.
CAPÍTULO III
DOS RISCOS E CONSEQUÊNCIAS OPERACIONAIS
Art. 4º O acesso inadequado ao repositório Git poderá:
I - Comprometer o histórico de versionamento;
II - Corromper código-fonte;
III - Introduzir vulnerabilidades;
IV - Causar perda de integridade de artefatos;
V - Gerar incidentes de segurança;
VI - Impactar sistemas em produção;
VII - Afetar contratos e SLAs; e
VIII - Prejudicar a rastreabilidade técnica e funcional das soluções.
Art. 5º O risco é particularmente elevado para repositórios institucionais (legados), que armazenam código-fonte de soluções estratégicas da Anatel, razão pela qual exigem regras mais rígidas e Termos de Ciência e Responsabilidade específicos.
Parágrafo único. Em virtude das hipóteses previstas no presente artigo, o acesso será sempre excepcional, monitorado e restrito.
CAPÍTULO IV
DOS TIPOS DE ACESSO
Art. 6º Com base nos Termos de Ciência e Responsabilidade, disponibilizados nos anexos desta portaria, o acesso poderá ser:
I - Acesso Somente Leitura
a) Aplicável, mediante justificativa e Termo de Ciência e Responsabilidade (TCR), a:
1 - repositórios de soluções departamentais;
2 - repositórios institucionais (sob maior controle).
b) Permitirá:
1 - visualizar código-fonte;
2 - revisar histórico;
3 - analisar commits, branches e documentos técnicos.
II - Acesso Leitura e Escrita
a) Aplicável mediante justificativa e TCR, permitindo:
1 - editar arquivos;
2 - criar branches;
3 - submeter commits; e
4 - abrir merge requests.
Art. 7º Tanto para soluções departamentais quanto para soluções institucionais/legadas, o acesso exigirá:
I - Justificativa funcional;
II - Autorização da Área Gestora da solução de TIC;
III - Validação da GIDS/SGI; e
IV - Assinatura de Termo de Ciência e Responsabilidade (TCR) específico, conforme anexos a esta portaria.
CAPÍTULO V
DAS RESTRIÇÕES E VEDAÇÕES
Art. 8º Independentemente do tipo de acesso, é vedado:
I - Alterar código-fonte sem autorização;
II - Excluir branches, tags ou commits sem autorização;
III - Sobrescrever histórico (force push) sem permissão expressa da GIDS;
IV - Modificar pipelines, integrações ou configurações avançadas;
V - Alterar regras de proteção de branch;
VI - Copiar, divulgar ou redistribuir código-fonte sem autorização;
VII - Comprometer rastreabilidade, integridade ou versionamento;
VIII - Utilizar o acesso para fins privados, externos ou inadequados; e
IX - Inserir códigos maliciosos, backdoors ou práticas inseguras.
Art. 9º Para repositórios institucionais, vedações adicionais poderão constar do TCR específico.
CAPÍTULO VI
DAS RESPONSABILIDADES
Art. 10. O autorizado deverá:
I - Atuar estritamente dentro das permissões concedidas;
II - Manter sigilo sobre informações técnicas;
III - Observar o PPSI, normas de desenvolvimento seguro e diretrizes da SGI;
IV - Garantir integridade e rastreabilidade de commits;
V - Submeter alterações a revisão técnica quando aplicável;
VI - Atuar conforme orientações da GIDS; e
VII - Responder individualmente por mau uso, negligência ou ações indevidas.
Art. 11. O responsável na Área Gestora pela solução de TIC incumbe:
I - Validar a necessidade funcional do acesso;
II - Justificar pedidos de acesso para repositórios institucionais;
III - Comunicar alterações de vínculo ou necessidade de revogação;
IV - Assegurar alinhamento entre necessidades funcionais e segurança;
V - Proibir compartilhamento de acessos; e
VI - Solicitar acesso apenas quando indispensável.
CAPÍTULO VII
DO MONITORAMENTO, CONTROLE E AUDITORIA
Art. 12. Todo acesso ao Git:
I - Será monitorado por logs;
II - Poderá ser auditado pela SGI;
III - Estará sujeito a rastreamento permanente; e
IV - poderá ser suspenso imediatamente em caso de risco, mau uso ou violação.
CAPÍTULO VIII
DAS SANÇÕES
Art. 13. Identificado o mau uso do acesso concedido, o autorizado estará sujeito a:
I - Suspensão imediata do acesso;
II - Responsabilização administrativa;
III - Registro na área de segurança da informação;
IV - Comunicação à chefia imediata;
V - Abertura de procedimento disciplinar; e
VI - Comunicação ao Encarregado pela Proteção de Dados quando envolver dados pessoais.
CAPÍTULO IX
DA VIGÊNCIA E REVOGAÇÃO
Art. 14. O acesso concedido:
I - Vigorará a partir da assinatura do TCR;
II - Permanecerá enquanto durar a necessidade operacional;
III - Será automaticamente revogado ao cessar o motivo; e
IV - Poderá ser revogado a qualquer tempo por risco ou decisão da SGI.
ANEXOS ÀS DIRETRIZES E PROCEDIMENTOS PARA CONTROLE DE ACESSO AO REPOSITÓRIO GIT DA ANATEL
Anexo I - Modelo de Termo de Ciência e Responsabilidade (TCR) para acesso somente leitura ao Repositório Git:
Termo de Ciência e Responsabilidade – <nº do Termo>
Autorizado: < identificação do Servidor solicitante >
Autorizador 1: < Responsável pela área gestora da solução de TIC >
Autorizador 2: < Product Owner da solução de TIC, quando não for este o solicitante >
Concedente: Gerência de Planejamento, Desenvolvimento e Segurança de Sistemas (GIDS)
Objeto (Descrição detalhada do acesso a ser concedido):
O presente Termo registra a ciência e responsabilidade do AUTORIZADO quanto ao acesso excepcional, em MODO SOMENTE LEITURA, ao repositório do Git em operação na Anatel, em caráter restrito, controlado e temporário.
Identificação dos documentos que estabelecem as Diretrizes, Restrições e Condições do Acesso a ser concedido.
Todas as diretrizes, restrições e condições de acesso, aplicáveis ao AUTORIZADO e à Área negocial responsável pela solução de TIC estão definidas nas portarias: <Portaria de diretrizes e procedimentos gerais> e <Portaria de diretrizes e procedimentos específicos>.
Data de validade: < data limite de validade do acesso >
Anexo II - Modelo de Termo de Ciência e Responsabilidade (TCR) para acesso de leitura e escrita ao Repositório Git:
Termo de Ciência e Responsabilidade – <nº do Termo>
Autorizado: < identificação do Servidor solicitante >
Autorizador 1: < Responsável pela área gestora da solução de TIC >
Autorizador 2: < Product Owner da solução de TIC, quando não for este o solicitante >
Concedente: Gerência de Planejamento, Desenvolvimento e Segurança de Sistemas (GIDS)
Objeto (Descrição detalhada do acesso a ser concedido):
O presente Termo registra a ciência e responsabilidade do AUTORIZADO quanto ao acesso excepcional, em MODO LEITURA e ESCRITA, ao repositório do Git em operação na Anatel, em caráter restrito, controlado e temporário.
Identificação dos documentos que estabelecem as Diretrizes, Restrições e Condições do Acesso a ser concedido.
Todas as diretrizes, restrições e condições de acesso, aplicáveis ao AUTORIZADO e à Área negocial responsável pela solução de TIC estão definidas nas portarias: <Portaria de diretrizes e procedimentos gerais> e <Portaria de diretrizes e procedimentos específicos>.
Data de validade: < data limite de validade do acesso >
