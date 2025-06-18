import streamlit as st
import pandas as pd

st.set_page_config(page_title="Práctica Contable", layout="wide")
st.title("Práctica Contable: Asientos, Libro Mayor y Balance")

# Definición inicial de asientos contables sugeridos
default_entries = [
    {"Fecha": "2025-06-01", "Cuenta": "Banco", "Debe": 100000, "Haber": 0},
    {"Fecha": "2025-06-01", "Cuenta": "Capital Social", "Debe": 0, "Haber": 100000},
    {"Fecha": "2025-06-02", "Cuenta": "Compras", "Debe": 50000, "Haber": 0},
    {"Fecha": "2025-06-02", "Cuenta": "IVA Crédito Fiscal", "Debe": 10500, "Haber": 0},
    {"Fecha": "2025-06-02", "Cuenta": "Proveedores", "Debe": 0, "Haber": 60500},
    {"Fecha": "2025-06-03", "Cuenta": "Clientes", "Debe": 36300, "Haber": 0},
    {"Fecha": "2025-06-03", "Cuenta": "Servicios Prestados", "Debe": 0, "Haber": 30000},
    {"Fecha": "2025-06-03", "Cuenta": "IVA Débito Fiscal", "Debe": 0, "Haber": 6300},
    {"Fecha": "2025-06-04", "Cuenta": "Banco", "Debe": 36300, "Haber": 0},
    {"Fecha": "2025-06-04", "Cuenta": "Clientes", "Debe": 0, "Haber": 36300},
    {"Fecha": "2025-06-05", "Cuenta": "Sueldos y Salarios", "Debe": 20000, "Haber": 0},
    {"Fecha": "2025-06-05", "Cuenta": "Banco", "Debe": 0, "Haber": 20000},
]

# Editable: usuario puede añadir/editar asientos
entries_df = pd.DataFrame(default_entries)
st.subheader("1. Registro de Asientos Contables")
edited_df = st.data_editor(entries_df, num_rows="dynamic", use_container_width=True)

# 2. Desarrollo del Libro Mayor
grouped = edited_df.groupby("Cuenta").agg(
    Debe=pd.NamedAgg(column="Debe", aggfunc="sum"),
    Haber=pd.NamedAgg(column="Haber", aggfunc="sum")
)
grouped["Saldo"] = grouped["Debe"] - grouped["Haber"]
st.subheader("2. Libro Mayor")
st.dataframe(grouped.reset_index(), use_container_width=True)

# 3. Elaboración del Balance
t_balance = grouped.copy()
t_balance["AuxDebe"] = t_balance["Saldo"].apply(lambda x: x if x > 0 else 0)
t_balance["AuxHaber"] = t_balance["Saldo"].apply(lambda x: -x if x < 0 else 0)
balance_summary = pd.DataFrame({
    "Total Debe": [t_balance["AuxDebe"].sum()],
    "Total Haber": [t_balance["AuxHaber"].sum()]
})
st.subheader("3. Balance de Sumas y Saldos")
st.dataframe(balance_summary, use_container_width=True)
if balance_summary.at[0, "Total Debe"] == balance_summary.at[0, "Total Haber"]:
    st.success("✅ El Balance está cuadrado.")
else:
    st.error("❌ El Balance NO cuadra.")

# 4. Visualización de Resultados
st.subheader("4. Visualización de Saldos por Cuenta")
st.bar_chart(grouped["Saldo"])
