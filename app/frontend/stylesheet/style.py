def obtener_estilos():
    return """
        QWidget {
            font-family: Arial;
            color: #4ADE80;
        }

        QMainWindow {
            background-color: #121212;
        }

        #menu {
            background-color: #0D0D0D;
        }

        #logo {
            color: #22C55E;
            font-size: 19px;
            font-weight: bold;
            padding-bottom: 25px;
        }

        #menuButton {
            background-color: transparent;
            color: #9CA3AF;
            border: none;
            padding: 13px;
            text-align: left;
            border-radius: 7px;
            font-size: 14px;
        }

        #menuButton:hover {
            background-color: #1E1E1E;
            color: #4ADE80;
        }

        #version {
            color: #6B7280;
            font-size: 11px;
        }

        #contenido {
            background-color: #121212;
        }

        #titulo {
            font-size: 25px;
            font-weight: bold;
            color: #4ADE80;
        }

        #estado {
            color: #22C55E;
            font-size: 13px;
        }

        #tarjeta {
            background-color: #1E1E1E;
            border: 1px solid #2E2E2E;
            border-radius: 10px;
        }

        #textoTarjeta {
            color: #9CA3AF;
            font-size: 12px;
        }

        #numeroTarjeta {
            color: #22C55E;
            font-size: 25px;
            font-weight: bold;
        }

        #subtitulo {
            font-size: 18px;
            font-weight: bold;
            color: #4ADE80;
        }

        /* TABLAS */

        QTableWidget {
            background-color: #1E1E1E;
            alternate-background-color: #262626;
            color: #DCFCE7;
            border: 1px solid #2E2E2E;
            border-radius: 8px;
            gridline-color: #2E2E2E;
            selection-background-color: #166534;
            selection-color: #FFFFFF;
        }

        QHeaderView::section {
            background-color: #171717;
            color: #22C55E;
            padding: 12px;
            border: none;
            font-weight: bold;
        }

        QTableWidget::item {
            padding: 10px;
        }

        /* CAMPOS DE TEXTO */

        QLineEdit {
            background-color: #1E1E1E;
            color: #DCFCE7;
            border: 1px solid #2E2E2E;
            border-radius: 7px;
            padding: 10px;
            font-size: 13px;
        }

        QLineEdit:focus {
            border: 1px solid #22C55E;
        }

        QLineEdit:disabled {
            background-color: #141414;
            color: #6B7280;
        }

        /* AREA DE INFORMACION */

        QTextEdit {
            background-color: #1E1E1E;
            color: #DCFCE7;
            border: 1px solid #2E2E2E;
            border-radius: 7px;
            padding: 10px;
            font-size: 13px;
        }

        QTextEdit:focus {
            border: 1px solid #22C55E;
        }

        /* BOTONES */

        QPushButton {
            background-color: #1E1E1E;
            color: #4ADE80;
            border: 1px solid #2E2E2E;
            border-radius: 7px;
            padding: 10px 15px;
            font-size: 13px;
        }

        QPushButton:hover {
            background-color: #166534;
            color: #FFFFFF;
            border: 1px solid #22C55E;
        }

        QPushButton:pressed {
            background-color: #14532D;
        }

        QPushButton:disabled {
            background-color: #141414;
            color: #6B7280;
            border: 1px solid #2E2E2E;
        }

        #actualizar, #escanear {
            background-color: #1E1E1E;
            color: #4ADE80;
            border: 1px solid #22C55E;
            border-radius: 7px;
            padding: 10px 20px;
        }

        #actualizar:hover, #escanear:hover {
            background-color: #166534;
            color: #FFFFFF;
        }

        /* COMBOBOX (DESPLEGABLES) */

        QComboBox {
            background-color: #1E1E1E;
            color: #DCFCE7;
            border: 1px solid #2E2E2E;
            border-radius: 7px;
            padding: 10px;
            font-size: 13px;
        }

        QComboBox:hover, QComboBox:focus {
            border: 1px solid #22C55E;
        }

        QComboBox::drop-down {
            border: none;
            width: 28px;
        }

        QComboBox QAbstractItemView {
            background-color: #1E1E1E;
            color: #DCFCE7;
            border: 1px solid #22C55E;
            selection-background-color: #166534;
            selection-color: #FFFFFF;
            outline: none;
        }

        /* VENTANAS DE MENSAJE */

        QMessageBox {
            background-color: #171717;
        }

        QMessageBox QLabel {
            color: #DCFCE7;
            font-size: 13px;
        }

        QMessageBox QPushButton {
            min-width: 75px;
            padding: 8px 15px;
        }
    """