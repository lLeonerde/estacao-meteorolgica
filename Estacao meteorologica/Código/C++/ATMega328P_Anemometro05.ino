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
uint8_t sensoresAnterior = 0x00;
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
ISR(PCINT2_vect)
{
    //-- Captura evento de acionamento dos três sensores
    delay(10);

    //-- Consideramos apenas PD4, PD5 e PD6
    sensores = PIND & 0b01110000;

    //-- Passamos estes bits para os menos significativos para melhor tratá-los
    sensores = sensores >> 4;
    Serial.println(sensores);

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
    
    Serial.print("Contagem de voltas: ");
    Serial.println(contadorVoltas);
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
    Serial.begin(57600);

    DDRD &= ~(1<< DDD4);  //-- PD4 - Sensor da porta 01 (pino 04)
    DDRD &= ~(1<< DDD5);  //-- PD5 - Sensor da porta 02 (pino 05)
    DDRD &= ~(1<< DDD6);  //-- PD6 - Sensor da porta 03 (pino 06)

    //-- Registradores para a interrução nos pinos PB1 e PB4
    PCICR |= (1 << PCIE2);
    PCMSK2 |= (1 << PCINT18 | 1 << PCINT19 | 1 << PCINT20 | 1 << PCINT21 | 1 << PCINT22 | 1 << PCINT23);
    SREG |= (1 << SREG_I);
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
