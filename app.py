"""Main App file"""
import dearpygui.dearpygui as dpg
import numpy as np

from yakobi_rotation import yakobi_rotation


class App:
    """Main application."""
    def _update_table(self) -> None:
        """Function for updating table."""
        rows_and_cols = int(dpg.get_value("RowsAndCols"))

        dpg.delete_item("Result")
        dpg.delete_item("Check")
        dpg.delete_item("Table")
        dpg.delete_item("Button")

        with dpg.table(id="Table", parent="Primary Window", header_row=False):
            for j in range(rows_and_cols):
                dpg.add_table_column(parent="Table")
            for i in range(rows_and_cols):
                with dpg.table_row(parent="Table"):
                    for j in range(rows_and_cols):
                        dpg.add_input_int(tag=f"Cell: {i} {j}", default_value=0)

        dpg.add_button(tag="Button", label="Calculate", callback=self.yakobi, parent="Primary Window")

    def _transform_table_into_matrix(self):
        rows_and_cols = int(dpg.get_value("RowsAndCols"))
        _matrix = []
        for i in range(rows_and_cols):
            _arr = []
            for j in range(rows_and_cols):
                _arr.append(int(dpg.get_value(f"Cell: {i} {j}")))
            _matrix.append(_arr)
        return np.array(_matrix, dtype=np.float64)

    def yakobi(self) -> None:
        """Yakobi rotation usage."""
        matrix = self._transform_table_into_matrix()
        eps = dpg.get_value("Eps")
        result, responce = yakobi_rotation(matrix, eps)
        dpg.delete_item("Result")
        dpg.delete_item("Check")
        if result:
            dpg.add_text(f"Matrix:\n{matrix}\nA:\n{result[0]}\nV:\n{result[1]}\nMessage:{responce}",
                         parent="Primary Window",
                         tag="Result")
            dpg.add_text(tag="Check",
                         parent="Primary Window",
                         default_value=f"Check:\n{np.dot(np.dot(result[1], result[0]), result[1].T)}")
        else:
            dpg.add_text(f"Message:{responce}",
                         parent="Primary Window",
                         tag="Result")

    def __init__(self) -> None:
        """Drawing the main app on class init."""
        dpg.create_context()

        with (dpg.window(tag="Primary Window")):
            dpg.add_text("Select Matrix Size")
            with dpg.group(horizontal=True):
                dpg.add_combo(tag="RowsAndCols",
                              items=[str(i) for i in range(2,8)],
                              width=100,
                              default_value="2",
                              callback=self._update_table)
            dpg.add_text("Select epsilon")
            dpg.add_input_float(default_value=0.1, tag="Eps")
            dpg.add_text("Fill in Matrix")
            self._update_table()

        dpg.create_viewport(title='Jacobi rotation method', large_icon='logo.ico')
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()


if __name__ == '__main__':
    App()
