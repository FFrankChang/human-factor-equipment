'''
(c) 2023 Twente Medical Systems International B.V., Oldenzaal The Netherlands

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#######  #     #   #####   #
   #     ##   ##  #        
   #     # # # #  #        #
   #     #  #  #   #####   #
   #     #     #        #  #
   #     #     #        #  #
   #     #     #  #####    #

/**
 * @file dialog_confirm.py 
 * @brief 
 * Dialog object to communicate with the user to get confirmation of action.
 */


'''
from ..dialog import *

class DialogConfirm(Dialog):
    """Dialog object to get confirmation of action from the user
    """
    def __init__(self, title = "Dialog", message = "message", parent=None):
        """Initialize DialogConfirm object

        :param title: title of the dialog, defaults to "Dialog"
        :type title: str, optional
        :param message: message of the dialog, defaults to "message"
        :type message: str, optional
        :param parent: parent widget if needed, defaults to None
        :type parent: QWidget, optional
        """
        super().__init__(title, message, parent)
        self.layout.takeAt(1)
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)
        return