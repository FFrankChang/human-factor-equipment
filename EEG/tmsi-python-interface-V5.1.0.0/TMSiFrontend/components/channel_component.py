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
 * @file channel_component.py 
 * @brief 
 * Component to collect, show and manipulate information about channels.
 */


'''
from PySide2 import QtWidgets

class ChannelComponent:
    """Component to collect information for the channel
    """
    def __init__(self, 
        index, 
        layout, 
        widget, 
        connect_chb = None, 
        checked_state = True, 
        connect_offset = None,
        offset_value = 0,
        connect_scale = None,
        scale_value = 100,
        connect_combo = None,
        name = "Channel component"):
        """Initialization of ChannelComponent

        :param index: channel index
        :type index: int
        :param layout: parent layout where it lays
        :type layout: Q*Layout
        :param widget: Widget where it lays
        :type widget: QWidget
        :param connect_chb: action to be triggered when clicking on enabled/disabled checkbox, defaults to None
        :type connect_chb: function, optional
        :param checked_state: initial state of the checkbox (enabled or disabled), defaults to True
        :type checked_state: bool, optional
        :param connect_offset: action to be triggered when changing offset, defaults to None
        :type connect_offset: function, optional
        :param offset_value: initial offset value, defaults to 0
        :type offset_value: float, optional
        :param connect_scale: action to be triggered when changing scale, defaults to None
        :type connect_scale: function, optional
        :param scale_value: initial scale value, defaults to 100
        :type scale_value: float, optional
        :param connect_combo: action to be triggered when changing color, defaults to None
        :type connect_combo: function, optional
        :param name: name, defaults to "Channel component"
        :type name: str, optional
        """
        self._name = name
        self._index = index
        self._parent_layout = layout
        self._parent_widget = widget
        
        self._checkbox = QtWidgets.QCheckBox(self._parent_widget)
        self._checkbox.setObjectName("chb_channel_{}".format(self._index))
        self._checkbox.setText("{}".format(self._name))
        self._checkbox.setChecked(checked_state)
        if connect_chb is not None:
            self._checkbox.stateChanged.connect(connect_chb)

        self._combobox = QtWidgets.QComboBox(self._parent_widget)
        self._combobox.wheelEvent = lambda event: None
        self._combobox.setObjectName("cbb_channel_{}".format(self._index))
        for i in ChannelComponent.colors().keys():
            self._combobox.addItem(i)
        if connect_combo is not None:
            self._combobox.currentIndexChanged.connect(connect_combo)

        self._offset = QtWidgets.QDoubleSpinBox(self._parent_widget)
        self._offset.wheelEvent = lambda event: None
        self._offset.setObjectName("spin_offset_{}".format(self._index))
        self._offset.setMaximum(1_000_000_000)
        self._offset.setMinimum(-1_000_000_000)
        self._offset.setValue(offset_value)
        if connect_offset is not None:
            self._offset.valueChanged.connect(connect_offset)
        
        self._scale = QtWidgets.QDoubleSpinBox(self._parent_widget)
        self._scale.wheelEvent = lambda event: None
        self._scale.setObjectName("spin_scale_{}".format(self._index))
        self._scale.setMaximum(1_000_000_000)
        self._scale.setMinimum(-1_000_000_000)
        self._scale.setValue(scale_value)
        if connect_scale is not None:
            self._scale.valueChanged.connect(connect_scale)

        self._frame = QtWidgets.QFrame(self._parent_widget)
        self._frame.setObjectName("frame_{}".format(self._index))
        self._parent_layout.addWidget(self._frame)
        
        self._horizontal_layout = QtWidgets.QGridLayout()
        self._horizontal_layout.setObjectName("layout_{}".format(self._index))
        self._frame.setLayout(self._horizontal_layout)
        
        self._horizontal_layout.addWidget(self._checkbox, 0, 0, 1, 1)
        self._horizontal_layout.addWidget(self._combobox, 0, 1, 1, 1)
        self._horizontal_layout.addWidget(self._offset, 1, 0, 1, 1)
        self._horizontal_layout.addWidget(self._scale, 1, 1, 1, 1)

    def colors():
        """Available colors

        :return: colors dictionary
        :rtype: dict
        """
        _dict = {}
        _dict["Black"]= (20,20,20)
        _dict["Red"]= (200,20,20)
        _dict["Green"]= (20,200,20)
        _dict["Blue"]= (20,20,200)
        return _dict
    
    def delete(self):
        """Delete component
        """
        self._frame.deleteLater()

    def get_color(self):
        """Get color rgb

        :return: rgb values for the selected color
        :rtype: tuple
        """
        return ChannelComponent.colors()[self._combobox.currentText()]

    def get_index(self):
        """Get component index

        :return: index of the component
        :rtype: int
        """
        return self._index

    def get_name(self):
        """Get channel name

        :return: the name of the channel
        :rtype: str
        """
        return self._name
    
    def get_offset(self):
        """Get the offset of the component

        :return: offset
        :rtype: float
        """
        return self._offset.value()

    def get_scale(self):
        """Get the scale of the component

        :return: scale
        :rtype: float
        """
        return self._scale.value()
    
    def set_checked(self, checked):
        """Set channel checked"""
        self._checkbox.setChecked(checked)
    
    def set_color(self, color_index):
        """Set channel's color

        :param color_index: index of the color to choose
        :type color_index: int
        """
        self._combobox.setCurrentIndex(color_index % self._combobox.count())
    
    def set_offset(self, value):
        """Set offset of the component

        :param value: offset
        :type value: float
        """
        self._offset.setValue(value)

    def set_scale(self, value):
        """Set scale of the component

        :param value: scale
        :type value: float
        """
        self._scale.setValue(value)
    
    def set_text(self, text):
        """Set text of the component

        :param value: text
        :type value: float
        """
        self._name = text
        self._checkbox.setText("{}".format(self._name))
        