import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QFont

# Facts
infections = {
    'clabsi': {
        'symptoms': ['fever', 'chills', 'hypotension'],
        'tests': {
            'blood': {
                'pathogen': ['Staphylococcus Aureus']
            },
            'imaging': {
                'xray': 'Normal'
            }
        }
    },
    'cauti': {
        'symptoms': ['urinary frequency', 'dysuria', 'cloudy urine'],
        'tests': {
            'blood': {
                'pathogen': ['Escherichia Coli', 'Klebsiella Pneumoniae', 'Enterococcus Faecalis']
            },
            'imaging': {
                'xray': 'Normal'
            }
        }
    },
    'vap': {
        'symptoms': ['fever', 'cough', 'purulent sputum'],
        'tests': {
            'blood': {
                'pathogen': ['Pseudomonas Aeruginosa', 'Staphylococcus Aureus', 'Klebsiella Pneumoniae']
            },
            'imaging': {
                'xray': 'Abnormal'
            }
        }
    }
}

# Rules
def has_symptoms(infection, symptoms):
    return set(symptoms).issubset(infections[infection]['symptoms'])

def has_pathogen_in_blood(infection, pathogen):
    blood_test = infections[infection]['tests']['blood']
    return pathogen in blood_test['pathogen']

def has_abnormal_xray(infection):
    imaging_study = infections[infection]['tests']['imaging']
    return imaging_study['xray'] == 'Abnormal'

def is_infected(person, symptoms, pathogen, xray_result):
    for infection in infections:
        if (
            has_symptoms(infection, symptoms) and
            has_pathogen_in_blood(infection, pathogen) and
            (xray_result == 'Normal' or has_abnormal_xray(infection))
        ):
            return infection
    return None

# GUI
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Disease Diagnosis')
        self.setGeometry(100, 100, 500, 400)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        main_layout = QVBoxLayout(widget)

        font = QFont()  # Create a QFont object
        font.setFamily('Futura')  # Set the font family to 'Futura'
        font.setPointSize(16)  # Set the font size to 16 points

        self.label_symptoms = QLabel('Symptoms (separated by comma):')
        self.label_symptoms.setFont(font)  # Apply the font to the label
        self.entry_symptoms = QLineEdit()
        self.entry_symptoms.setFont(QFont('Arial', 14))  # Apply the font to the text input

        self.label_pathogen = QLabel('Pathogen (Blood Test):')
        self.label_pathogen.setFont(font)  # Apply the font to the label
        self.combo_pathogen = QComboBox()
        self.combo_pathogen.addItems(
            sum([infection['tests']['blood']['pathogen'] for infection in infections.values()], [])
        )
        self.combo_pathogen.setFont(QFont('Arial', 14))  # Apply the font to the combo box

        self.label_xray = QLabel('X-ray Result:')
        self.label_xray.setFont(font)  # Apply the font to the label
        self.combo_xray = QComboBox()
        self.combo_xray.addItems(['Normal', 'Abnormal'])
        self.combo_xray.setFont(QFont('Arial', 14))  # Apply the font to the combo box

        button_layout = QHBoxLayout()  # Horizontal layout for the button
        self.button_diagnose = QPushButton('Diagnose')
        self.button_diagnose.setFixedSize(100, 30)  # Set fixed size for the button
        self.button_diagnose.clicked.connect(self.diagnose_disease)
        button_layout.addStretch(1)  # Add stretchable space before the button
        button_layout.addWidget(self.button_diagnose)
        button_layout.addStretch(1)  # Add stretchable space after the button

        main_layout.addWidget(self.label_symptoms)
        main_layout.addWidget(self.entry_symptoms)
        main_layout.addWidget(self.label_pathogen)
        main_layout.addWidget(self.combo_pathogen)
        main_layout.addWidget(self.label_xray)
        main_layout.addWidget(self.combo_xray)
        main_layout.addLayout(button_layout)  # Add the button layout

    def diagnose_disease(self):
        symptoms = [s.strip() for s in self.entry_symptoms.text().split(',')]
        pathogen = self.combo_pathogen.currentText()
        xray_result = self.combo_xray.currentText()
        disease = is_infected(None, symptoms, pathogen, xray_result)
        self.show_result(disease)

    def show_result(self, disease):
        message_box = QMessageBox()
        if disease is not None:
            message_box.information(self, 'Diagnosis Result', f'The patient is diagnosed with: {disease}')
        else:
            message_box.information(self, 'Diagnosis Result', 'No matching infection found.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())