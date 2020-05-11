import copy
import subprocess
from .runthis import run_this
from .runthis import tidy_command
from .runthis import run_cdo
from .temp_file import temp_file
from .cleanup import cleanup
from .cleanup import disk_clean
from .session import nc_safe
from .show import nc_variables


def cell_areas(self, join=True):
    """
    Calculate the cell areas in square meters

    Parameters
    -------------
    join: boolean
        Set to False if you only want the cell areas to be in the output. join=True adds the areas as a variable to the dataset.
    """

    if isinstance(join, bool) == False:
        raise TypeError("join is not boolean")

    # release if you need to join the cell areas to the original file
    if join:
        self.run()


    #get the cdo version

    cdo_check = subprocess.run("cdo --version", shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    cdo_version = cdo_check.split("(")[0].strip().split(" ")[-1]


    # first run the join case
    if join:

        new_files = []
        new_commands = []

        for ff in self:

            if cdo_version in ["1.9.3", "1.9.4", "1.9.5"]:

                if "cell_area" in nc_variables(ff):
                    raise ValueError("cell_area is already a variable")

                target1 = temp_file(".nc")

                cdo_command = f"cdo -gridarea {ff} {target1}"
                cdo_command = tidy_command(cdo_command)
                target1 = run_cdo(cdo_command, target1)
                new_commands.append(cdo_command)

                target = temp_file(".nc")

                cdo_command = f"cdo -merge {ff} {target1} {target}"
                cdo_command = tidy_command(cdo_command)
                target = run_cdo(cdo_command, target)
                new_files.append(target)

                new_commands.append(cdo_command)

            else:

                if "cell_area" in nc_variables(ff):
                    raise ValueError("cell_area is already a variable")

                target = temp_file(".nc")

                cdo_command = f"cdo -merge {ff} -gridarea {ff} {target}"
                cdo_command = tidy_command(cdo_command)
                target = run_cdo(cdo_command, target)
                new_files.append(target)

                new_commands.append(cdo_command)

        for x in new_commands:
            self.history.append(x)

        self.current = new_files

        self._hold_history = copy.deepcopy(self.history)

        cleanup()

    else:

        cdo_command = "-gridarea"
        run_this(cdo_command, self, output="ensemble")

    # add units

    self.set_units({"cell_area": "m^2"})

    if join:
        self.run()
        self.disk_clean()