import subprocess
import os

class SplatHelper:
    def __init__(self, splat_path: str, splat_hd_path: str, use_hd: bool = False):
        """
        Initialize the SplatHelper class.

        :param splat_path: Path to the `splat` executable.
        :param splat_hd_path: Path to the `splat-hd` executable.
        :param use_hd: Boolean to determine whether to use `splat-hd` or `splat`.
        """
        self.splat_path = splat_path
        self.splat_hd_path = splat_hd_path
        self.use_hd = use_hd
        self.executable = self.splat_hd_path if self.use_hd else self.splat_path
        self.pardir = os.path.dirname(self.executable)

        # Verify the executable by running it with the `--help` flag
        if not self._verify_executable():
            raise RuntimeError(f"Failed to verify the executable: {self.executable}")

    def _verify_executable(self) -> bool:
        """
        Verify that the executable can be run with the `--help` flag.

        :return: True if the executable runs successfully, False otherwise.
        """
        try:
            result = subprocess.run(
                [self.executable],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.returncode == 1
        except FileNotFoundError:
            return False

    def run(self, *args) -> subprocess.CompletedProcess:
        """
        Run the selected executable with the provided arguments.

        :param args: Arguments to pass to the executable.
        :return: The CompletedProcess object containing the result of the execution.
        """
        if not os.path.isfile(self.executable):
            raise FileNotFoundError(f"Executable not found: {self.executable}")

        try:
            result = subprocess.run(
                [self.executable, *args],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to run the executable: {e}")

    def switch_to_hd(self):
        """
        Switch to using the `splat-hd` executable.
        """
        self.use_hd = True
        self.executable = self.splat_hd_path

    def switch_to_splat(self):
        """
        Switch to using the `splat` executable.
        """
        self.use_hd = False
        self.executable = self.splat_path

    # Wrapper methods for splat commands

    def calculate_kml(self, tx_qth_filepath: str, rx_qth_filepath: str):
        """Generate Google Earth (.kml) compatible output"""
        return self.run("-d",
                        "third_party/splat/sdf/", 
                        "-metric", 
                        "-t",
                        tx_qth_filepath, 
                        "-r",
                        rx_qth_filepath, 
                        "-kml")
