import csv
import os
import openpyxl
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog,QMessageBox,QFileDialog, QVBoxLayout, QPushButton, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,QInputDialog
import pandas as pd


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.current_file_path = None
        self.table_widgets = []
        self.dialog = QDialog()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(815, 635)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create a vertical layout for the central widget
        central_layout = QVBoxLayout(self.centralwidget)

        # Add a tab widget
        self.tabWidget = QTabWidget(self.centralwidget)
        central_layout.addWidget(self.tabWidget)

        # Initial tab
        self.addNewTab()  # Add an initial tab

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()

        # Extract button setup
        self.btExtract = QtWidgets.QPushButton(self.centralwidget)
        self.btExtract.setObjectName("btExtract")
        button_layout.addWidget(self.btExtract)

        # Add Empty Row button setup
        self.btAddEmptyRow = QtWidgets.QPushButton(self.centralwidget)
        self.btAddEmptyRow.setObjectName("btAddEmptyRow")
        self.btAddEmptyRow.setText("Add Empty Row")
        button_layout.addWidget(self.btAddEmptyRow)

        # Delete selected row
        self.btDeleteSelectedRow = QtWidgets.QPushButton(self.centralwidget)
        self.btDeleteSelectedRow.setObjectName("btDeleteSelectedRow")
        self.btDeleteSelectedRow.setText("Delete Selected Row")
        button_layout.addWidget(self.btDeleteSelectedRow)

       
        # Find Null Values button setup
        self.btFindNullValue = QtWidgets.QPushButton(self.centralwidget)
        self.btFindNullValue.setObjectName("btFindNullValue")
        button_layout.addWidget(self.btFindNullValue)

        # Delete Null Values button setup
        self.btDeleteNullValue = QtWidgets.QPushButton(self.centralwidget)
        self.btDeleteNullValue.setObjectName("btDeleteNullValue")
        button_layout.addWidget(self.btDeleteNullValue)

        # Refresh button
        self.btRefreshData = QtWidgets.QPushButton(self.centralwidget)
        self.btRefreshData.setObjectName("btRefreshData")
        button_layout.addWidget(self.btRefreshData)

        self.btLoad = QtWidgets.QPushButton(self.centralwidget)
        self.btLoad.setObjectName("btLoad")
        self.btAddTab = QtWidgets.QPushButton(self.centralwidget)
        self.btAddTab.setObjectName("btAddTab")
        self.btRemoveTab = QtWidgets.QPushButton(self.centralwidget)
        self.btRemoveTab.setObjectName("btRemoveTab")
        button_layout.addWidget(self.btLoad)
        button_layout.addWidget(self.btAddTab)
        button_layout.addWidget(self.btRemoveTab)

        # Set the central widget's layout to the created QVBoxLayout
        central_layout.addLayout(button_layout)

        # Set the central widget's layout to the created QVBoxLayout
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 815, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")

        # SetupUi Save As
        self.actionSaveAs= QtGui.QAction(MainWindow)
        self.actionSaveAs.setObjectName("Save As")
        self.menuFile.addAction(self.actionSaveAs)

        self.actionSave= QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("Save")
        self.menuFile.addAction(self.actionSave)

        self.actionImport_File = QtGui.QAction(MainWindow)
        self.actionImport_File.setObjectName("actionImport_File")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport_File)
        self.menubar.addAction(self.menuFile.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect actions
        self.btExtract.clicked.connect(self.loadData)
        self.btAddTab.clicked.connect(self.addNewTab)
        self.btRemoveTab.clicked.connect(self.removeCurrentTab)
        self.tabWidget.tabBarDoubleClicked.connect(self.handleTabDoubleClick)
        self.actionSaveAs.triggered.connect(self.saveData)
        self.actionSave.triggered.connect(self.Save)
        self.btRefreshData.clicked.connect(self.refreshData)
        self.btAddEmptyRow.clicked.connect(self.addEmptyRow)
        self.btDeleteSelectedRow.clicked.connect(self.deleteSelectedRow)
        self.btFindNullValue.clicked.connect(self.markNullRows)

    
    def markNullRows(self):
        # Lấy tab hiện tại
        current_index = self.tabWidget.currentIndex()
        if current_index >= 0:
            table_widget = self.table_widgets[current_index]
            tab = self.tabWidget.widget(current_index)

            for row in range(table_widget.rowCount()):
                null_row = False
                for col in range(table_widget.columnCount()):
                    item = table_widget.item(row, col)
                    if item is not None:
                        text = item.text().strip()
                        if text == '' or text.lower() == 'nan' or (text.lower() == 'null'):
                            null_row = True
                            break
                    
                # Đánh dấu dòng null bằng màu sắc hoặc biểu tượng
                if null_row:
                    for col in range(table_widget.columnCount()):
                        item = table_widget.item(row, col)
                        if item is not None:
                            item.setBackground(QtGui.QColor(255, 0, 0)) # Đặt màu nền là đỏ cho các ô trong dòng null

            self.showMessageBox("Mark Null Rows", "Null rows have been marked.")
        else:
            self.showMessageBox("Info", "No tab selected.")
    def addEmptyRow(self):
        current_index = self.tabWidget.currentIndex()
        if current_index >= 0:
            table_widget = self.table_widgets[current_index]
            tab = self.tabWidget.widget(current_index)
            table_widget = tab.findChild(QTableWidget)
            current_row_count = table_widget.rowCount()
            table_widget.setRowCount(current_row_count + 1)

    def deleteSelectedRow(self):
        # Lấy tab hiện tại
        current_index = self.tabWidget.currentIndex()
        if current_index >= 0:
            table_widget = self.table_widgets[current_index]
            tab = self.tabWidget.widget(current_index)
            table_widget = tab.findChild(QTableWidget)

            # Lấy danh sách các hàng được chọn
            selected_rows = set(item.row() for item in table_widget.selectedItems())

            # Sắp xếp các hàng theo thứ tự giảm dần để xóa chúng từ dưới lên
            rows_to_delete = sorted(list(selected_rows), reverse=True)

            for row in rows_to_delete:
                table_widget.removeRow(row)

            self.showMessageBox("Success", "Selected rows deleted successfully!")
        else:
            self.showMessageBox("Info", "No tab selected.")

    def refreshData(self):
        # Kiểm tra xem có đường dẫn file dữ liệu hiện tại không
        if self.current_file_path:
            # Thực hiện các thao tác cần thiết để tải lại dữ liệu từ đường dẫn đã lưu
            file_path = self.current_file_path  # Lấy đường dẫn file dữ liệu đã lưu
            # Tiếp tục với việc tải lại dữ liệu từ đường dẫn file_path, giống như trong hàm loadData
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                print("Unsupported file format")
                return

            # Lấy tab hiện tại
            current_index = self.tabWidget.currentIndex()
            if current_index >= 0:
                tab = self.tabWidget.widget(current_index)
                table_widget = tab.findChild(QTableWidget)

                # Kiểm tra xem bảng có dữ liệu không
                if table_widget.rowCount() > 0:
                    # Xóa tất cả dữ liệu hiện có trong bảng
                    table_widget.setRowCount(0)
                    table_widget.setColumnCount(0)

                # Set lại dữ liệu từ DataFrame lên table widget
                table_widget.setRowCount(df.shape[0])
                table_widget.setColumnCount(df.shape[1])
                table_widget.setHorizontalHeaderLabels(df.columns.astype(str))

                for row in range(df.shape[0]):
                    for col in range(df.shape[1]):
                        item = QTableWidgetItem(str(df.iloc[row, col]))
                        table_widget.setItem(row, col, item)

                self.showMessageBox("Success", "Data refreshed successfully!")
            else:
                self.showMessageBox("Info", "No tab selected.")
        else:
            self.showMessageBox("Info", "No data to refresh.")

    # Message Box
    def showMessageBox(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()

    # Function Save 
    def Save(self):
        # Get the currently selected tab
        current_index = self.tabWidget.currentIndex()
        if current_index >= 0:
            tab = self.tabWidget.widget(current_index)
            table_widget = tab.findChild(QTableWidget)

            # Get the data from the table widget
            data = []
            header_labels = []
            for col in range(table_widget.columnCount()):
                header_labels.append(table_widget.horizontalHeaderItem(col).text())
            data.append(header_labels)

            for row in range(table_widget.rowCount()):
                row_data = []
                for col in range(table_widget.columnCount()):
                    item = table_widget.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                data.append(row_data)

            # Get the original file path from the tab's tooltip
            original_file_path = tab.toolTip()
            if original_file_path:
                try:
                    if original_file_path.lower().endswith('.csv'):
                        # Write data to a CSV file
                        with open(original_file_path, 'w', newline='') as csv_file:
                            writer = csv.writer(csv_file)
                            for row in data:
                                writer.writerow(row)
                        print("CSV data saved successfully.")
                    elif original_file_path.lower().endswith('.xlsx'):
                        # Write data to an Excel file using pandas
                        df = pd.DataFrame(data[1:], columns=data[0])
                        df.to_excel(original_file_path, index=False)
                        print("Excel data saved successfully.")
                    else:
                        print("Unsupported file format.")

                    # Hiển thị thông báo cho người dùng
                    self.showMessageBox("Success", "Data saved successfully!")

                except Exception as e:
                    print(f"Error saving data: {str(e)}")
                    self.showMessageBox("Error", f"Error saving data: {str(e)}")
    # Function Save As
    def saveData(self):
        # Get the currently selected tab
        current_index = self.tabWidget.currentIndex()
        if current_index >= 0:
            tab = self.tabWidget.widget(current_index)
            table_widget = tab.findChild(QTableWidget)

            # Get the data from the table widget
            data = []
            header_labels = []
            for col in range(table_widget.columnCount()):
                header_labels.append(table_widget.horizontalHeaderItem(col).text())
            data.append(header_labels)

            for row in range(table_widget.rowCount()):
                row_data = []
                for col in range(table_widget.columnCount()):
                    item = table_widget.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                data.append(row_data)

            # Get the file path to save the data
            save_file_path = self.getSaveFileName()
            if save_file_path:
                try:
                    if save_file_path.endswith('.txt'):
                        # Save data to a text file
                        with open(save_file_path, 'w') as file:
                            for row in data:
                                file.write(','.join(row) + '\n')
                    elif save_file_path.endswith('.csv'):
                        # Convert data to a DataFrame
                        df = pd.DataFrame(data[1:], columns=data[0])

                        # Save data to a CSV file
                        df.to_csv(save_file_path, index=False)
                    else:
                        # Convert data to a DataFrame
                        df = pd.DataFrame(data[1:], columns=data[0])

                        # Save data to an Excel file
                        df.to_excel(save_file_path, index=False)

                    print("Data saved successfully.")

                    # Dislay messagebox
                    self.showMessageBox("Success", "Data saved successfully!")

                except Exception as e:
                    print(f"Error saving data: {str(e)}")

                    # Hiển thị hộp thoại thông báo lỗi
                    self.showMessageBox("Error", f"Error saving data: {str(e)}")

    def addNewTab(self):
        # Create a new tab with a table widget
        tab = QtWidgets.QWidget()
        self.tabWidget.addTab(tab, f"Tab {self.tabWidget.count() + 1}")

        # Create a table widget in the new tab
        table_widget = QTableWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.addWidget(table_widget)
        tab.setLayout(tab_layout)

        # Add the table widget to the list
        self.table_widgets.append(table_widget)

    def removeCurrentTab(self):
        # Remove the current tab
        current_index = self.tabWidget.currentIndex()
        if current_index >= 0:
            self.tabWidget.removeTab(current_index)
    def handleTabDoubleClick(self, index):
        # Get the current tab text
        current_tab_text = self.tabWidget.tabText(index)
        # Show an input dialog to get a new tab name from the user
        new_tab_text, ok = QInputDialog.getText(
        self.centralwidget,
            "Rename Tab",
            "Enter a new name for the tab:",
            text=current_tab_text,
        )
        # If the user clicks OK and provides a new name, update the tab text
        if ok and new_tab_text.strip():
            self.tabWidget.setTabText(index, new_tab_text)
    
    def getFileName(self):
        file_filter = 'Data File (*.xlsx *.csv *.txt *.xlsx *.xls) ;;Image File (*.png *.jpg)'
        response = QFileDialog.getOpenFileName(
            parent=self.centralwidget,
            caption='Select a file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)'
        )
        return response[0]

    def getFileNames(self):
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls);; Image File (*.png *.jpg)'
        response = QFileDialog.getOpenFileNames(
            parent=self.centralwidget,
            caption='Select file(s)',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)'
        )
        return response[0]

    def getDirectory(self):
        response = QFileDialog.getExistingDirectory(
            self.centralwidget,
            caption='Select a folder',
            directory=os.getcwd()
        )
        return response

    def getSaveFileName(self):
        file_filter = 'All file (*.xlsx *.xls *.csv *.txt) ;; Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;Text Files (*.txt)'
        response = QFileDialog.getSaveFileName(
            parent=self.centralwidget,
            caption='Select a data file',
            filter=file_filter,
            initialFilter='All file (*.xlsx *.xls *.csv *.txt)'
        )
        return response[0]
    
    def loadData(self):
        file_path = self.getFileName()  # Get the selected file path
        if file_path:
            self.current_file_path = file_path
            # Check if the selected file is a CSV or Excel file
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path,encoding='ISO-8859-1')
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                print("Unsupported file format")
                return

            # Get the currently selected tab
            current_index = self.tabWidget.currentIndex()
            if current_index >= 0:
                tab = self.tabWidget.widget(current_index)
                table_widget = tab.findChild(QTableWidget)

                # Clear the existing table widget
                table_widget.setRowCount(0)
                table_widget.setColumnCount(0)

                # Set the table widget with data from the DataFrame
                table_widget.setRowCount(df.shape[0])
                table_widget.setColumnCount(df.shape[1])
                table_widget.setHorizontalHeaderLabels(df.columns.astype(str))

                for row in range(df.shape[0]):
                    for col in range(df.shape[1]):
                        item = QTableWidgetItem(str(df.iloc[row, col]))
                        table_widget.setItem(row, col, item)

                # Store the original file path in the tab's tooltip
                tab.setToolTip(file_path)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btExtract.setText(_translate("MainWindow", "Extract"))
        self.btFindNullValue.setText(_translate("MainWindow", "Find Null Values"))
        self.btLoad.setText(_translate("MainWindow", "Load"))
        self.btAddTab.setText(_translate("MainWindow", "Add Tab"))
        self.btRemoveTab.setText(_translate("MainWindow", "Remove Tab"))
        self.menuFile.setTitle(_translate("MainWindow", "Window"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionImport_File.setText(_translate("MainWindow", "Import File"))
        self.actionSaveAs.setText(_translate("MainWindow", "Save As"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.btRefreshData.setText(_translate("MainWindow", "Refresh Data"))
        self.btDeleteSelectedRow.setText(_translate("MainWindow", "Delete Selected Row"))
        self.btDeleteNullValue.setText(_translate("MainWindow", "Delete Null Value"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # Change name program
    MainWindow.setWindowTitle("ETL TOOL")
    # Icon window
    icon = QtGui.QIcon("etl_icon.png")
    MainWindow.setWindowIcon(icon)
    # Showing and Exiting window
    MainWindow.show()
    sys.exit(app.exec())
