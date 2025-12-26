ANEXO
DIRETRIZES E PROCEDIMENTOS PARA CONTROLE DE ACESSO A BANCO DE DADOS DE DESENVOLVIMENTO DE SOLUÇÕES DE TIC
CAPÍTULO I
DO OBJETO
Art. 1º Estabelecer as diretrizes, condições, responsabilidades e limitações relacionadas ao acesso à ferramenta WSO2 em operação na Anatel, com base nos Termos de Ciência e Responsabilidade (TCR) vigentes, contemplando:
I - Acessos somente leitura; e
II - Acessos de leitura e escrita.
Art. 2º A presente portaria formaliza, para fins de governança e segurança da informação, todos os requisitos de uso, obrigações, vedações, responsabilidades, riscos, mecanismos de controle e regras aplicáveis para concessão e manutenção desses acessos.
CAPÍTULO II
DA ABRANGÊNCIA
Art. 3º As disposições desta portaria se aplicam a:
I - Servidores da GIDS/SGI responsáveis por administrar bancos de dados de desenvolvimento;
II - Product Owners (PO) das soluções de TIC legadas;
III - Representantes das áreas negociais, gestoras das soluções de TIC; e
IV - Servidores que, mediante necessidade funcional, requeiram acesso a bancos de dados em ambiente de desenvolvimento.
CAPÍTULO III
DOS RISCOS E CONSEQUÊNCIAS OPERAICONAIS
Art. 4º O acesso inadequado a bancos de dados de soluções legadas pode resultar em:
I - Perda de integridade de dados;
II - Corrupção de tabelas, schemas ou registros;
III - Quebra de compatibilidade entre ambientes;
IV - Exposição de dados pessoais ou sigilosos;
V - Interrupção de serviços devido a inconsistências;
VI - Degradação de performance ou falhas nos sistemas;
VII - Comprometimento da lógica institucional;
VIII - Impacto em SLAs e contratos de serviços; e
IX - Riscos regulatórios e jurídicos relacionados à LGPD.
Parágrafo único. Em virtude das hipóteses previstas no presente artigo, o acesso será sempre excepcional, monitorado e restrito.
CAPÍTULO IV
DOS TIPOS DE ACESSO
Art. 5º São tipos de acesso previstos às bases de dados de desenvolvimento:
I - Acesso Somente Leitura
a) Esse acesso permitirá:
1 - visualizar tabelas, registros e estruturas;
2 - executar consultas SELECT;
3 - analisar modelos de dados;
4 - diagnosticar comportamentos; e
5 - acompanhar logs e estatísticas.
b) Proíbe qualquer forma de escrita, alteração, deleção ou criação.
II - Acesso Leitura e Escrita
a) Esse acesso permitirá:
1 -executar inserts, updates e deletes;
2 - criar ou ajustar estruturas temporárias;
3 - realizar scripts de manutenção pertinentes ao desenvolvimento; e
4 - corrigir inconsistências identificadas em ambiente DEV.
b) Para soluções legadas, é permitido somente em caráter excepcional, com:
1 - justificativa funcional explícita;
2 - autorização do PO da solução;
3 - autorização da chefia da área gestora;
4 - avaliação técnica da GIDS; e
5 - registro formal e monitoramento contínuo.
Art. 6º Todo acesso será:
I - Excepcional;
II - Individual e intransferível;
III - Temporário;
IV - Concedido apenas com necessidade funcional comprovada;
V - Revogável a qualquer tempo;
VI - Condicionado ao perfil adequado; e
VII - Monitorado com logs permanentes.
CAPÍTULO V
DAS RESTRIÇÕES E VEDAÇÕES
Art. 7º Independentemente do tipo de acesso, é vedado:
I - Alterar dados sensíveis ou estratégicos sem autorização;
II - Modificar estruturas críticas sem revisão técnica;
III - Executar scripts não validados;
IV - Promover engenharia reversa para fins indevidos;
V - Copiar bases integrais para ambientes não autorizados;
VI - Expor dados pessoais ou sigilosos;
VII - Compartilhar credenciais;
VIII - Promover ações que comprometam integridade ou disponibilidade; e
IX - Replicar estruturas sem autorização da GIDS.
CAPÍTULO VI
DAS RESPONSABILIDADES
Art. 8º O autorizado deverá:
I - Atuar apenas no escopo concedido;
II - Proteger credenciais e dados acessados;
III - Registrar e documentar alterações quando aplicável;
IV - Respeitar a LGPD, POSIN e normas de desenvolvimento;
V - Comunicar incidentes imediatos;
VI - Submeter-se à rastreabilidade integral do acesso; e
VII - Responder individualmente por ações realizadas sob seu usuário.
Art. 9º Ao representante da área gestora da solução de TIC compete:
I - Validar e justificar o acesso solicitado;
II - Autorizar formalmente o uso;
III - Garantir que o acesso está alinhado às necessidades funcionais;
IV - Comunicar à GIDS mudanças de vínculo ou necessidade de revogação; e
V - Supervisionar o uso dos acessos concedidos.
Art. 10. O PO da solução deverá:
I - Validar a necessidade técnica do acesso;
II - Acompanhar riscos associados às manipulações;
III - Garantir aderência funcional às alterações permitidas.
CAPÍTULO VII
DO MONITORAMENTO, CONTROLE E AUDITORIA
Art. 11. O acesso será:
I - Monitorado por logs internos;
II - Auditável pela SGI e pelas áreas de segurança;
III - Registrado em sistema de controle de acessos;
IV - Acompanhado pela equipe técnica da GIDS; e
V - Suspenso a qualquer tempo em caso de risco.
CAPÍTULO VIII
DAS SANÇÕES
Art. 12. Identificado o uso indevido do acesso concedido, o autorizado estará sujeito a:
I - Suspensão imediata do acesso;
II - Responsabilização administrativa;
III - Registro na área de segurança da informação;
IV - Comunicação à chefia imediata;
V - Abertura de procedimento disciplinar; e
VI - Comunicação ao Encarregado pela Proteção de Dados quando envolver dados pessoais.
CAPÍTULO IX
DA VIGÊNCIA E REVOGAÇÃO
Art. 13. O acesso concedido:
I - Vigorará a partir da autorização registrada;
II - Permanecerá válido enquanto durar a necessidade funcional;
III - Será automaticamente revogado ao cessar o motivo;
IV - Poderá ser revogado sem aviso, por risco ou decisão da SGI; e
V - Deverá ser revalidado periodicamente.
ANEXOS ÀS DIRETRIZES E PROCEDIMENTOS PARA CONTROLE DE ACESSO À FERRAMENTA WSO2
Anexo I - Modelo de Termo de Ciência e Responsabilidade (TCR) para acesso somente leitura a Banco de Dados de Desenvolvimento:
Termo de Ciência e Responsabilidade – <nº do Termo>
Autorizado: < identificação do Servidor solicitante >
Autorizador 1: < Responsável pela área gestora da solução de TIC >
Autorizador 2: < Product Owner da solução de TIC, quando não for este o solicitante >
Concedente: Gerência de Planejamento, Desenvolvimento e Segurança de Sistemas (GIDS)
Objeto (Descrição detalhada do acesso a ser concedido):
O presente Termo registra a ciência e responsabilidade do AUTORIZADO quanto ao acesso excepcional, em MODO SOMENTE LEITURA, a Banco de Dados de desenvolvimento na Anatel, denominada <NOME DA BASE>, em caráter restrito, controlado e temporário.
Identificação dos documentos que estabelecem as Diretrizes, Restrições e Condições do Acesso a ser concedido.
Todas as diretrizes, restrições e condições de acesso, aplicáveis ao AUTORIZADO e à Área negocial responsável pela solução de TIC estão definidas nas portarias: <Portaria de diretrizes e procedimentos gerais> e <Portaria de diretrizes e procedimentos específicos>.
Data de validade: < data limite de validade do acesso >
Anexo II - Modelo de Termo de Ciência e Responsabilidade (TCR) para acesso leitura e escrita a Banco de Dados de Desenvolvimento:
Termo de Ciência e Responsabilidade – <nº do Termo>
Autorizado: < identificação do Servidor solicitante >
Autorizador 1: < Responsável pela área gestora da solução de TIC >
Autorizador 2: < Product Owner da solução de TIC, quando não for este o solicitante >
Concedente: Gerência de Planejamento, Desenvolvimento e Segurança de Sistemas (GIDS)
Objeto (Descrição detalhada do acesso a ser concedido):
O presente Termo registra a ciência e responsabilidade do AUTORIZADO quanto ao acesso excepcional, em MODO LEITURA e ESCRITA, a Banco de Dados de desenvolvimento na Anatel, denominada <NOME DA BASE>, em caráter restrito, controlado e temporário.
Identificação dos documentos que estabelecem as Diretrizes, Restrições e Condições do Acesso a ser concedido.
Todas as diretrizes, restrições e condições de acesso, aplicáveis ao AUTORIZADO e à Área negocial responsável pela solução de TIC estão definidas nas portarias: <Portaria de diretrizes e procedimentos gerais> e <Portaria de diretrizes e procedimentos específicos>.
Data de validade: < data limite de validade do acesso >
