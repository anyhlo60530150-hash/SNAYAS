def obtener_estilos():
    return """
        QWidget {
            font-family: Arial;
            color: #E5E7EB;
        }

        QMainWindow {
            background-color: #111827;
        }

        #menu {
            background-color: #0B1220;
        }

        #logo {
            color: #38BDF8;
            font-size: 19px;
            font-weight: bold;
            padding-bottom: 25px;
        }

        #menuButton {
            background-color: transparent;
            color: #AAB4C5;
            border: none;
            padding: 13px;
            text-align: left;
            border-radius: 7px;
            font-size: 14px;
        }

        #menuButton:hover {
            background-color: #1E293B;
            color: #38BDF8;
        }

        #version {
            color: #64748B;
            font-size: 11px;
        }

        #contenido {
            background-color: #111827;
        }

        #titulo {
            font-size: 25px;
            font-weight: bold;
            color: white;
        }

        #estado {
            color: #4ADE80;
            font-size: 13px;
        }

        #tarjeta {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 10px;
        }

        #textoTarjeta {
            color: #94A3B8;
            font-size: 12px;
        }

        #numeroTarjeta {
            color: #38BDF8;
            font-size: 25px;
            font-weight: bold;
        }

        #subtitulo {
            font-size: 18px;
            font-weight: bold;
            color: white;
        }

        QTableWidget {
            background-color: #1E293B;
            alternate-background-color: #253449;
            color: #E5E7EB;
            border: 1px solid #334155;
            border-radius: 8px;
            gridline-color: #334155;
            selection-background-color: #075985;
            selection-color: white;
        }

        QHeaderView::section {
            background-color: #0F172A;
            color: #38BDF8;
            padding: 12px;
            border: none;
            font-weight: bold;
        }

        QTableWidget::item {
            padding: 10px;
        }

        #actualizar, #escanear {
            background-color: #1E293B;
            color: #38BDF8;
            border: 1px solid #38BDF8;
            border-radius: 7px;
            padding: 10px 20px;
        }

        #actualizar:hover, #escanear:hover {
            background-color: #075985;
            color: white;
        }

        QPushButton {
            font-size: 13px;
        }
    """