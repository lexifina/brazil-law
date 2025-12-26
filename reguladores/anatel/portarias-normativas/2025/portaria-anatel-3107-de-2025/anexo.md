ANEXO
DIRETRIZES E PROCEDIMENTOS PARA CONTROLE DE ACESSO À FERRAMENTA WSO2 EM OPERAÇÃO NA ANATEL
CAPÍTULO I
DO OBJETO
Art. 1º Estabelecer as diretrizes, condições, responsabilidades e limitações relacionadas ao acesso à ferramenta WSO2 em operação na Anatel, com base nos Termos de Ciência e Responsabilidade (TCR) vigentes, contemplando:
I - Gestão de APIs;
II - Orquestração de serviços;
III - Integração de sistemas legados;
IV - Autenticação e controle de acesso;
V - Gestão de identidades;
VI - Governança de serviços; e
Comunicação entre aplicações distribuídas.
Art. 2º A presente portaria formaliza, para fins de governança e segurança da informação, todos os requisitos de uso, obrigações, vedações, responsabilidades, riscos, mecanismos de controle e regras aplicáveis para concessão e manutenção desses acessos.
CAPÍTULO II
DA ABRANGÊNCIA
Art. 3º As disposições desta portaria se aplicam:
I - Administradores da Plataforma WSO2 (GIDS/SGI);
II - Product Owners (PO) das soluções integradas pela plataforma;
III - Aos representantes das áreas negociais gestora da solução de TIC; e
IV - Servidores autorizados a efetuar integrações departamentais.
CAPÍTULO III
DOS RISCOS E CONSEQUÊNCIAS OPERACIONAIS
Art. 4º O Acesso inadequado ao WSO2 pode resultar em:
I - Exposição indevida de APIs ou dados;
II - Falhas de autenticação/autorização;
III - Interrupções de serviços institucionais;
IV - Alteração incorreta de pipelines e fluxos de mediação;
V - Inserção de vulnerabilidades;
VI - Ruptura de integrações críticas entre sistemas;
VII - Degradação ou indisponibilidade de sistemas legados;
VIII - Impacto em SLAs de contratos terceirizados;
IX - Falhas de auditoria e rastreabilidade; e
X - Riscos jurídicos e regulatórios relacionados à LGPD.
Parágrafo único. Em virtude das hipóteses previstas no presente artigo, o acesso será sempre excepcional, monitorado e restrito.
CAPÍTULO IV
DOS TIPOS DE ACESSO
Art. 5º São tipos de acesso passível de ser concedido:
I - Acesso Somente Leitura
a) Esse acesso permitirá:
1 - visualizar APIs;
2 - consultar fluxos de integração;
3 - acompanhar logs (read only);
4 - analisar regras, policies e configurações; e
5 - acessar documentação técnica interna.
II - Acesso Leitura e Escrita
a) Esse acesso permitirá:
1 - criar APIs;
2 - editar definições OpenAPI/Swagger;
3 - desenvolver fluxos de integração;
4 - realizar ajustes em medição (in/out bound);
5 - criar conectores, endpoints e sequences; e
6 - submeter artefatos para teste.
Art. 6º Todo acesso ao WSO2 será:
I - Excepcional;
II - Motivado por necessidade estritamente funcional;
III - Individual e intransferível;
IV - Temporário e revogável;
V - Restrito ao perfil concedido; e
VI - Sujeito a logs, auditoria e monitoramento permanente.
CAPÍTULO V
DAS RESTRIÇÕES E VEDAÇÕES
Art. 7º Independentemente do tipo de acesso, é vedado:
I - Alterar políticas de segurança sem autorização técnica;
II - Publicar APIs em produção sem fluxo formal;
III - Editar pipelines críticos sem validação da GIDS;
IV - Criar endpoints que exponham dados sensíveis;
V - Inserir lógica de integração insegura;
VI - Alterar mecanismos de autenticação;
VII - Sobrescrever artefatos ou configurações protegidas;
VIII - Compartilhar credenciais;
IX - Utilizar o acesso para fins não institucionais;
X - Remover ou modificar configurações essenciais do gateway; e
XI - comprometer a rastreabilidade das integrações.
CAPÍTULO VI
DAS RESPONSABILIDADES
Art. 8º O autorizado deverá:
I - Atuar estritamente dentro do escopo da permissão concedida;
II - Manter sigilo sobre políticas, credenciais, tokens e configurações;
III - Respeitar políticas de desenvolvimento seguro e integrações;
IV - Garantir integridade das APIs e fluxos criados;
V - Submeter alterações a revisão técnica quando aplicável;
VI - Reportar incidentes imediatamente;
VII - Agir conforme orientações da GIDS/SGI;
VIII - Responder individualmente por ações indevidas ou negligentes.
Art. 9º Ao representante da Área Gestora da solução de TIC compete:
I - Validar a necessidade funcional do acesso;
II - Justificar acessos que envolvam integrações institucionais;
III - Solicitar revogação quando cessada a necessidade;
IV - Não autorizar acessos compartilhados;
V - Garantir alinhamento entre requisitos técnicos e segurança; e
VI - Supervisionar o uso dos acessos concedidos.
CAPÍTULO VII
DO MONITORAMENTO, CONTROLE E AUDITORIA
Art. 10. O ambiente WSO2:
I - Registrará logs de todas as ações;
II - Será monitorado 24x7 conforme diretrizes internas;
III - Poderá ser auditado a qualquer momento pela SGI;
IV - Permitirá rastrear toda modificação ou implantação de APIs; e
V - poderá ter acessos suspensos imediatamente em caso de risco.
CAPÍTULO VIII
DAS SANÇÕES
Art. 11. Identificado o mau uso do acesso concedido, o autorizado estará sujeito a:
I - Suspensão imediata do acesso;
II - Responsabilização administrativa;
III - Registro na área de segurança da informação;
IV - Comunicação à chefia imediata;
V - Abertura de procedimento disciplinar; e
VI - Comunicação ao Encarregado pela Proteção de Dados quando envolver dados pessoais.
CAPÍTULO IX
DA VIGÊNCIA E REVOGAÇÃO
Art. 12. O acesso concedido:
I - Vigorará a partir da assinatura do TCR;
II - Permanecerá enquanto durar a necessidade operacional;
III - Será automaticamente revogado ao cessar o motivo; e
IV - Poderá ser revogado a qualquer tempo por risco ou decisão da SGI.
ANEXOS ÀS DIRETRIZES E PROCEDIMENTOS PARA CONTROLE DE ACESSO À FERRAMENTA WSO2
Anexo I - Modelo de Termo de Ciência e Responsabilidade (TCR) para acesso somente leitura à ferramenta WSO2:
Termo de Ciência e Responsabilidade – <nº do Termo>
Autorizado: < identificação do Servidor solicitante >
Autorizador 1: < Responsável pela área gestora da solução de TIC >
Autorizador 2: < Product Owner da solução de TIC, quando não for este o solicitante >
Concedente: Gerência de Planejamento, Desenvolvimento e Segurança de Sistemas (GIDS)
Objeto (Descrição detalhada do acesso a ser concedido):
O presente Termo registra a ciência e responsabilidade do AUTORIZADO quanto ao acesso excepcional, em MODO SOMENTE LEITURA, à ferramenta WSO2 em operação na Anatel, em caráter restrito, controlado e temporário.
Identificação dos documentos que estabelecem as Diretrizes, Restrições e Condições do Acesso a ser concedido.
Todas as diretrizes, restrições e condições de acesso, aplicáveis ao AUTORIZADO e à Área negocial responsável pela solução de TIC estão definidas nas portarias: <Portaria de diretrizes e procedimentos gerais> e <Portaria de diretrizes e procedimentos específicos>.
Data de validade: < data limite de validade do acesso >
Anexo II - Modelo de Termo de Ciência e Responsabilidade (TCR) para acesso de leitura e escrita à ferramenta WSO2:
Termo de Ciência e Responsabilidade – <nº do Termo>
Autorizado: < identificação do Servidor solicitante >
Autorizador 1: < Responsável pela área gestora da solução de TIC >
Autorizador 2: < Product Owner da solução de TIC, quando não for este o solicitante >
Concedente: Gerência de Planejamento, Desenvolvimento e Segurança de Sistemas (GIDS)
Objeto (Descrição detalhada do acesso a ser concedido):
O presente Termo registra a ciência e responsabilidade do AUTORIZADO quanto ao acesso excepcional, em MODO LEITURA e ESCRITA, à ferramenta WSO2 em operação na Anatel, em caráter restrito, controlado e temporário.
Identificação dos documentos que estabelecem as Diretrizes, Restrições e Condições do Acesso a ser concedido.
Todas as diretrizes, restrições e condições de acesso, aplicáveis ao AUTORIZADO e à Área negocial responsável pela solução de TIC estão definidas nas portarias: <Portaria de diretrizes e procedimentos gerais> e <Portaria de diretrizes e procedimentos específicos>.
Data de validade: < data limite de validade do acesso >
