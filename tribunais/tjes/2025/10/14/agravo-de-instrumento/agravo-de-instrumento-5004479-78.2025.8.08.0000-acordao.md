ESTADO DO ESPÍRITO SANTO
PODER JUDICIÁRIO

PROCESSO Nº 5004479-78.2025.8.08.0000

AGRAVO DE INSTRUMENTO (202)

AGRAVANTE: VIASAT BRASIL SERVICOS DE COMUNICACOES LTDA

AGRAVADO: ALESSANDRA BASSO

RELATOR(A):
ARTHUR JOSE NEIVA DE ALMEIDA

______________________________________________________________________________________________________________________________________________

EMENTA

DIREITO CIVIL E PROCESSUAL CIVIL. AGRAVO DE INSTRUMENTO. RESPONSABILIDADE DE PROVEDOR DE CONEXÃO. FORNECIMENTO DE DADOS DE USUÁRIO. ALEGADA IMPOSSIBILIDADE TÉCNICA QUE ENCONTRA RESPALDO JURISPRUDENCIAL. RECURSO PROVIDO.

I. CASO EM EXAME

Agravo de Instrumento interposto por Viasat Brasil Serviços de Comunicações Ltda contra decisão que deferiu, em sede de tutela de urgência, pedido para que a empresa agravante fornecesse dados de usuários supostamente envolvidos na criação de perfis falsos em rede social, os quais teriam utilizado imagem da autora para ofender terceiros. A decisão recorrida reconheceu a presença dos requisitos do art. 300 do CPC e determinou, sob pena de multa, a disponibilização de dados como nome, CPF, RG, endereço, registros eletrônicos e logs de conexão. A agravante alegou impossibilidade técnica de cumprimento da ordem judicial, em razão da ausência da porta lógica de origem dos IPs fornecidos pela plataforma, elemento indispensável para identificação precisa dos usuários, dada a tecnologia NAT utilizada.

II. QUESTÃO EM DISCUSSÃO

A questão em discussão consiste em verificar se é possível impor à empresa agravante, na qualidade de provedora de conexão, a obrigação de fornecer dados pessoais e registros eletrônicos de usuários sem que tenha sido disponibilizada a porta lógica de origem, indispensável para a identificação precisa dos responsáveis, em razão da utilização da tecnologia NAT.

III. RAZÕES DE DECIDIR

A tecnologia NAT (Network Address Translation), utilizada por provedores de conexão, permite o compartilhamento de um mesmo IP público por múltiplos usuários, de modo que a identificação precisa depende da disponibilização da porta lógica de origem, além do IP, data e horário.

O Marco Civil da Internet (Lei nº 12.965/2014) impõe aos provedores de conexão apenas a guarda de registros de conexão (IP, data e hora), sendo vedada a retenção de dados de acesso a aplicações de internet, o que limita sua capacidade de identificar usuários sem colaboração dos provedores de aplicação.

O STJ, no julgamento do REsp nº 1.784.156/SP, reconheceu a existência de limitações técnicas relevantes à identificação de usuários com base apenas no IP, notadamente em contextos de uso de NAT, exigindo a presença da porta lógica de origem como elemento essencial.

O fornecimento de dados de usuários em tais condições, sem elementos técnicos suficientes, implica risco de responsabilização indevida e descumprimento de normas legais sobre proteção de dados e privacidade, razão pela qual se justifica a reforma da decisão que deferiu a tutela de urgência exclusivamente quanto à agravante.

IV. DISPOSITIVO E TESE

Recurso provido.

Tese de julgamento
:

A imposição judicial de fornecimento de dados de usuários a provedores de conexão é incabível quando não demonstrada a viabilidade técnica da medida, especialmente diante da ausência de porta lógica de origem em casos de utilização de tecnologia NAT.

O Marco Civil da Internet limita a obrigação de guarda de registros dos provedores de conexão aos dados de conexão (IP, data e horário), não abrangendo registros de acesso a aplicações.

A identificação precisa de usuários em redes com IPs compartilhados exige colaboração dos provedores de aplicação, sob pena de inviabilizar o cumprimento da ordem judicial.

Dispositivos relevantes citados
: Lei nº 12.965/2014 (Marco Civil da Internet), arts. 10, 13 e 14; CPC, art. 300.

Jurisprudência relevante citada
: STJ, REsp nº 1.784.156/SP, Rel. Min. Marco Aurélio Bellizze, 3ª Turma, DJe 21.11.2019.

