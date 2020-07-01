ANEXO
REQUISITOS TÉCNICOS E OPERACIONAIS DE USO DA FAIXA DE RADIOFREQUÊNCIAS DE 2.300 MHz A 2.400 MHz
1. OBJETIVO
1.1. Estabelecer os requisitos técnicos e operacionais de uso do espectro por estações operando na faixa de 2.300 MHz a 2.400 MHz e em conformidade com o Regulamento sobre Condições de Uso da Faixa de Radiofrequências de 2,3 GHz, aprovado pela Resolução nº 710, de 28 de maio de 2019, associadas ao Serviço Móvel Pessoal – SMP, Serviço de Comunicação Multimídia – SCM, Serviço Telefônico Fixo Comutado – STFC ou Serviço Limitado Privado – SLP.
2. REFERÊNCIAS
2.1. Regulamento sobre Condições de Uso da Faixa de Radiofrequências de 2,3 GHz, aprovado pela Resolução nº 710, de 28 de maio de 2019.
2.2. 3GPP TS 38.101 V16.3.0 (2020-03): User Equipment (UE) radio transmission and reception (Release 16).
2.3. 3GPP TS 38.104 V16.3.0 (2020-03): Base Station (BS) radio transmission and reception (Release 16).
2.4. 3GPP TS 38.141 V16.4.0 (2019-12): Base Station (BS) conformance testing.
2.5. ECC Report 281 (2018-06): Analysis of the suitability of the regulatory technical conditions for 5G MFCN operation in the 3400-3800 MHz band.
3. DEFINIÇÕES
3.1. AAS (do inglês, Active Antenna System): sistema de antenas integradas aos elementos ativos do transceptor (transmissor, receptor).
3.2. ACLR (do inglês, Adjacent Channel Leakage Ratio): mede o desempenho de um transmissor quanto à capacidade de supressão de energia no canal adjacente, é definida como a razão, expressa em dB, entre a potência média no canal de operação e a potência média emitida no canal adjacente.
3.3. EIRP: potência equivalente isotropicamente radiada.
3.4. Emissões espúrias: são emissões causadas por efeitos indesejados do transmissor, como emissão de harmônicos, emissão parasitária, produtos de intermodulação e produtos de conversão de frequência, excluídas as emissões fora de faixa.
3.5. Emissões fora de faixa: são emissões indesejáveis imediatamente fora da largura de faixa do canal, resultantes do processo de modulação e da não linearidade no transmissor, excluídas as emissões espúrias.
3.6. Emissões indesejáveis: consistem em emissões fora de faixa e emissões espúrias.
3.7. OBUE (do inglês, Operating Band Unwanted Emissions): consistem nas emissões indesejáveis compreendidas na faixa de operação do sistema acrescida de um deslocamento de frequências (f_offset) abaixo e acima das extremidades inferior e superior da faixa de operação, respectivamente.
3.8. TRP (do inglês, Total Radiated Power): é definido como a integral da potência transmitida em diferentes direções em toda a esfera de radiação.
4. POTÊNCIA DE OPERAÇÃO
4.1. A potência utilizada deve ser a mínima necessária à realização do serviço com boa qualidade e adequada confiabilidade.
4.2. Estações base, nodal e repetidora devem operar com EIRP máxima de acordo com a Tabela I.
Tabela I – Potência máxima transmitida pela estação base, nodal ou repetidora.
Faixa de frequência
Potência máxima
2.300 - 2.390 MHz
62 dBm/10 MHz EIRP por polarização
2.390 - 2400 MHz
52 dBm/10 MHz EIRP por polarização
4.3. Estações móveis ou terminais devem operar com o EIRP máxima de acordo com a Tabela II e devem implementar controle automático de potência.
Tabela II – Potência máxima transmitida pela estação móvel ou terminal.
Tipo de estação
Potência máxima
Móvel portátil
26 dBm na saída do transmissor
Móvel veicular
40 dBm EIRP
Terminal
40 dBm EIRP
5. EMISSÕES INDESEJÁVEIS
5.1. Emissões fora de faixa:
5.1.1. As emissões fora de faixa são especificadas em termos de ACLR e em termos de OBUE.
5.1.2. Para estação móvel ou terminal operando na faixa de frequências de 2.300 MHz a 2.400 MHz o ACLR deve ser no mínimo de 30 dB.
5.1.3. Para estação base, nodal ou repetidora operando na faixa de frequências de 2.300 MHz a 2.400 MHz o ACLR deve estar de acordo com a Tabela III.
Tabela III – ACLR mínimo para estação base, nodal ou repetidora
Largura de faixa BWCanal [MHz]
Deslocamento da frequência central da portadora transmitida em relação a frequência central do canal adjacente superior ou inferior
Canal Adjacente
Tipo de filtro no canal adjacente e respectiva largura de faixa
ACLR mínimo
5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100
BWCanal
Mesma largura de BWConfig
Filtro Quadrado (BWConfig)
45 dB
2 x BWCanal
Mesma largura de BWConfig
Filtro Quadrado (BWConfig)
45 dB
BWCanal /2 + 2,5 MHz
Largura de BW de 5 MHz
Filtro Quadrado (4,5 MHz)
45 dB
BWCanal /2 + 7,5 MHz
Largura de BW de 5 MHz
Filtro Quadrado (4,5 MHz)
45 dB
onde:
a) BWCanal é a largura de faixa do canal;
b) BWConfig é a configuração da largura de faixa de transmissão (em MHz) no canal de frequência consignado, isto é, BWConfig (em MHz) = NRB (número de resource blocks) x espaçamento de subportadoras x 12; e,
c) BW é a largura de faixa.
5.1.4. Para estação base, nodal ou repetidora com antena não AAS (antena não integrada) as emissões indesejáveis na faixa de frequências 2.290 MHz a 2.410 MHz (OBUE) devem estar de acordo com as Tabela IV.
Tabela IV – Limites de OBUE da estação base, nodal ou repetidora com antena não AAS (antena não integrada)
Deslocamento de frequência a partir das extremidades do bloco (foffset)
Nível máximo de potência
Faixa de resolução para medição
0 MHz ≤ foffset < 5 MHz
-7 dBm -7/5 * (foffset/MHz -0,05) dB
100 kHz
5 MHz ≤ foffset < 10 MHz
-14 dBm
100 kHz
5.1.5. Para estação base, nodal ou repetidora com antena AAS (antena integrada) as emissões indesejáveis na faixa de frequências 2.260 MHz a 2.440 MHz (OBUE) devem estar de acordo com as Tabela V.
Tabela V – Limites de OBUE da estação base, nodal ou repetidora com antena AAS (antena integrada)
Deslocamento de frequência a partir das extremidades do bloco (foffset)
Nível máximo de potência
Faixa de resolução para medição
0 MHz ≤ foffset < 5 MHz
2 dBm -7/5 * (foffset /MHz -0,05) dB
100 kHz
5 MHz ≤ foffset < 10 MHz
-5 dBm
100 kHz
10 MHz ≤ foffset < 40 MHz
-6 dBm
1 MHz
5.2. Emissões espúrias:
5.2.1. Para estações com antena não AAS (antena não integrada) são consideradas espúrias emissões em frequências inferiores a 2.290 MHz e superiores a 2.410 MHz (deslocamento de 10 MHz abaixo e acima das extremidades inferior e superior da faixa de operação, respectivamente).
5.2.2. Para estação base, nodal ou repetidora com antena não AAS (antena não integrada) as emissões espúrias devem ser no máximo de -30 dBm/MHz na faixa de frequências de 1 GHz a 12,75 GHz, exceto na faixa de frequências de 4,5 GHz a 4,8 GHz que devem ser no máximo de -52 dBm/MHz.
5.2.3. Para estações com antena AAS (antena integrada) são consideradas espúrias emissões em frequências inferiores a 2.260 MHz e superiores a 2.440 MHz (deslocamento de 40 MHz abaixo e acima das extremidades inferior e superior da faixa de operação, respectivamente).
5.2.4. Para estação base, nodal ou repetidora com antena AAS (antena integrada) as emissões espúrias devem ser no máximo de -21 dBm/MHz de TRP na faixa de frequências de 1 GHz a 12,75 GHz, exceto na faixa de frequências de 4,5 GHz a 4,8 GHz que devem ser no máximo de -43 dBm/MHz.
5.2.5. Para estação móvel ou terminal as emissões espúrias devem ser no máximo de -30 dBm/MHz na faixa de frequências de 1 GHz a 12,75 GHz.
