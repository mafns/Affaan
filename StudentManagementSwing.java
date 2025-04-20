import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.Color;
import java.io.*;
import java.util.regex.*;

public class StudentManagementSwing extends JFrame {
    private final DefaultTableModel tableModel;
    private final JTable table;
    private final JTextField idField, nameField, ageField, yearOfJoiningField;
    private final JComboBox<String> departmentComboBox;
    private String fileName = "students.xlsx"; // File for student data

    public StudentManagementSwing() {
        setTitle("Student Management System");
        setSize(600, 450);  // Adjusted size to accommodate fields
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Table Setup
        String[] columns = {"ID", "Name", "Age", "Year of Joining", "Department"};
        tableModel = new DefaultTableModel(columns, 0);
        table = new JTable(tableModel);

        JScrollPane tableScrollPane = new JScrollPane(table);

        // Form Setup
        JPanel formPanel = new JPanel(new GridLayout(0, 2));
        idField = new JTextField();
        nameField = new JTextField();
        ageField = new JTextField();
        yearOfJoiningField = new JTextField();  // Year of Joining field

        // Department Drop-down menu
        String[] departments = {"BBA","Biotech","Chemical Engineering","Civil Engineering", "Computer Science","Electrical Engineering", "Mechanical Engineering"};
        departmentComboBox = new JComboBox<>(departments);

        formPanel.add(new JLabel("ID:"));
        formPanel.add(idField);
        formPanel.add(new JLabel("Name:"));
        formPanel.add(nameField);
        formPanel.add(new JLabel("Age:"));
        formPanel.add(ageField);
        formPanel.add(new JLabel("Department:"));
        formPanel.add(departmentComboBox);  // Department combo box
        formPanel.add(new JLabel("Year of Joining:"));
        formPanel.add(yearOfJoiningField);  // Year of Joining field
        idField.addActionListener(e -> nameField.requestFocus());
        nameField.addActionListener(e -> ageField.requestFocus());
        ageField.addActionListener(e -> departmentComboBox.requestFocus());
        departmentComboBox.addActionListener(e -> yearOfJoiningField.requestFocus());
        // Layout Setup
        setLayout(new BorderLayout());
        add(tableScrollPane, BorderLayout.CENTER);
        add(formPanel, BorderLayout.NORTH);

        // Button Panel for Add, Update, Delete
        JPanel buttonPanel = new JPanel(new FlowLayout());
        JButton addButton = new JButton("Add");
        addButton.setForeground(Color.white);
        addButton.addActionListener(e -> addStudent());
        addButton.setBackground(Color.gray);
        JButton updateButton = new JButton("Update");
        updateButton.addActionListener(e -> updateStudent());
        updateButton.setBackground(Color.gray);
        updateButton.setForeground(Color.white);
        JButton deleteButton = new JButton("Delete");
        deleteButton.addActionListener(e -> deleteStudent());
        deleteButton.setBackground(Color.gray);
        deleteButton.setForeground(Color.white);

        buttonPanel.add(addButton);
        buttonPanel.add(updateButton);
        buttonPanel.add(deleteButton);

        // Button Panel for Import/Export
        JButton importButton = new JButton("Import from Excel");
        importButton.addActionListener(e -> importFromExcel());
        importButton.setBackground(Color.gray);
        importButton.setForeground(Color.white);
        JButton exportButton = new JButton("Export to Excel");
        exportButton.addActionListener(e -> exportToExcel());
        exportButton.setBackground(Color.gray);
        exportButton.setForeground(Color.white);

        buttonPanel.add(importButton);
        buttonPanel.add(exportButton);

        add(buttonPanel, BorderLayout.SOUTH);
    }

    private void addStudent() {
        try {
            int id = Integer.parseInt(idField.getText());
            if (id > 10000) {
                showMessage("ID cannot be greater than 10000.", "Validation Error");
                return;
            }

            String name = nameField.getText();
            if (!isValidName(name)) {
                showMessage("Name cannot contain numbers.", "Validation Error");
                return;
            }

            int age = Integer.parseInt(ageField.getText());
            if (age < 17 || age > 120) {
                showMessage("Age cannot be greater than 120 or lesser than 17.", "Validation Error");
                return;
            }

            String department = (String) departmentComboBox.getSelectedItem();
            int yearOfJoining = Integer.parseInt(yearOfJoiningField.getText());
            if (yearOfJoining < 2000 || yearOfJoining > 2024) {
                showMessage("Year of Joining must be between 2000 and 2024.", "Validation Error");
                return;
            }

            if (name.isEmpty()) {
                showMessage("Name cannot be empty.", "Validation Error");
                return;
            }

            // Add row for student
            tableModel.addRow(new Object[]{id, name, age, yearOfJoining, department});
            clearFields();
        } catch (NumberFormatException e) {
            showMessage("Invalid ID, Age, or Year. Please enter numeric values.", "Validation Error");
        }
    }

