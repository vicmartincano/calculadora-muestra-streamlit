import math
import streamlit as st

st.set_page_config(page_title='Calculadora de tamaño de muestra', page_icon='📊', layout='centered')

Z_VALUES = {
    '80%': 1.282,
    '85%': 1.440,
    '90%': 1.645,
    '95%': 1.960,
    '98%': 2.326,
    '99%': 2.576,
}

st.title('📊 Calculadora de tamaño de muestra')
st.caption('Población finita · Encuestas, auditorías, estudios y diagnósticos')

st.info(
    'Usa esta herramienta cuando conoces el número total de personas, registros o elementos '
    'de tu población y necesitas definir cuántos debes seleccionar para obtener resultados '
    'con un nivel de precisión determinado.'
)

with st.expander('¿Qué debes definir antes de calcular?', expanded=True):
    st.markdown('''
**1. Población total (N):** número total de personas o elementos que podrías estudiar.  
**2. Nivel de confianza:** qué tan seguro quieres estar de que la muestra representa a la población.  
**3. Margen de error:** diferencia máxima aceptable entre el resultado de la muestra y el valor real de la población.  
**4. Proporción esperada (p):** estimación de la característica que buscas medir. Si no la conoces, usa 50%; es la opción más conservadora.

**Ejemplo:** si hay 500 colaboradores y quieres conocer su percepción, la población es 500. Con 90% de confianza y 10% de error, la herramienta estima cuántas encuestas necesitas.
''')

col1, col2 = st.columns(2)
with col1:
    N = st.number_input('Población total (N)', min_value=1, value=500, step=1,
                        help='Cantidad total de personas, registros o elementos disponibles para el estudio.')
    confidence_label = st.selectbox('Nivel de confianza', list(Z_VALUES.keys()), index=2,
                                    help='90% suele ser útil para estudios exploratorios; 95% es una elección frecuente en investigaciones y auditorías.')
with col2:
    error_pct = st.slider('Margen de error (%)', 1, 20, 10, 1,
                          help='Un error menor exige una muestra mayor. Por ejemplo, 5% requiere más observaciones que 10%.')
    p_pct = st.slider('Proporción esperada p (%)', 1, 99, 50, 1,
                      help='Déjalo en 50% cuando no tengas una estimación previa confiable.')

z = Z_VALUES[confidence_label]
e = error_pct / 100
p = p_pct / 100
q = 1 - p
numerator = N * (z ** 2) * p * q
denominator = (e ** 2) * (N - 1) + (z ** 2) * p * q
n_exact = numerator / denominator
n_final = math.ceil(n_exact)

st.divider()
st.subheader('Resultado')
a, b, c = st.columns(3)
a.metric('Muestra mínima', f'{n_final:,}'.replace(',', '.') + ' unidades')
b.metric('Cálculo exacto', f'{n_exact:.2f}')
c.metric('Fracción de la población', f'{(n_final / N) * 100:.1f}%')

st.success(f'Debes incluir **al menos {n_final:,}** personas o elementos en la muestra. El valor se redondea hacia arriba para no perder precisión.'.replace(',', '.'))

with st.expander('Ver fórmula y sustitución de valores'):
    st.latex(r'n = \frac{N \cdot Z^2 \cdot p \cdot q}{e^2 \cdot (N - 1) + Z^2 \cdot p \cdot q}')
    st.markdown(f'''**Valores usados**
- N = {N:,}
- Z = {z}
- e = {e:.2f} ({error_pct}%)
- p = {p:.2f} ({p_pct}%)
- q = {q:.2f} ({100 - p_pct}%)

**Sustitución**''')
    st.latex(rf'n = \frac{{{N} \times {z:.3f}^2 \times {p:.2f} \times {q:.2f}}}{{{e:.2f}^2 \times ({N} - 1) + {z:.3f}^2 \times {p:.2f} \times {q:.2f}}} = {n_exact:.2f}')

st.subheader('Ajuste por no respuesta')
st.write('Si esperas que algunas personas no respondan, aumenta el número de invitaciones. Esto no cambia la muestra válida requerida; solo evita quedarte corto.')
response_rate = st.slider('Tasa esperada de respuesta (%)', 10, 100, 80, 5)
invitations = math.ceil(n_final / (response_rate / 100))
st.metric('Personas o elementos que conviene invitar/seleccionar', f'{invitations:,}'.replace(',', '.'))

with st.expander('Recomendaciones de uso'):
    st.markdown('''
- Selecciona la muestra con un método que reduzca sesgos: aleatorio simple, sistemático o estratificado.
- Si la población es muy pequeña y la muestra calculada se acerca al total, puede ser más útil hacer un censo.
- El cálculo asume que cada elemento tiene una oportunidad razonable de ser seleccionado.
- Para estudios con grupos muy diferentes entre sí, considera calcular o distribuir la muestra por estratos.
- El resultado define cantidad, no reemplaza el diseño metodológico ni los criterios de inclusión/exclusión.
''')

st.divider()
autor_col1, autor_col2 = st.columns([1, 4], vertical_alignment='center')
with autor_col1:
    st.image('autor_victor_cano.jpeg', width=100)
with autor_col2:
    st.markdown('''
**Autor:** Víctor Javier Cano González  
Ingeniero Industrial · MSc. Supply Chain Management  
Especialista en Inteligencia de Negocios · Especialista en Logística Empresarial / DDMRP
''')

st.caption('Herramienta orientativa para estimar tamaño de muestra en poblaciones finitas.')
