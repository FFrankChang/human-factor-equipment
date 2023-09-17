TMSiStyle = '''
* {
    background: transparent;
    font-size: 12px;
}                                

QMainWindow {
    border-image: url(TMSiFrontend/media/images/Achtergrond.png) 0 0 0 0 stretch stretch;
}

QPushButton { 
    background-color: white;
    border-style: solid; 
    border-radius: 14px;
    border-color:  #FC4C02;
    border-width: 4px;
    padding: 8px;
    color: black;
}



QPushButton:hover {
    background-color: #FC4C02;
    color: white;
    font-weight: bold;
}

QRadioButton::indicator {
    width: 13px;
    height: 13px;
}

QRadioButton::indicator::unchecked {
        image: url(TMSiFrontend/media/images/radiobutton_unchecked.png);
    }

QRadioButton::indicator::checked {
    image: url(TMSiFrontend/media/images/radiobutton_checked.png);
}

QRadioButton::indicator:unchecked:hover {
    image: url(TMSiFrontend/media/images/radiobutton_unchecked.png);
}

QRadioButton::indicator:unchecked:pressed {
    image: url(TMSiFrontend/media/images/radiobutton_unchecked.png);
}

QRadioButton::indicator:checked:hover {
    image: url(TMSiFrontend/media/images/radiobutton_checked.png);
}

QRadioButton::indicator:checked:pressed {
    image: url(TMSiFrontend/media/images/radiobutton_checked.png);
}
QFrame {
    background: transparent;
}

QToolBar {
    background: transparent;
    border-right: 1px solid #E5E5E5;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FC4C02, stop:1 #FF8200);
    width: 18px;
    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
    border-radius: 3px;
}

QGroupBox {
    font-weight: bold;
}

QComboBox {
    background: white;
    border: 1px solid #ced4da;
    border-radius: 15px;
    padding-left: 10px;
}

QComboBox::drop-down {
    border: 0px;
}

QComboBox::down-arrow {
    image: url(TMSiFrontend/media/images/arrow_down.png);
    width: 12px;
    height: 12px;
    margin-right: 15px;
}

QComboBox::on {
    border: 1px solid #FF8200;
}

QComboBox QAbstractItemView {
    border: 1px solid darkgrey;
    selection-background-color: #FF8200;
}

QListView {
    border: 1px solid rgba(0, 0, 0, 10%);
    padding: 5px;
    outline: 0px;
}

QListView::item {
    padding-left: 10px;
}

QListView::item:hover {
    background-color: #FF8200;
}

QScrollBar:vertical, QScrollBar:horizontal {
    background-color: #d6d6d6;
    width: 15px;
    margin: 15px 3px 15px 3px;
    border: 1px #d6d6d6;
    border-radius: 4px;
}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FC4C02, stop:1 #FF8200);;         
    min-height: 5px;
    border-radius: 4px;
}

QScrollBar::sub-line:vertical {
    margin: 3px 0px 3px 0px;
    border-image: url(TMSiFrontend/media/images/arrow_up.png);        /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    margin: 3px 0px 3px 0px;
    border-image: url(TMSiFrontend/media/images/arrow_left.png);        /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}


QScrollBar::add-line:vertical {
    margin: 3px 0px 3px 0px;
    border-image: url(TMSiFrontend/media/images/arrow_down.png);       /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal {
    margin: 0px 3px 0px 3px;
    border-image: url(TMSiFrontend/media/images/arrow_right.png);       /* # <-------- */
    width: 10px;
    height: 10px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}


QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {
    border-image: url(TMSiFrontend/media/images/arrow_up.png);                  /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on {
    border-image: url(TMSiFrontend/media/images/arrow_left.png);               /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on {
    border-image: url(TMSiFrontend/media/images/arrow_right.png);               /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {
    border-image: url(TMSiFrontend/media/images/arrow_down.png);                /* # <-------- */
    height: 10px;
    width: 10px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
    background: none;
}


QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QDialog {
background: white;
}

QCheckBox {
spacing: 5px;
}

QCheckBox::indicator {
width: 13px;
height: 13px;
}

QCheckBox::indicator:unchecked {
image: url(TMSiFrontend/media/images/checkbox_unchecked.png);
}

QCheckBox::indicator:unchecked:hover {
image: url(TMSiFrontend/media/images/checkbox_unchecked.png);
}

QCheckBox::indicator:unchecked:pressed {
image: url(TMSiFrontend/media/images/checkbox_unchecked.png);
}

QCheckBox::indicator:unchecked:disabled {
image: url(TMSiFrontend/media/images/checkbox_unchecked_disabled.png);
}

QCheckBox::indicator:checked {
image: url(TMSiFrontend/media/images/checkbox_checked.png);
}

QCheckBox::indicator:checked:hover {
image: url(TMSiFrontend/media/images/checkbox_checked.png);
}

QCheckBox::indicator:checked:pressed {
image: url(TMSiFrontend/media/images/checkbox_checked.png);
}

QCheckBox::indicator:checked:disabled {
image: url(TMSiFrontend/media/images/checkbox_checked_disabled.png);
}


'''