    private void updateStudent() {
        int selectedRow = table.getSelectedRow();
        if (selectedRow == -1) {
            showMessage("Please select a row to update.", "No Selection");
            return;
        }

        try {
            int id = Integer.parseInt(idField.getText());
            if (id > 10000) {
                showMessage("ID cannot be greater than 10000.", "Validation Error");
                return;
            }

            String name = nameField.getText();
            if (!isValidName(name)) {
                showMessage("Name cannot contain numbers.", "Validation Error");
                return;
            }

            int age = Integer.parseInt(ageField.getText());
            if (age < 17 || age > 120) {
                showMessage("Age cannot be greater than 120 or lesser than 17.", "Validation Error");
                return;
            }

            String department = (String) departmentComboBox.getSelectedItem();
            int yearOfJoining = Integer.parseInt(yearOfJoiningField.getText());
            if (yearOfJoining < 2000 || yearOfJoining > 2024) {
                showMessage("Year of Joining must be between 2000 and 2024.", "Validation Error");
                return;
            }

            if (name.isEmpty()) {
                showMessage("Name cannot be empty.", "Validation Error");
                return;
            }

            tableModel.setValueAt(id, selectedRow, 0);
            tableModel.setValueAt(name, selectedRow, 1);
            tableModel.setValueAt(age, selectedRow, 2);
            tableModel.setValueAt(yearOfJoining, selectedRow, 3);
            tableModel.setValueAt(department, selectedRow, 4);
            clearFields();
        } catch (NumberFormatException e) {
            showMessage("Invalid ID, Age, or Year. Please enter numeric values.", "Validation Error");
        }
    }

    private void deleteStudent() {
        int selectedRow = table.getSelectedRow();
        if (selectedRow == -1) {
            showMessage("Please select a row to delete.", "No Selection");
            return;
        }
        tableModel.removeRow(selectedRow);
    }

    private boolean isValidName(String name) {
        // Regex to check if the name contains any numbers
        Pattern pattern = Pattern.compile(".\\d.");
        return !pattern.matcher(name).matches();
    }

    private void importFromExcel() {
        JFileChooser fileChooser = new JFileChooser();
        if (fileChooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
            File file = fileChooser.getSelectedFile();
            if (!file.getName().toLowerCase().endsWith(".xlsx")) {
                file = new File(file.getAbsolutePath() + ".xlsx");  // Add .xlsx extension if not present
            }
            try (FileInputStream fis = new FileInputStream(file);
                 Workbook workbook = new XSSFWorkbook(fis)) {
                Sheet sheet = workbook.getSheetAt(0);
                tableModel.setRowCount(0); // Clear current data

                for (Row row : sheet) {
                    if (row.getRowNum() == 0) continue; // Skip header row

                    int id = (int) row.getCell(0).getNumericCellValue();
                    String name = row.getCell(1).getStringCellValue();
                    int age = (int) row.getCell(2).getNumericCellValue();
                    int yearOfJoining = (int) row.getCell(3).getNumericCellValue();
                    String department = row.getCell(4).getStringCellValue();

                    tableModel.addRow(new Object[]{id, name, age, yearOfJoining, department});
                }
            } catch (Exception e) {
                showMessage("Failed to import data: " + e.getMessage(), "Import Error");
            }
        }
    }

    private void exportToExcel() {
        JFileChooser fileChooser = new JFileChooser();
        if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            File file = fileChooser.getSelectedFile();
            if (!file.getName().toLowerCase().endsWith(".xlsx")) {
                file = new File(file.getAbsolutePath() + ".xlsx");  // Add .xlsx extension if not present
            }
            try (Workbook workbook = new XSSFWorkbook()) {
                Sheet sheet = workbook.createSheet("Student Details");

                // Add header row
                Row headerRow = sheet.createRow(0);
                for (int i = 0; i < tableModel.getColumnCount(); i++) {
                    Cell cell = headerRow.createCell(i);
                    cell.setCellValue(tableModel.getColumnName(i));
                }

                // Add table data
                for (int i = 0; i < tableModel.getRowCount(); i++) {
                    Row row = sheet.createRow(i + 1);
                    for (int j = 0; j < tableModel.getColumnCount(); j++) {
                        Cell cell = row.createCell(j);
                        Object value = tableModel.getValueAt(i, j);
                        if (value instanceof Integer) {
                            cell.setCellValue((Integer) value);
                        } else if (value instanceof String) {
                            cell.setCellValue((String) value);
                        }
                    }
                }

                try (FileOutputStream fos = new FileOutputStream(file)) {
                    workbook.write(fos);
                    showMessage("Data exported successfully.", "Success");
                }
            } catch (Exception e) {
                showMessage("Failed to export data: " + e.getMessage(), "Export Error");
            }
        }
    }

    private void clearFields() {
        idField.setText("");
        nameField.setText("");
        ageField.setText("");
        yearOfJoiningField.setText("");
    }

    private void showMessage(String message, String title) {
        JOptionPane.showMessageDialog(this, message, title, JOptionPane.INFORMATION_MESSAGE);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            StudentManagementSwing frame = new StudentManagementSwing();
            frame.setVisible(true);
        });
    }
}