______________________________________________________________________________________________________________________________________________
ACÓRDÃO

Decisão
: À unanimidade, conhecer e dar provimento ao recurso, nos termos do voto do Relator.

Órgão julgador vencedor
: Gabinete Des. ARTHUR JOSÉ NEIVA DE ALMEIDA

Composição de julgamento: Gabinete Des. ARTHUR JOSÉ NEIVA DE ALMEIDA - ARTHUR JOSE NEIVA DE ALMEIDA - Relator / Gabinete Desª. ELIANA JUNQUEIRA MUNHOS FERREIRA - ELIANA JUNQUEIRA MUNHOS FERREIRA - Vogal / Gabinete Des. ROBSON LUIZ ALBANEZ - ROBSON LUIZ ALBANEZ - Vogal
VOTOS VOGAIS
Gabinete Desª. ELIANA JUNQUEIRA MUNHOS FERREIRA - ELIANA JUNQUEIRA MUNHOS FERREIRA (Vogal)
Acompanhar
Gabinete Des. ROBSON LUIZ ALBANEZ - ROBSON LUIZ ALBANEZ (Vogal)
Acompanhar

______________________________________________________________________________________________________________________________________________

RELATÓRIO

_______________________________________________________________________________________________________________________________________________

NOTAS TAQUIGRÁFICAS

________________________________________________________________________________________________________________________________________________
VOTO VENCEDOR

QUARTA CÂMARA CÍVEL

AGRAVO DE INSTRUMENTO N.º 5004479-78.2025.8.08.0000

AGRAVANTE: VIASAT BRASIL SERVIÇOS DE COMUNICAÇÕES LTDA

AGRAVADA: ALESSANDRA BASSO

RELATOR: DESEMBARGADOR ARTHUR JOSÉ NEIVA DE ALMEIDA

V O T O

Eminentes Pares, Viasat Brasil Serviços de Comunicações Ltda interpôs Agravo de Instrumento em face da Decisão inserida no id 64027801 do processo originário (n.º 5006904-06.2025.8.08.0024), na qual o MM. Juiz
a quo
assim expôs os fatos que deram origem à demanda e as razões pelas quais concedeu a medida liminar requerida na petição inicial:

“Trata-se de ação obrigação de fazer com pedido de tutela de urgência proposta por Alessandra Basso em face de Maranet Telecom LTDA, Viasat Brasil Serviços de Comunicações LTDA, Nort Telecom LTDA e Tim SA, visando, sobretudo, o fornecimento de informações.

Na petição inicial (Id 63872548) a autora alegou que tomou conhecimento, em março de 2024, de que duas contas anônimas estavam utilizando sua imagem para ofender outras pessoas. A imagem original havia sido publicada por sua namorada em julho de 2023, o que indica que o responsável pode ser alguém próximo a ela. Diante da situação, a autora ingressou com uma ação contra o Twitter, que forneceu os endereços de IP e um número de telefone associado aos perfis falsos. A partir dessas informações, foi constatado que os serviços de conexão utilizados pertenciam às empresas rés, o que levou ao ajuizamento da presente ação.

(...).

A probabilidade do direito da autora é incontroversa, pois, conforme as imagens das respectivas contas (ID 63873469 e 63873470), é escudado em indícios suficientes o uso indevido de sua imagem para atacar terceiros, fato que pode vir a difamar seu nome e prejudicar sua reputação.

(...).

Na linha dos entendimentos supracitados, ao compulsar os autos, verifico que a parte autora cumpriu a exigência solicitada para a obtenção da tutela, tendo realizado a juntada dos IPs das contas para as quais se requer o fornecimento de dados.

(...).

Ante o exposto, preenchidos os requisitos do artigo 300 do CPC, DEFIRO o pedido de tutela de urgência para determinar que as empresas rés Maranet Telecom LTDA, Viasat Brasil Serviços de Comunicações LTDA, Nort Telecom LTDA, no prazo de 15 (quinze) dias e sob pena de multa diária de R$ 500,00 até o limite de R$ 15.000,00 (quinze mil reais) [sem prejuízo da adoção de outras medidas sub-rogatórias e coercitivas que vierem a se revelar necessárias ao cumprimento das ordens ora expedidas], forneçam:

