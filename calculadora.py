import streamlit as st
import pandas as pd
# import locale
import segno
from funcs_suporte import format_brl, make_on_change, coalesce, remove_chars, build_string



# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

list_empreendimentos = [{"Empreendimento": "Senna Tower","Descrição": "Senna Tower traz ao Brasil as mais inovadoras soluções para a construção de supertalls e será o primeiro residencial a alcançar a maior certificação em sustentabilidade do mundo." , "url": "https://www.sennatower.com/"}]

escolha_empreendimento = []

for empreendimento in list_empreendimentos:
    escolha_empreendimento.append(empreendimento["Empreendimento"])
     

#####################################################################################################
############################### PAGE DEFINITION #####################################################
#####################################################################################################


def calculadora_page():

############################### HEADER CONTAINER ####################################################

    st.title("Calculadora")
    with st.container(border=True) as header_container:

        column1, column2, column3 = st.columns(3)

        with column1:
                st.markdown("<h4>Cliente:</h4>", unsafe_allow_html=True)    
                cliente = st.text_input("Cliente:",key='valor_cliente',label_visibility="collapsed")

        with column2:
                st.markdown("<h4>Empreendimento:</h4>", unsafe_allow_html=True)   
                empreendimento = st.selectbox(
                                                "Empreendimento:",
                                                escolha_empreendimento,
                                                index=None,
                                                label_visibility="collapsed"
                                            )

        with column3:
                st.markdown("<h4>Apartamento:</h4>", unsafe_allow_html=True)   
                apartamento = st.text_input("Apartamento:",key='valor_apartamento',label_visibility="collapsed")

        
        column1, column2, column3, column4, column5, column6 = st.columns(6)

        with column3:
                st.markdown("<h4>De:</h4>", unsafe_allow_html=True)   
                if 'valor_de' not in st.session_state:
                    st.session_state.valor_de = ""
                valor_de = st.text_input("De:" ,value=st.session_state.valor_de, key='valor_de',label_visibility="collapsed", on_change=make_on_change('valor_de'))
                            
        with column4:
                st.markdown("<h4>Por:</h4>", unsafe_allow_html=True)
                if 'valor_por' not in st.session_state:
                    st.session_state.valor_por = ""   
                valor_por = st.text_input("Por:", value=st.session_state.valor_por, key='valor_por' , label_visibility="collapsed", on_change=make_on_change('valor_por'))

        with column5:
                desconto =  int( coalesce( remove_chars(str(valor_de)),0) ) - int( coalesce( remove_chars(str(valor_por)),0)) 
                desconto_percentual = desconto / int( coalesce( remove_chars(str(valor_de)),1) ) * 100
                if valor_por != valor_de and desconto_percentual != 100:
                    st.metric("Desconto", format_brl(str(desconto)), delta= f'{desconto_percentual:.0f}%' , border=True)
                    st.markdown(
                                '''
                                <style>
                                [data-testid="stMetricDelta"] svg {
                                    transform: rotate(180deg);
                                }
                                </style>
                                ''',unsafe_allow_html=True)
            
############################### BODY CONTAINER ######################################################


    with st.container(border=False) as body_container:

            left, mid, right = st.columns(3)

