from pathlib import Path
from typing import List, Tuple

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


TASA = 7.04

def format_money(money: float) -> str:
    """Formatea una cantidad como moneda."""
    return "${:,.2f} MN".format(money)

def format_duration(months: int) -> str:
    """Formatea una duración en meses como años y meses."""
    if months > 12:
        return f'{months // 12} años y {months % 12} meses'
    return f'{months} meses'

def calculate_accumulated_values(init_money: float, duration: int, monthly_rate: float) -> Tuple[List[float], List[float]]:
    """Calcula los valores acumulados y compuestos mensualmente."""
    accumulated_values = []
    compounded_values = []
    current_value = init_money

    for month in range(duration):
        accumulated_values.append(init_money * (month + 1))  # Capital acumulado
        current_value = current_value * (1 + monthly_rate)  # Interés compuesto
        compounded_values.append(current_value)
        current_value += init_money  # Añadir contribución mensual

    return accumulated_values, compounded_values

def main():
    st.image(Path(__file__).parent/'assets/logo_banorte.png', width=450)
    st.title('Simulación de Fondo de Inversión')

    # Entrada: Capital inicial
    init_money = st.slider(
        label='Ingresando al fondo de inversión mensualmente:',
        min_value=1000,
        max_value=22346,
        value=3350,
        format='$ %d',
        step=100
    )
    st.write(f"Capital seleccionado: {format_money(init_money)}")

    # Entrada: Duración
    duration = st.slider(
        label='Duración de la inversión:',
        min_value=1,
        max_value=36,
        value=12,
        format='%d meses',
    )
    st.write(f"Duración seleccionada: {format_duration(duration)}")

    # Cálculo del valor total acumulado
    monthly_rate = TASA / 100 / 12  # Tasa mensual
    accumulated_value = init_money * ((1 + monthly_rate) ** duration - 1) / monthly_rate

    st.markdown(
        f"Si usted hubiera invertido **{format_money(init_money)}** hace **{format_duration(duration)}**, "
        f"ingresando la misma cantidad mensualmente, el monto total con ganancias sería de:"
    )
    st.markdown(f"<h2 style='text-align: center; color: green;'>{format_money(accumulated_value)}</h2>", unsafe_allow_html=True)
    st.markdown('---')

    # Calcular valores mensuales
    months = list(range(1, duration + 1))
    accumulated_values, compounded_values = calculate_accumulated_values(init_money, duration, monthly_rate)

    # Crear DataFrame
    data = pd.DataFrame({
        'Mes': months,
        'Capital acumulado (sin intereses)': accumulated_values,
        'Valor compuesto (con intereses)': compounded_values,
    })

    # Gráfica
    fig, ax = plt.subplots()
    ax.plot(data['Mes'], data['Valor compuesto (con intereses)'], label='Valor compuesto (con intereses)', linewidth=2, color='green')
    ax.plot(data['Mes'], data['Capital acumulado (sin intereses)'], label='Capital acumulado (sin intereses)', linewidth=2, color='black')
    ax.set_title('Crecimiento del Interés Compuesto')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Valor acumulado ($)')
    ax.legend()

    st.pyplot(fig)

    # Tabla
    st.write('Tabla de valores:')
    st.dataframe(data)

if __name__ == '__main__':
    main()
