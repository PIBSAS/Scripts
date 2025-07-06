//---------------------------------------------------------------------------
// Se dispone de un archivo que contiene los datos de los alumnos de un
// instituto.
// El archivo se denomina “alumnos.dat”, es de tipo binario y contiene los
// siguientes datos: Nombre (char[20]), Apellido(char [20]), Legajo (long),
// Cantidad de materias aprobadas (int) y Promedio general (flota).
// Se desea realizar un programa que permita Ingresar nuevos alumnos, modificar
// el promedio general cada vez que apruebe una materia, eliminar los alumnos
// que aprobaron todas las materias (40).
// Se deberá bajar el contenido del archivo a una lista ordenada por promedio.
// Cuando se agregue un alumno su promedio será cero y la cantidad de materias
// aprobadas cero.
// Cuando un alumno haya aprobado la última materia se deberá eliminar los datos
// de este alumno de la lista y guardarlo en el archivo “graduado.dat” en el que
// se guardaran los datos del alumno y su promedio general.
// Al finalizar el procesamiento de los datos se deberá realizar un listado de
// los alumnos en el que figure nombre, apellido y promedio general ordenado por
// promedio, al finalizar este se tiene que guardar en el archivo “alumnos.dat”
// todos los datos de la lista, eliminando cada uno de los nodos de esta.
//---------------------------------------------------------------------------
#include <stdio.h>
#include <stdlib.h>
//---------------------------------------------------------------------------
struct Alumnos
{
    char Nombre[20],Apellido[20];
    long Legajo;
    int CantMat;
    float Prom;
};
//---------------------------------------------------------------------------
struct Nodo
{
    struct Alumnos Dato;
    struct Nodo *Sig;
};
//---------------------------------------------------------------------------
struct Pun
{
    struct Nodo *Ant,*Act,*Nvo;
};
//---------------------------------------------------------------------------
void LeerArchivo(struct Nodo **Pri);
void Insertar(struct Nodo *Nvo,struct Nodo **Pri);
void AgreAlum(struct Nodo **Pri);
void AGREGALULI(struct Alumnos Al,struct Nodo **Pri);
void MODIFPRAL(struct Nodo **Pri);
struct Pun BuscaNodo(long Leg,struct Nodo **Pri);
void AGREGOARCHEGRE();
char Menu(void);
//---------------------------------------------------------------------------
int main()
{
    struct Nodo *INI=NULL;
    printf("Menu\n");
    //opciones//
    //ingreso opcion con scanf//
    switch(opcion)
    {
        case '1':
        LeerArchivo();
        break;
        //aca van los otros casos//
    }
}
//---------------------------------------------------------------------------
void LeerArchivo(struct Nodo **Pri)
{
    FILE *fp;
    struct Nodo *Nvo;
    fp=fopen("alumnos.dat","rb");//porq es binario//
    if(!fp)//chequeo el archivo//
    {
        printf("NO ABRO");
        exit(1);
    }
    while(!feof(fp))//leo hasta el fin de archivo//
    {
        if(Nvo=malloc(sizeof(struct Nodo)))//le pido memoria al SO(el nodo)//
        {
            printf("NO MEMORY");//aviso de NO MEMORIA, luego cierro el archivo//
            fclose(fp);
            return;
        }
        fread(&Nvo->Dato,sizeof(struct Alumnos),1,fp);//leo el dato del archivo y lleno el nodo//
        Insertar(Nvo,Pri);//inserto el nodo en la lista(Pri es la direccion de inicio)//
    }
    fclose(fp);//leyo todos los datos, cierro el programa//
}
//---------------------------------------------------------------------------
void Insertar(struct Nodo *Nvo,struct Nodo **Pri)//RECIBE EL NODO QE CREE Y EL INICIO A LA LISTA//
{
    struct Nodo *Act=*Pri,*Ant=*Pri;
    if(!*Pri)
    {
        *Pri=Nvo;
        Nvo->Sig=NULL;
        return;
    }
    while(Act&&(Act->Dato.Prom>Nvo->Dato.Prom))
    {
        Ant=Act;
        Act=Act->Sig;
    }
    if(Ant==Act)//CUANDO ES PRIMERO//
    {
        Nvo->Sig=Act;
        *Pri=Nvo;
        return;
    }
    Nvo->Sig=Act;//CUANDO ES ULTIMO Y CUANDO ES EL DEL MEDIO//
    Act->Sig=Nvo;
}
//---------------------------------------------------------------------------
void AgreAlum(struct Nodo **Pri)
{
    struct Alumnos Alu;//CREO UNA ESSTRUCTURA PARA INGRASARLA MANUALMENTE//
    Alu=INGDATAL();//LO MANDO A UNA FUNCION QUE ME CARGA LOS DATOS DEL TECLADO//
    AGREGALULI(Alu,Pri);//LO AGREGA AL FINAL DE LA LISTA//
}
//---------------------------------------------------------------------------
void AGREGALULI(struct Alumnos Al,struct Nodo **Pri)
{
    struct Nodo *Nvo,*Act=*Pri;
    if(!(Nvo=malloc(sizeof(struct Nodo))))//pido memoria//
    {
        printf("NO MEMORY");
        return;
    }
    Nvo->Dato=Al; //CARGO LA ESTRUCTURA A LA VARIABLE AL//
    Nvo->Sig=NULL;//APUNTO EL Sig DEL Nvo A NULL//
    if(!*Pri)//SI ESTA VACIA LA LISTA SE CARGA EN EL PRIMER LUGAR//
    {
        *Pri=Nvo;
        return;
    }
    while(Act->Sig)//MIENTRAS QUE NO ESTE EN EL FINAL DE LISTA...//
    {
        Act->Sig;
    }
    Act->Sig=Nvo;// ASI SERA EL ULTIMO DE LA LISTA//
}
//---------------------------------------------------------------------------
void MODIFPRAL(struct Nodo **Pri)//RECIBE EL PUNTERO A LA LISTA//
{
    long Leg;
    float Np,Pgt;
    struct Pun Ubica;
    scanf("%ld",&Leg);
    Ubica=BuscaNodo(Leg,Pri);//UBICA EL NODO A MODIFICAR EN LA LISTA//
    scanf("%f",&Np);
    Pgt=(Ubica.CantMat*Ubica.Prom+Np)/(Ubica.CantMat+1); //MODIFICO EL PGT//
    Ubica.Nvo->Dato.CantMat++; //AUMENTO LAS MATERIAS//
    if((Pgt!=Ubica.Nvo->Dato.Prom)&&(Ubica.Nvo->Dato.CantMat<40)) // SI EL PROMEDIO GENERAL SE MODIFICÓ REORDENO LA LISTA//
    {
        Ubica.Nvo->Dato.Prom=Pgt;
        Ubica.Ant->Sig=Ubica.Act;
        Insertar(Ubica.Nvo,Pri);// REORDENO LA LISTA//
    }
    if(Ubica.Nvo->Dato.CantMat==40)// SI APRUEBA LAS 40 MATERIAS...//
    {
        Ubica.Nvo->Dato.Prom=Pgt;
        Ubica.Ant->Sig=Ubica.Act;
        AGREGOARCHEGRE(Ubica.Nvo->Dato);
    }
}
//---------------------------------------------------------------------------
struct Pun BuscaNodo(long Leg,struct Nodo **Pri)
{
    struct Pun Aux;
    Aux.Ant=*Pri;
    Aux.Act=*Pri;
    while(Aux.Act&&(Aux.Act->Dato.leg!=leg))
    {
        Aux.Ant=Aux.Act;
        Aux.Act=Aux.Act->Sig;
    }
    Aux.Nvo=Aux.Act;
    Aux.Act=Aux.Act->Sig;
    return Aux;
}
//---------------------------------------------------------------------------
void AGREGOARCHEGRE
//---------------------------------------------------------------------------
char Menu(void)
{
    char Opcion;
    sy
}

//---------------------------------------------------------------------------