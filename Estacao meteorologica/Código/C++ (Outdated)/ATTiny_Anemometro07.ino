#include <Wire.h>
#include <util/delay.h>

//-- Constantes para controle geral
#define TAM_BUFFER          15
#define POS_DIRECAO         9
#define MODO_DEBUG          0

//-- Variáveis para a captura dos sensores ópticos
bool sensor01 = false,
     sensor02 = false,
     sensor03 = false;
uint8_t sensores = 0x00;

bool CW  = false;
bool CCW = false;
bool voltaEmCurso = false;

//-- Variável para contagem de voltas da roda de conchas
int contadorVoltas = 0;
int contadorTempo = 0;

//-- Buffer de envio para dispositivo master - 15 bytes mais terminador \0
char bufTransmissao[TAM_BUFFER] = "000000000000000";

//== Função chamada na ocasião da solicitação pelo master
void requestEvent() {

    //-- Transmite o buffer montado até o momento
    Wire.write(bufTransmissao);

    //-- Após realizado o envio, zera o contador de voltas e o buffer
    contadorVoltas = 0;
    for (int8_t i = 0; i < TAM_BUFFER; i++) bufTransmissao[i] = '0';
}

//-- Interrupção para mudança de estado dos pinos PB.
ISR(PCINT0_vect)
{
    //-- Captura evento de acionamento dos três sensores
    sensor01 = (PINB & (1 << PINB1)) == (1 << PINB1);
    sensor02 = (PINB & (1 << PINB3)) == (1 << PINB3);
    sensor03 = (PINB & (1 << PINB4)) == (1 << PINB4);
    delay(10);

    //-- Sensores estão pulled-up: portanto, precisa invertê-los
    sensores = ((sensor03 << 2) | (sensor02 << 1) | (sensor01 << 0));

    //-- ...e considerar apenas os três bits menos significativos...

    bufTransmissao[0] = sensor01 + 48;
    bufTransmissao[1] = sensor02 + 48;
    bufTransmissao[2] = sensor03 + 48;
    bufTransmissao[3] = sensores + 48;

    //-- conforme configuração de acionamento dos sensores, incrementa
    //   ou decrementa contador de voltas
    switch (sensores)
    {
        case 3:             //-- Roda foi acionada no sentido anti-horário
        {
            if (CW && voltaEmCurso)
            {
                contadorVoltas++;
                voltaEmCurso = false;
            }
            else CCW = true;

            break;
        }
        case 5:             //-- Roda passando pelo sensor central
        {
            voltaEmCurso = true;
            break;
        }
        case 6:             //-- Roda foi acionada no sentido horário
        {
            if (CCW && voltaEmCurso)
            {
                contadorVoltas--;
                voltaEmCurso = false;
            }
            else CW = true;

            break;
        }
        default:
        {
            break;
        }
    }
}

//== Função de montagem do buffer de transmissão para master I2C
int montaBuffer(char bufTransmissao[], uint8_t tamBuffer, int contadorVoltas)
{
    int dividendo = contadorVoltas;
    if (contadorVoltas < 0)
    {
        dividendo = contadorVoltas * -1;
        bufTransmissao[POS_DIRECAO] = 'S';
    }
    else
        bufTransmissao[POS_DIRECAO] = 'N';

    int divisor = 10;
    int8_t resto = 0;
    int8_t i = 0;

    while (1)
    {
        resto = dividendo % divisor;
        dividendo = dividendo / divisor;
        if ((dividendo == 0) && (resto == 0)) break;
        bufTransmissao[tamBuffer-i-1] = 48 + resto;
        i++;
    }
}

//== Programa principal ==========================================
void setup() {
    Wire.begin(0x09);                // Inicializa o dispositivo com o endereço I2C 0x09
    Wire.onRequest(requestEvent);    // Registra o serviço para a solicitação I2C

    //-- Registradores para a interrução nos pinos PB1 e PB4
    GIMSK |= (1 << PCIE);                                   // Habilita interrupção nos pinos PB
    PCMSK |= (1 << PCINT1) | (1 << PCINT3) | (1 << PCINT4); // Configura os pinos PB1, PB3 e PB4 para uma interrupção de mudança de estado
}

//== Loop infinito do programa principal =========================
void loop()
{

    //== Gerador de base de tempo para pisca-pisca de 1Hz ========
    if (TCNT0 >= 0xFA)
    {
        TCNT0 = 0;
        contadorTempo++;
    }

    //-- Monta buffer para envio para dispositivo master I2C
    montaBuffer(bufTransmissao, TAM_BUFFER, contadorVoltas);
}