###### CALCULADORA ######

            with mid:
                with st.container(border=True) as calculadora:
                    with st.container(border=True) as valores_de_entrada:
                        st.markdown("<h4>Valores de Entrada:</h4>", unsafe_allow_html=True)
                        
                        df_entrada = pd.DataFrame([{"Período": "No ato", "Valor": 0.00}])
                        tabela_entrada = st.data_editor(df_entrada, num_rows="dynamic",
                                                        column_config={
                                                            "Período": st.column_config.TextColumn("Período", max_chars=50),
                                                            "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f")
                                                        }, 
                                                        use_container_width=True, 
                                                        hide_index=True,
                                                        key='tabela_entrada')
                        
                        total_entradas = f'R$ {tabela_entrada['Valor'].sum():,.2f}'
                        total_entradas_formatado = total_entradas.replace('.', '|').replace(',', '.').replace('|', ',') # Troca para formato brasileiro
                        st.markdown(f'<div align="right">{total_entradas_formatado}</div>', unsafe_allow_html=True)



                    with st.container(border=True) as valores_de_parcelas:
                        st.markdown("<h4>Valores de Parcelas:</h4>", unsafe_allow_html=True)
                        
                        df_parcelas = pd.DataFrame([{"Período": "No ato", "Parcelas":0, "Valor": 0.00}])
                        tabela_parcelas = st.data_editor(df_parcelas, num_rows="dynamic",
                                                        column_config={
                                                            "Período": st.column_config.TextColumn("Período", max_chars=50),
                                                            "Parcelas": st.column_config.NumberColumn("Parcelas"),
                                                            "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f")
                                                        }, 
                                                        use_container_width=True, 
                                                        hide_index=True,
                                                        key='tabela_parcelas')
                        
                        tabela_parcelas['Total'] = tabela_parcelas['Parcelas'] * tabela_parcelas['Valor']
                        total_parcelas = f'R$ {tabela_parcelas['Total'].sum():,.2f}'
                        total_parcelas_formatado = total_parcelas.replace('.', '|').replace(',', '.').replace('|', ',') # Troca para formato brasileiro
                        st.markdown(f'<div align="right">{total_parcelas_formatado}</div>', unsafe_allow_html=True)


                    with st.container(border=True) as valores_de_reforcos:
                        st.markdown("<h4>Valores de Reforço:</h4>", unsafe_allow_html=True)
                        
                        df_reforcos = pd.DataFrame([{"Período": "No ato", "Reforços":0, "Valor": 0.00}])
                        tabela_reforcos = st.data_editor(df_reforcos, num_rows="dynamic",
                                                        column_config={
                                                            "Período": st.column_config.TextColumn("Período", max_chars=50),
                                                            "Reforços": st.column_config.NumberColumn("Reforços"),
                                                            "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f")
                                                        }, 
                                                        use_container_width=True, 
                                                        hide_index=True,
                                                        key='tabela_reforços')
                        
                        tabela_reforcos['Total'] = tabela_reforcos['Reforços'] * tabela_reforcos['Valor']                    
                        total_reforcos = f'R$ {tabela_reforcos['Total'].sum():,.2f}'
                        total_reforcos_formatado = total_reforcos.replace('.', '|').replace(',', '.').replace('|', ',') # Troca para formato brasileiro
                        st.markdown(f'<div align="right">{total_reforcos_formatado}</div>', unsafe_allow_html=True)



                    with st.container(border=True) as valores_entrega_chaves:
                        st.markdown("<h4>Valor a Pagar na Entrega das Chaves:</h4>", unsafe_allow_html=True)
                        
                        df_entrega_chaves = pd.DataFrame([{"Período": "No ato", "Valor": 0.00}])
                        tabela_entrega_chaves = st.data_editor(df_entrega_chaves, num_rows="dynamic",
                                                        column_config={
                                                            "Período": st.column_config.TextColumn("Período", max_chars=50),
                                                            "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f")
                                                        }, 
                                                        use_container_width=True, 
                                                        hide_index=True,
                                                        key='tabela_entrega_chaves')
                        
                        total_entrega_chaves = f'R$ {tabela_entrega_chaves['Valor'].sum():,.2f}'
                        total_entrega_chaves_formatado = total_entrega_chaves.replace('.', '|').replace(',', '.').replace('|', ',') # Troca para formato brasileiro
                        st.markdown(f'<div align="right">{total_entrega_chaves_formatado}</div>', unsafe_allow_html=True)



                    with st.container(border=True) as valores_permuta:
                        st.markdown("<h4>Valor de Permuta:</h4>", unsafe_allow_html=True)
                        
                        df_permuta = pd.DataFrame([{"Período": "No ato", "Valor": 0.00}])
                        tabela_permuta = st.data_editor(df_permuta, num_rows="dynamic",
                                                        column_config={
                                                            "Período": st.column_config.TextColumn("Período", max_chars=50),
                                                            "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f")
                                                        }, 
                                                        use_container_width=True, 
                                                        hide_index=True,
                                                        key='tabela_permuta')
                        
                        total_permuta = f'R$ {tabela_permuta['Valor'].sum():,.2f}'
                        total_permuta_formatado = total_permuta.replace('.', '|').replace(',', '.').replace('|', ',') # Troca para formato brasileiro
                        st.markdown(f'<div align="right">{total_permuta_formatado}</div>', unsafe_allow_html=True)
                    
                    total_planejado= ( tabela_entrada['Valor'].sum() + tabela_parcelas['Total'].sum() + tabela_reforcos['Total'].sum() + tabela_entrega_chaves['Valor'].sum() + tabela_permuta['Valor'].sum())

                    total_planejado = format_brl(str(total_planejado*10))

                    st.markdown(f'<div align="right"><h3>Valor Total: {total_planejado}</h3></div>', unsafe_allow_html=True)

                    

