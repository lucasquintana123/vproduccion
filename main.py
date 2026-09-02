# ============================================================
# PANTALLA INICIO
# ============================================================

if st.session_state.pagina == "inicio":

    st.markdown(
        """
        <div class="titulo-principal">
            <h1>🍫 Modelo Inteligente de Exportación del Cacao</h1>
            <p>
                Sistema basado en Machine Learning e Inteligencia Artificial
                para el análisis predictivo de exportaciones de cacao.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="linea"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            text-align: center;
            font-size: 20px;
            color: #d0d0d0;
            padding-bottom: 30px;
        ">
            Seleccione la versión del sistema que desea utilizar.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    # ========================================================
    # DEMO
    # ========================================================

    with col1:

        st.markdown(
            """
            <div class="card">

                <h2>Demo</h2>

                <p>
                    Ejecuta el modelo con datos precargados.
                </p>

                <p>
                    Incluye:
                </p>

                <p>
                    ✔ Predicciones automáticas<br>
                    ✔ Métricas del modelo<br>
                    ✔ Visualizaciones<br>
                    ✔ Análisis con IA
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Ingresar a la Demo",
            key="demo",
            use_container_width=True
        ):
            st.session_state.pagina = "demo"
            st.rerun()

    # ========================================================
    # COMPLETA
    # ========================================================

    with col2:

        st.markdown(
            """
            <div class="card">

                <h2>Versión Completa</h2>

                <p>
                    Plataforma interactiva personalizada.
                </p>

                <p>
                    Incluye:
                </p>

                <p>
                    ✔ Carga de Excel<br>
                    ✔ Filtros avanzados<br>
                    ✔ Visualizaciones dinámicas<br>
                    ✔ Descarga de resultados
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Ingresar a la Versión Completa",
            key="completa",
            use_container_width=True
        ):
            st.session_state.pagina = "completa"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="footer">
            Proyecto aplicado
        </div>
        """,
        unsafe_allow_html=True
    )
