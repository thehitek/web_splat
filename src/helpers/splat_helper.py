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
                [self.executable, "--help"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.returncode == 0
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

    def calculate_path_loss(self, input_file: str, output_file: str):
        """
        Calculate path loss using the input file and save the result to the output file.

        :param input_file: Path to the input file.
        :param output_file: Path to the output file.
        :return: The CompletedProcess object containing the result of the execution.
        """
        return self.run("-t", input_file, "-o", output_file)

    def generate_terrain_profile(self, transmitter_file: str, receiver_file: str, output_file: str):
        """
        Generate a terrain profile between a transmitter and receiver.

        :param transmitter_file: Path to the transmitter file.
        :param receiver_file: Path to the receiver file.
        :param output_file: Path to the output file.
        :return: The CompletedProcess object containing the result of the execution.
        """
        return self.run("-t", transmitter_file, "-r", receiver_file, "-o", output_file)

    def calculate_field_strength(self, input_file: str, output_file: str):
        """
        Calculate field strength using the input file and save the result to the output file.

        :param input_file: Path to the input file.
        :param output_file: Path to the output file.
        :return: The CompletedProcess object containing the result of the execution.
        """
        return self.run("-f", input_file, "-o", output_file)

    def generate_coverage_map(self, input_file: str, output_file: str):
        """
        Generate a coverage map using the input file and save the result to the output file.

        :param input_file: Path to the input file.
        :param output_file: Path to the output file.
        :return: The CompletedProcess object containing the result of the execution.
        """
        return self.run("-c", input_file, "-o", output_file)

    def calculate_interference(self, input_file: str, output_file: str):
        """
        Calculate interference using the input file and save the result to the output file.

        :param input_file: Path to the input file.
        :param output_file: Path to the output file.
        :return: The CompletedProcess object containing the result of the execution.
        """
        return self.run("-i", input_file, "-o", output_file)