i) os dados completos (nome, RG, CPF, endereço, telefone e demais registros eletrônicos) do(s) usuário(s), assim, como o(s) número(s) do(s) terminal(is) telefônico(s) por meio do(s) qual(is) ocorreu o acesso aos seus serviços;

ii) demais registros de logs (n. ºs IP, datas e horários) do(s) responsável(is) pelos acessos supra, identificado(s) no item “a.1”, no caso de eventuais IPs dinâmicos;

E, sob idêntica cominação e em igual prazo:

iii) abstenham-se de comunicar o(s) usuário(s) identificado(s) acerca dos presentes requerimentos e dos termos desta demanda, impedindo a destruição de provas pelo(s) mesmo(s)

No caso da ré Tim SA, determino que, no prazo de no prazo de 15 (quinze) dias e sob pena de multa diária de R$ 500,00 até o limite de R$ 15.000,00 (quinze mil reais) [sem prejuízo da adoção de outras medidas sub-rogatórias e coercitivas que vierem a se revelar necessárias ao cumprimento das ordens ora expedidas], forneça:

i) os dados completos (nome, RG, CPF, endereço, telefone e demais registros eletrônicos) do(s) usuário(s), assim, como o(s) número(s) do(s) terminal(is) telefônico(s) por meio do(s) qual(is) ocorreu o acesso aos seus serviços;

E, sob idêntica cominação e em igual prazo:

ii) abstenha-se de comunicar o(s) usuário(s) identificado(s) acerca dos presentes requerimentos e dos termos desta demanda, impedindo a destruição de provas pelo(s) mesmo(s).”

A ora Agravante defende, nas razões de seu recurso (id 12852941), que a Decisão recorrida deve ser reformada porque, em síntese, há impossibilidade técnica de cumprimento da medida, já que os IPs fornecidos pela rede social não vêm acompanhados da porta lógica de origem, elemento necessário para identificar os usuários em razão da tecnologia NAT (
Network Address Translation
) utilizada.

Argumenta, ainda, que como provedora de conexão, armazena dados técnicos no exterior e depende da cooperação dos provedores de aplicação (a exemplo do X [antigo Twitter], Facebook e Whatsapp) para que se completem as informações necessárias à identificação dos usuários.

O recurso em exame, insta salientar, foi recebido com efeito suspensivo, porquanto o Desembargador substituto Luiz Guilherme Risso assim entendeu na Decisão inserida no id 13230773:

“O
fumus boni iuris
parece residir na plausibilidade da alegação de impossibilidade técnica para o cumprimento da ordem judicial nos moldes estabelecidos. A Agravante apresenta argumentação técnica consistente, ainda que a ser oportunamente comprovada e debatida sob o crivo do contraditório, no sentido de que a identificação unívoca de um usuário que acessa a internet por meio de sua rede, especialmente utilizando tecnologia satelital e compartilhamento de IPs via NAT, depende intrinsecamente do fornecimento, pelo provedor de aplicação (no caso, a rede social X/Twitter, que forneceu os dados iniciais à Agravada em outro processo), não apenas do endereço IP, data e horário, mas também da respectiva porta lógica de origem da conexão.

A Agravante sustenta que, sem essa informação crucial, a qual não consta dos dados que lhe foram repassados para cumprimento da ordem, torna-se tecnicamente inviável correlacionar o acesso específico, dentro de um bloco de IPs compartilhados, a um determinado usuário cadastrado em seus sistemas.

A complexidade técnica envolvida na rastreabilidade de conexões em ambientes de IP compartilhado, como o NAT, mostra-se relevante no campo da tecnologia da informação, e a exigência da porta lógica de origem para a desambiguação é frequentemente apontada como necessária por especialistas e órgãos reguladores, conforme mencionado pela Agravante.

Dessa forma, a alegação de que a ordem judicial, ao não considerar essa especificidade técnica e exigir o fornecimento de dados com base apenas no bloco de IPs, data e horário genéricos, impõe uma obrigação de cumprimento tecnicamente inviável, apresenta, a priori, verossimilhança suficiente para caracterizar a probabilidade de provimento do recurso neste ponto específico.”

Em cognição exauriente e a partir da análise dos autos, das normas legais aplicáveis e, ainda, da jurisprudência em casos análogos, a conclusão,
data maxima venia
e a despeito das relevantes alegações contidas nas contrarrazões (id 13746708), é pelo provimento do recurso.

