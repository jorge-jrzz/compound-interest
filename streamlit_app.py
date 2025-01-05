'''Simulation of an investment fund with compound interest'''

from pathlib import Path

import streamlit as st
import matplotlib.pyplot as plt


TASA = 8.03  # Tasa anual


def format_money(money: float) -> str:
    """Formatea una cantidad como moneda."""
    return "${:,.2f} MN".format(money)


def format_duration(months: int) -> str:
    """Formatea una duración en meses como años y meses."""
    if months > 12:
        return f'{months // 12} años y {months % 12} meses'
    return f'{months} meses'


def main():
    st.image(Path(__file__).parent/'assets/logo_banorte.png', width=450)
    st.title('Simulación de Fondo de Inversión')

    # Entrada: Capital inicial
    initial_capital = st.slider(
        label='Ingresando al fondo de inversión mensualmente:',
        min_value=1000,
        max_value=22346,
        value=3350,
        format='$ %d',
        step=100
    )
    st.write(f"Capital seleccionado: {format_money(initial_capital)}")

    # Entrada: Duración
    months = st.slider(
        label='Duración de la inversión:',
        min_value=1,
        max_value=36,
        value=12,
        format='%d meses',
    )
    st.write(f"Duración seleccionada: {format_duration(months)}")

    # Cálculo del valor total acumulado
    monthly_rate = (1 + (TASA / 100)) ** (1 / 12) - 1 # Tasa mensual
    accumulated = [0]
    interest = [0]

    for _ in range(1, months + 1):
        new_accumulated = accumulated[-1] + initial_capital
        new_interest = new_accumulated * monthly_rate
        accumulated.append(new_accumulated)
        interest.append(interest[-1] + initial_capital + new_interest)

    st.markdown(
        f"Si usted hubiera invertido **{format_money(initial_capital)}** hace **{format_duration(months)}**, "
        f"ingresando la misma cantidad mensualmente, el monto total con ganancias sería de:"
    )
    st.markdown(f"<h2 style='text-align: center; color: green;'>{format_money(interest[-1])}</h2>", unsafe_allow_html=True)
    st.markdown('---')

    plt.plot(range(months + 1), accumulated, label='Capital acumulado', marker='o')
    plt.plot(range(months + 1), interest, label='Capital con interes compuesto', marker='o')
    plt.title("Crecimiento del Interés Compuesto", fontsize=14)
    plt.xlabel("Mes", fontsize=12)
    plt.ylabel("Valor acumulado ($)", fontsize=12)
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)


if __name__ == '__main__':
    main()
