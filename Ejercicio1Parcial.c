#include <stdio.h>  //Agrego librerias de entrada/salida

int main(void)  //Programa Principal
{
    int ContadorCamiones=0,ContadorValor=0; //Declaro los contadores y los inicializo, seran de tipo ENTERO.
    float distancia,consumo,mayordistancia,PromConsumo,porcentaje,valor,sumaconsumo; //Declaro variables de tipo flotante para calcular lo demas.

    printf("Ingrese el VALOR de CONSUMO que desee para luego calcular el porcentaje:  \n\n ");  //Pido que ingrese el valor por teclado
    scanf("%f", &valor);    //Guardo lo ingresado en la variable "valor".

    do  // HACER todo lo que esta entre llaves
    {
        printf("Ingrese la distancia del camion %d \n\n", ContadorCamiones); //Pido que ingrese distancia
        scanf("%f", &distancia);    //Guardo distancia en la variable "distancia".
        printf("Ingrese el consumo del camion %d \n\n", ContadorCamiones);  //Pido que ingrese consumo
        scanf("%f", &consumo);  //Guardo consumo en la variable "consumo".

        ContadorCamiones++;     //Cada vez que ingreso un camion nuevo agrego +1 al contador.(Cuento camiones)

        sumaconsumo=sumaconsumo+consumo;    //Sumo el total del consumo en la variable "sumaconsumo".

        if(distancia>mayordistancia)    //SI "distancia" es mayor que "mayordistancia"
        {
            mayordistancia=distancia; //Guardo el valor de "distancia" en "mayordistancia"
        }                              //Cierro IF

        if(consumo >= valor)    //SI "consumo" es mayor igual a "Valor".
        {
            ContadorValor++;    //Incremento +1 a la variable "ContadorValor" (Esto lo uso para luego calcular porcentaje).
        }                               //Cierro IF


    }
    while(distancia>0); //Ejecutar continuamente todo lo del DO de arriba MIENTRAS QUE distancia sea mayor a 0.

    PromConsumo=sumaconsumo/ContadorCamiones; // Calculo promedio del consumo y lo guardo en PromConsumo (Promedio=SumaDeTodosLosConsumos DIVIDIDO CantTotalDeCamiones).

    porcentaje=ContadorValor*ContadorCamiones/100; // Calculo el porcentaje y lo guardo en "porcentaje" (Porcentaje=CantDeCamionesQueSuperaronElValor X CantTotalDeCamiones SOBRE 100)


    printf("La mayor distancia recorrida fue:  %f \n\n",mayordistancia); //Muestro la mayor distancia recorrida.
    printf("El primedio del consumo es: %f \n\n",PromConsumo);  //Muestro el promedio del consumo
    printf("El porcentaje de camiones que consumieron mas de %f es: %f ",valor,porcentaje); //Muestro el porcentaje.

    return 0;
}