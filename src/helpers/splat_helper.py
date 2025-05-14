import subprocess
import os

from PIL import Image, ImageFilter

class SplatHelper:
    def __init__(self, 
                 splat_path: 
                 str, 
                 splat_hd_path: str, 
                 working_dir = None, 
                 use_hd: bool = False, 
                 sdf_path: str = None):
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
        self.working_dir = working_dir if working_dir else os.path.dirname(splat_path)
        self.sdf_path = sdf_path if sdf_path else os.path.join(self.working_dir, "sdf")

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
                [self.executable, 
                 "-d",
                 self.sdf_path,
                 "-metric", 
                 *args],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.working_dir,
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

    def calculate_kml(self):
        """Generate Google Earth (.kml) compatible output"""
        filename = "TX-to-RX.kml"
        filepath = os.path.join(self.working_dir, filename)
        os.remove(filepath) if os.path.exists(filepath) else None
        # Remove the existing KML file if it exists
        return self.run("-t", "tx.qth", 
                        "-r", "rx.qth", 
                        "-kml")
    
    def calculate_terrain_profile(self):
        """Generate terrain profile"""
        filename = "terrain_profile.png"
        filepath = os.path.join(self.working_dir, filename)

        os.remove(filepath) if os.path.exists(filepath) else None
        return self.run("-t", "tx.qth", 
                        "-r", "rx.qth", 
                        "-p", filename)
    
    def calculate_elevation_profile(self):
        """Generate elevation profile"""

        filename = "elevation_profile.png"
        filepath = os.path.join(self.working_dir, filename)

        os.remove(filepath) if os.path.exists(filepath) else None
        return self.run("-t", "tx.qth", 
                        "-r", "rx.qth", 
                        "-e", filename)
    
    def calculate_height_profile(self):
        """Generate height profile"""
        filename = "height_profile.png"
        filepath = os.path.join(self.working_dir, filename)

        os.remove(filepath) if os.path.exists(filepath) else None
        return self.run("-t", "tx.qth", 
                        "-r", "rx.qth", 
                        "-h", filename)
    
    def calculate_height_profile_norm(self):
        """Generate normalized height profile"""
        filename = "height_profile_norm.png"
        filepath = os.path.join(self.working_dir, filename)

        os.remove(filepath) if os.path.exists(filepath) else None
        return self.run("-t", "tx.qth", 
                        "-r", "rx.qth", 
                        "-H", filename)
    
    def calculate_path_loss_profile(self):
        """Generate path loss profile"""
        filename = "path_loss_profile.png"
        filepath = os.path.join(self.working_dir, filename)

        os.remove(filepath) if os.path.exists(filepath) else None
        return self.run("-t", "tx.qth", 
                        "-r", "rx.qth", 
                        "-l", filename)

    
    def calculate_tx_coverage_map(self, rx_antenna_height: int):
        """Generate tx coverage map"""
        ppm_filename = "tx_coverage_map.ppm"
        ppm_filepath = os.path.join(self.working_dir, ppm_filename)

        png_filename = "tx_coverage_map.png"
        png_filepath = os.path.join(self.working_dir, png_filename)

        os.remove(ppm_filepath) if os.path.exists(ppm_filepath) else None
        res = self.run("-t", "tx.qth", 
                        "-c", str(rx_antenna_height),
                        "-o", ppm_filename)

        with Image.open(ppm_filepath) as im:
                im.filter(ImageFilter.DETAIL)
                im.save(png_filepath, "PNG")
        return res
    
    def calculate_tx_loss_map(self, rx_antenna_height: int):
        """Generate tx loss map"""
        ppm_filename = "tx_loss_map.ppm"
        ppm_filepath = os.path.join(self.working_dir, ppm_filename)

        png_filename = "tx_loss_map.png"
        png_filepath = os.path.join(self.working_dir, png_filename)
        
        os.remove(ppm_filepath) if os.path.exists(ppm_filepath) else None
        res = self.run("-t", "tx.qth", 
                        "-L", str(rx_antenna_height),
                        "-o", ppm_filename)

        with Image.open(ppm_filepath) as im:
                im.filter(ImageFilter.DETAIL)
                im.save(png_filepath, "PNG")
        return res
    
    def calculate_tx_field_map(self, rx_antenna_height: int, erp: float):
        """Generate tx field map"""
        ppm_filename = "tx_field_map.ppm"
        ppm_filepath = os.path.join(self.working_dir, ppm_filename)

        png_filename = "tx_field_map.png"
        png_filepath = os.path.join(self.working_dir, png_filename)

        os.remove(ppm_filepath) if os.path.exists(ppm_filepath) else None
        res = self.run("-t", "tx.qth", 
                        "-L", str(rx_antenna_height),
                        "-erp", str(erp),
                        "-o", ppm_filename)

        with Image.open(ppm_filepath) as im:
                im.filter(ImageFilter.DETAIL)
                im.save(png_filepath, "PNG")
        return res
    



