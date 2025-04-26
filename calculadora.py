import streamlit as st
import pandas as pd

def calculadora_page():
    st.title("Calculadora")
    column1, column2, column3 = st.columns(3)
    with column1:
        st.text_input("Cliente:")
    with column2:
        st.text_input("Empreendimento:")
    with column3:
        st.text_input("Apartamento:")

    column1, column2, column3 = st.columns(3)  
    
    with column2:
        left, right = st.columns(2)

        if left.button("Padrão", use_container_width=True):
            st.session_state['calc_type'] = 'Padrão'

        if right.button("Customizado",  use_container_width=True):
            st.session_state['calc_type'] = 'Customizado'
    
    if st.session_state.get('calc_type') == 'Padrão':

        left, mid, right = st.columns(3)

        with left:
            entrada = st.number_input("Valor de Entrada:", step=1000.00, value=0.00,min_value=0.00)

            inicio_obras = st.number_input("Valor a Pagar no Início das Obras:", step=1000.00, value=0.00,min_value=0.00)

            column1, column2 = st.columns(2)
            with column1:
                total_parcelas = st.number_input("Total de Parcelas:", step=1, value=0,min_value=0)
                reforcos_anuais = st.number_input("Total de Reforços:", step=1, value=0,min_value=0)
            with column2:
                valor_parcelas = st.number_input("Valores das Parcelas:", step=1000.00, value=0.00,min_value=0.00)
                valor_reforcos = st.number_input("Valores por Reforço:", step=1000.00, value=0.00,min_value=0.00)

            entrega_chaves = st.number_input("Valor a Pagar na Entrega das Chaves:", step=1000.00, value=0.00,min_value=0.00)        
            permuta = st.number_input("Valor de Permuta:", step=1000.00, value=0.00,min_value=0.00)      

        with mid:
            valor_imovel = st.number_input("Valor do Imóvel:", step=1000.00, value=0.00, format="%0.2f",min_value=0.00)
            total_calculado = entrada + inicio_obras + (total_parcelas * valor_parcelas) + (reforcos_anuais * valor_reforcos) + entrega_chaves + permuta
            st.markdown("Valor Total Calculado:")
            st.markdown("{:,}".format(total_calculado))

    if st.session_state.get('calc_type') == 'Customizado':

        left, mid, right = st.columns(3)
        df = pd.DataFrame(
    [
       {"Etapa":"", "Valor":0.00},
   ]
)       
        with left:
            st.write("Plano de Pagamento")
            edited_df = st.data_editor( df,
                                        num_rows='dynamic',
                                        column_config={ 
                                        "Valor": st.column_config.NumberColumn(
                                            "Valor",
                                            min_value=0,
                                            format="%.2f",
                                        )
                                        })

        with mid:
            valor_imovel = st.number_input("Valor do Imóvel:", step=1000.00, value=0.00, format="%0.2f",min_value=0.00)
            total_calculado = edited_df['Valor'].sum()
            st.markdown("Valor Total Calculado:")
            st.markdown("{:,}".format(total_calculado))