Isso porque, como decorrência dos princípios do Marco Civil da Internet (Lei n.º 12.965/14), a proteção aos registros, dados pessoais e comunicações privadas “
foi disciplinada de modo a restringir sua guarda por provedores de conexão e de acesso a aplicações
”.

E como resultado da “
ponderação de interesses legítimos conflitantes, também se assegurou o acesso aos dados necessários à identificação de autores de crimes ou causadores de danos civis, obrigando-se, pela via judicial, os provedores à eventual disponibilização dos dados por eles guardados
”.

A obrigação de guarda, por sua vez, foi repartida entre os provedores de conexão (caso da Agravante) e os provedores de aplicação. Contudo, “
a preocupação constante com o respeito à privacidade no ambiente virtual, vedou-se a guarda dos dados de acessos a aplicações aos provedores de conexão
”. Em outros termos:

“(...) aos provedores de conexão somente cabe a guarda dos dados de conexão (IP, data e horário), tornando impossível, apenas com esses dados, se conhecer a atividade completa do internauta, enquanto efetivamente conectado à rede mundial (art. 14 da Lei n. 10.965/2014). (...).”

Esta fundamentação ora externada - e mencionada entre parênteses no voto escrito -,
data venia
. é extraída da orientação do colendo Superior Tribunal de Justiça (STJ), que, no julgamento do REsp n.º 1.784.156/SP (Relator Ministro Marco Aurélio Bellizze, Terceira Turma, DJe de 21.11.2019), também destacou, como defende a Agravante, questões técnicas que podem dificultar o cumprimento de ordens judiciais como aquela proferida na demanda originária.

Aliás, no referido julgado do STJ, em voto-vista proferido pela Ministra Nancy Andrighi, também foi lembrada, em certas ocasiões, a dificuldade técnica de identificação de usuários no sistema de Tradução de Endereço de Rede (Network Address Translation - NAT, alegadamente utilizado pela Agravante), inclusive com a seguinte citação doutrinária:

“Ocorre que os endereços IP, cuja função nas investigações sempre se prestou à identificação da localização do terminal de onde partiu a conexão, não mais poderão ser considerados como fonte segura para fins de identificação de autoria. Todos que se conectam à internet recebem necessariamente um endereço IP, único para determinada data e horário. Também durante a navegação na internet, o número do IP é registrado por provedores de aplicações. No entanto, os endereços IP que historicamente foram concebidos para uso individual, enfrentam hoje um cenário de esgotamento, de modo que vêm sendo compartilhados entre pessoas ou organizações distintas, de forma simultânea. Esta realidade já se faz presente hoje também em redes compartilhadas dentro de empresas ou condomínios, com estabelecimento de um IP e NAT, ou ainda, em redes abertas de wi-fi. Assim, enquanto o sistema estiver calcado no atual protocolo de internet chamado IPV4 e não houver a substituição pela versão IPV6, continuará a ocorrer o compartilhamento de IP e, por conseguinte, a impossibilidade de identificação de autorias com base em tal informação.” (BRAUN, Caroline; MARTINS, Rafael D'Enrrico; ARTESE, Gustavo (coord.). O Marco Civil da Internet, a guarda e fornecimento de registros por provedores de conexão e de acesso a aplicações de internet. São Paulo: Quartier Latin, 2015, p. 132).

Toda essa dificuldade apontada pela Agravante e, em tese, asseverada por entendimento já externado pelo STJ, indica, ao menos, a complexidade da questão controvertida e, por isso mesmo, um maior aprofundamento do tema antes de se determinar o cumprimento de ordem judicial que pode, ao fim e ao cabo, ser impossível de ser cumprida.

Destarte, minha conclusão é pelo provimento do recurso porque,
data venia
, ainda não há nos autos elementos seguros e precisos para imputar à Agravante a responsabilidade, sem eventual auxílio dos provedores de aplicação, de fornecer os dados solicitados pela Agravada na petição inicial; em suma, não é possível vislumbrar que a Agravada cumpriu os requisitos do art. 300 do Còdigo de Processo Civil para fins de obter a liminar concedida na Decisão recorrida.

Do exposto, dou provimento ao recurso para reformar, em parte, a Decisão recorrida de modo a indeferir o pedido liminar deduzido na petição inicial
exclusivamente em relação à Agravante
.

É como voto.

_________________________________________________________________________________________________________________________________
VOTOS ESCRITOS

(EXCETO VOTO VENCEDOR)

Acompanho o judicioso voto de relatoria.
