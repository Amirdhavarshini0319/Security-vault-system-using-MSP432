
#include "msp.h"
void UART0_init(void); 
void delayms(int n);
#define LED_PIN BIT0
void configureSevenSegment();
void displayNumber(int num);

unsigned char c[4];
unsigned char new[10]="\n\r";
unsigned char space[9]="  ";
unsigned char star[9]="*";
unsigned char tryy[66]="Attempts Failed Try again after 30 sec\n\r\t    ";
unsigned char tt[20]="TRY NOW\n\r\t    ";
unsigned char warning[50]="\n\rSYSTEM LOCKED";
unsigned char start[20]="\n\rEnter password : ";
unsigned char open[20]="\n\rVault open";
unsigned char lock[20]="\n\rStill locked\n\r";
unsigned char att[33]="\n\rYou Have 3 Attempts\n\r\t    ";
void configureServoMotor();
#define SERVO_CONTROL_PIN BIT4
void servoRotateClockwise();
unsigned char p[4];
int i,j=0;
int f=0;
int angle;

void delay_ms(uint32_t ms) {
    uint32_t i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 3000; j++) { 
        }
    }
}
void setup_pwm() {
    P2->SEL0 |= 0x10; 
    P2->SEL1 &= ~0x10;
    P2->DIR |= 0x10;

    TIMER_A0->CCR[0] = 30000 - 1; 
    TIMER_A0->CCTL[1] = 0xE0;
    TIMER_A0->CCR[1] = 1500; 

    TIMER_A0->CTL = TIMER_A_CTL_SSEL__SMCLK | 
                    TIMER_A_CTL_MC__UP | 
                    TIMER_A_CTL_CLR; 
}

void set_servo_position(uint32_t position) {
    int duty_cycle = 1500 +
                          ((position * (6000 - 1500)) / 180);

    TIMER_A0->CCR[1] = duty_cycle;
}


int main (void)
{
	UART0_init (); 
	
	

  setup_pwm();
	set_servo_position(0);
	
	P2->SEL1 &= ~3; 
	P2->SEL0 &= ~3;
	P2->DIR |= 3;
	
	P4->SEL1 &= ~0XFF; 
	P4->SEL0 &= ~0XFF;
	P4->DIR |= 0XFF;
	P4->OUT = 0X39;
	for (i=0;i<17;i++)
	{
		while (!(EUSCI_A0-> IFG & 0x02)) { } 
		EUSCI_A0 -> TXBUF=start[i];
	}
	for (i=0;i<4;i++)
	{
		while (!(EUSCI_A0-> IFG & 0x01)) { } 
	  p[i] = EUSCI_A0 -> RXBUF;
		while (!(EUSCI_A0-> IFG & 0x02)) { } 
		EUSCI_A0 -> TXBUF=star[0];
		
	}
	for (i=0;i<33;i++)
	{
		while (!(EUSCI_A0-> IFG & 0x02)) { } 
		EUSCI_A0 -> TXBUF=att[i];
	}
	while (j<6)
	{
		f=0;
		P4->OUT = 0X39;
		for (i=0;i<4;i++)
		{
			while (!(EUSCI_A0-> IFG & 0x01)) { }
			c[i] = EUSCI_A0 -> RXBUF;
			while (!(EUSCI_A0-> IFG & 0x02)) { } 
			EUSCI_A0 -> TXBUF=c[i];
			
		}
		for (i=0;i<2;i++)
		{
			while (!(EUSCI_A0-> IFG & 0x02)) { } 
			EUSCI_A0 -> TXBUF=space[i];
		}
		 
		for (i=0;i<4;i++)
		{
			if (c[i]==p[i])
			{
				f+=1;
			}
		}
		
		if (f == 4)
		{
			P2->OUT=0;
			P2->OUT = 2; 
			P4->OUT = 0X3F;	
			for ( angle = 0; angle <= 360; angle += 180) 
			{
				set_servo_position(angle);
				delay_ms(100);
			}		
			for (i=0;i<12;i++)
			{
				while (!(EUSCI_A0-> IFG & 0x02)) { } 
				EUSCI_A0 -> TXBUF=open[i];
			}
			Break;
		}
	  if (f != 4) 
		{
			P2->OUT=0;
			P2->OUT = 1; 
			P4->OUT = 0X39;
			for (i=0;i<15;i++)
			{
				while (!(EUSCI_A0-> IFG & 0x02)) { } 
				EUSCI_A0 -> TXBUF=lock[i];
			}
		}
		if (j==2)
		{
			for (i=0;i<48;i++)
			{
				while (!(EUSCI_A0-> IFG & 0x02)) { } 
				EUSCI_A0 -> TXBUF=tryy[i];
			}
			delayms(30000);
			for (i=0;i<17;i++)
			{
				while (!(EUSCI_A0-> IFG & 0x02)) { } 
				EUSCI_A0 -> TXBUF=tt[i];
			}
		}
		if (j==5)
		{
			for (i=0;i<35;i++)
			{
				while (!(EUSCI_A0-> IFG & 0x02)) { } 
				EUSCI_A0 -> TXBUF=warning[i];
			}
			for (i=0;i<20;i++)
			{
				P4->OUT = 0x38;
				delayms(1000);
				P4->OUT = 0x00;
				delayms(1000);
			}
		}		
		j++;
	}
}
void delayms(int n)
{
	int k,l;
	for (k=0;k<n;k++)
	{
		for (l=750;l>0;l--);
	}
}
void UART0_init(void)
{
	EUSCI_A0 -> CTLW0 |= 1; 
	EUSCI_A0 -> MCTLW = 0; 
	EUSCI_A0 -> CTLW0 = 0x0081; 
	EUSCI_A0 -> BRW = 26; 
	P1 -> SEL0 |= 0x0C; 
	P1 -> SEL1 &=~ 0x0C;
	EUSCI_A0 -> CTLW0 &= ~1; 
}

