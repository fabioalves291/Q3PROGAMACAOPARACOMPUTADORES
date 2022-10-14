import requests
import os
import json
import sys

#variac
calendario = [31,28,31,30,31,30,31,31,30,31,30,31] # dias dos meses em ordem
mês = 1
capitais = dict()
arquivo ='dados\dados_clima.txt'


def menu():
    print('''{a:#^40}
{b}
{c}
{d}
        '''.format(a=' menu ',b='0 - buscar na internet os dados',c='1 - ler dados e executar calculos',d='#'*40))
dicionariofinal = dict()


while True:
    menu()
    alter = input(':')
    
    if alter== '0':
        ano = input('digite o ano:')
        try:
            os.mkdir('dados')
        except FileExistsError:
            print('pasta dados já existente')
            os.remove(r'dados/dados_clima.txt')
            pass
        
        
        for meses in calendario:
            for a in range(1,meses+1):
                data = '{}-{:0>2}-{:0>2}'.format(ano,mês,a)
                print(fr'buscando {data}')
                if a == (meses):
                    mês = int(mês)
                    mês = mês + 1
                    mês = str(mês)
                
                url = fr'https://apitempo.inmet.gov.br/condicao/capitais/{data}'
                retorno_dados = requests.get(url).json()
                
                for i in retorno_dados:
                    i = json.dumps(i)           #converte json/dicionario a str()
                    arquivo = open('dados/dados_clima.txt','a')
                    arquivo.write(i+'\n')
                    arquivo.close()
        print('{a:#^40}\nencaminhados para dados\dados_clima.csv \n{b}'.format(a=' dados  ',b=40*'#'))
    elif alter == '1':
        
        capitais = list()
        
        #------- pegando capitais -------------#
        file = open('dados/dados_clima.txt','r')
        #pegando bandeiras
        for dados in file:
            dados = json.loads(dados)
            if not dados['CAPITAL'] in capitais:
                capitais.append(dados['CAPITAL'])
        file.close()
        #--------------------------------------#
        
        
        for capital in capitais:
            #print(capital)
            #input('.')
            lista_aux_TMIN18 = list()
            lista_aux_TMAX18 = list()
            mintemp = float(100)
            maxtemp = float(0)
            file = open('dados/dados_clima.txt','r')
            for dados in file:
                dados = json.loads(dados)
                if capital == dados['CAPITAL']:

                    
                    #---- apagando o  * ------#
                    if '*' in dados['TMIN18'] :
                        dados['TMIN18'] = dados['TMIN18'][:-1]
                    if '*' in dados['TMAX18'] :
                        dados['TMAX18'] = dados['TMAX18'][:-1]
                    
                    lista_aux_TMIN18.append(dados['TMIN18'])
                    lista_aux_TMAX18.append(dados['TMAX18'])
                    #-------------------------#

                    
                    try:
                        #----- pegando valores min/max ----#
                        if float(dados['TMIN18']) < mintemp:
                            mintemp = float(dados['TMIN18'])
                          
                        if float(dados['TMAX18']) > maxtemp:
                            maxtemp = float(dados['TMAX18'])
                        #----------------------------------#
                    except ValueError:
                        file = open('log.txt','a')
                        log = 'erro: {}'.format(sys.exc_info())
                        file.write(log)
                        file.close()
            file.close()
            # somando lista
            auxiliartemp = 0

            
            #-------somando temperaturas--------#
            for temperatura  in lista_aux_TMIN18:
                #print(temperatura)
                try:
                    auxiliartemp = float(temperatura)+auxiliartemp
                    
                except ValueError:
                    #input('ValueError')
                    pass
                
            auxiliartemp0 = 0
            for temperatura  in lista_aux_TMAX18:
                try:
                    #print(temperatura)
                    auxiliartemp0 = float(temperatura)+auxiliartemp
                except ValueError:
                    pass
            #------------------------------------#

                
            dicionariofinal[capital] = {'MEDIA_TMIN': auxiliartemp/len(lista_aux_TMIN18),'MEDIA_TMAX':auxiliartemp0/len(lista_aux_TMAX18),'TMIN':mintemp,'TMAX':maxtemp}
            #print(dicionariofinal)

            
        #------criando arquivo limpo--------#
        file = open('resultadofinal.txt','w')
        file.close()
        #-----------------------------------#


        #-----escrevendo arquivo final------#
        file = open('resultadofinal.txt','a')
        for dadofinal in dicionariofinal:
            print((dicionariofinal[dadofinal]))
            lenn = len(dadofinal)
            file.write(dadofinal+(15 - lenn)*' '+str(dicionariofinal[dadofinal])+'\n')
        file.close()
        #-----------------------------------#
            #dicionariofinal[capital] = {'media_temp_min':}
            
        input('processo finalizado !')
            

