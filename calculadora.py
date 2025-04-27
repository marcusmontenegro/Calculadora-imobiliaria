import streamlit as st
import pandas as pd
import locale
import re

#locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def format_brl(raw: str) -> str:
        digits = re.sub(r'\D', '', raw)
        if not digits:
            return ""
        value = float(digits) / 100
        return locale.currency(value, grouping=True)


    # Generate on_change callbacks for formatting
def make_on_change(key):
        def callback():
            st.session_state[key] = format_brl(st.session_state[key])
        return callback

def calculadora_page():

#####################################################################################################
############################### HEADER CONTAINER ####################################################
#####################################################################################################


    st.title("Calculadora")
    with st.container(border=True) as header_container:

        column1, column2, column3 = st.columns(3)

        with column1:
                st.markdown("<h4>Cliente:</h4>", unsafe_allow_html=True)    
                cliente = st.text_input("Cliente:",key='valor_cliente',label_visibility="collapsed")

        with column2:
                st.markdown("<h4>Empreendimento:</h4>", unsafe_allow_html=True)   
                empreendimento = st.text_input("Empreendimento:",key='valor_empreendimento',label_visibility="collapsed")
        with column3:
                st.markdown("<h4>Apartamento:</h4>", unsafe_allow_html=True)   
                empreendimento = st.text_input("Apartamento:",key='valor_apartamento',label_visibility="collapsed")



        
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

        

#####################################################################################################
############################### BODY CONTAINER ######################################################
#####################################################################################################

    with st.container(border=False) as body_container:

            left, mid, right = st.columns(3)

################################ CALCULADORA ########################################################

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

################################ RECOMENDAÇÕES ########################################################
            
            with right:
                with st.container(border=True) as recomendacoes:
                    st.markdown("<h4>Recomendações:</h4>", unsafe_allow_html=True)
                            
                    valor_por_digits = re.sub(r'\D', '', valor_por)
                    if not valor_por_digits:
                        return ""
                    valor_por_float = float(valor_por_digits) / 100
                    
                    diferenca = valor_por_float - ( tabela_entrada['Valor'].sum() + tabela_parcelas['Total'].sum() + tabela_reforcos['Total'].sum() + tabela_entrega_chaves['Valor'].sum() + tabela_permuta['Valor'].sum())
                    

                    distribuir_em_parcelas = diferenca / tabela_parcelas['Parcelas'].sum()

                    distribuir_na_entrada = diferenca / 6
                    
                    distribuir_em_reforcos = diferenca / tabela_reforcos['Reforços'].sum()
                    
                    
                    
                    st.markdown("<h4>Considerações:</h4>", unsafe_allow_html=True)
                    texto_longo = st.text_area("Digite aqui seu texto:",label_visibility="collapsed", height=200)