###### INFORMAÇÕES DO IMÓVEL ######

            with left:
                with st.container(border=True) as informacoes:
                    st.markdown("<h4>Informações do Imóvel:</h4>", unsafe_allow_html=True)
                    
                    if empreendimento == None:
                        st.markdown("", unsafe_allow_html=True)

                    else:
                        st.markdown(f'<h4>{empreendimento}</h4>', unsafe_allow_html=True)

                        for cadastro in list_empreendimentos:
                            if cadastro["Empreendimento"] == empreendimento:
                                link = segno.make(cadastro["url"])
                                link.save("link.png", border= 1, scale= 5)
                                with open("link.png", "rb") as f:
                                    bytes_link = f.read()
                                    st.image(bytes_link)
                                st.write(cadastro["Descrição"], unsafe_allow_html=True)
                                st.markdown(f'<a href="{cadastro["url"]}" target="_blank">Clique aqui para mais informações</a>', unsafe_allow_html=True)

###### RECOMENDAÇÕES ######
            
            with right:
                with st.container(border=True) as recomendacoes:
                    st.markdown("<h4>Recomendações</h4>", unsafe_allow_html=True)
                            
                    # Calcula os valores a serem sugeridos 
                    valor_por_digits = remove_chars(valor_por)
                    if not valor_por_digits:
                        return ""
                    valor_por_float = float(valor_por_digits) / 100
                    
                    diferenca = valor_por_float - (float(remove_chars(total_planejado))/100)

                    distribuir_em_parcelas = format_brl(str(diferenca*10 /  coalesce(tabela_parcelas['Parcelas'].sum(),1)))

                    distribuir_na_entrada = format_brl(str(round(float(diferenca / 6),2)))
                    
                    distribuir_em_reforcos = format_brl(str(diferenca*10 / coalesce(tabela_reforcos['Reforços'].sum(),1)))

                    # Cria textos de recomendações
                    if diferenca > 0:

                        st.write_stream(build_string('Seguem algumas sugestões para ajustar a diferença entre o valor sugerido e o calculado:','') )
                        st.write_stream(build_string('- Incrementar a entrada com 6 parcelas de ', distribuir_na_entrada) )
                        st.write_stream(build_string('- Aumentar o valor das parcelas em ', distribuir_em_parcelas) )
                        st.write_stream(build_string('- Aumentar o valor dos reforços em ', distribuir_em_reforcos) )

                    st.markdown("<h4>Considerações:</h4>", unsafe_allow_html=True)
                    texto_longo = st.text_area("Digite aqui seu texto:",label_visibility="collapsed", height=200)




